import http.client
import json
import os
import time
import re

# --- SETTINGS ---
OLLAMA_IP = "192.168.1.136"
OLLAMA_PORT = 11434
MODEL = "qwen-64k"
AGENT_FILE = "agents/hannah.json"
RESULTS_FILE = "hannah_full_validation.md"

# ============================================================
# 15 QUESTIONS WITH KNOWN CORRECT ANSWERS
# Grading uses flexible regex matching to handle LaTeX formatting
# ============================================================

TESTS = [
    {
        "id": 1,
        "category": "Transfer Function",
        "question": "What is the DC gain and the pole location of G(s) = 5 / (0.2s + 1)? State numeric values clearly.",
        "correct_answer": "DC gain = 5. Pole at s = -5.",
        "grading_patterns": [r"(?:dc\s*gain|DC\s*gain).*?(?:=|is|:)\s*5(?:\.0)?\b", r"(?:pole|s)\s*=?\s*-\s*5\b"]
    },
    {
        "id": 2,
        "category": "Transfer Function",
        "question": "A 2nd-order system has transfer function G(s) = 100 / (s^2 + 10s + 100). What are the natural frequency (wn) and damping ratio (zeta)?",
        "correct_answer": "wn = 10 rad/s, zeta = 0.5",
        "grading_patterns": [r"(?:omega_n|wn|\\omega_n|natural frequency).*?(?:=|is)\s*10\b", r"(?:zeta|\\zeta|damping ratio).*?(?:=|is)\s*0\.5\b"]
    },
    {
        "id": 3,
        "category": "PI Design",
        "question": "Plant: G(s) = 1.5 / (0.1s + 1). Design a PI controller using pole-zero cancellation for a closed-loop time constant of 0.05s. What are Kp and Ki?",
        "correct_answer": "Kp = 13.33, Ki = 133.3",
        "grading_patterns": [r"K_?p\s*=\s*(?:13\.3|13\.33|\\frac\{1\}\{0\.075\})", r"K_?i\s*=\s*(?:133\.3|133|133\.33)"]
    },
    {
        "id": 4,
        "category": "PI Design",
        "question": "Plant: G(s) = 3 / (0.5s + 1). Design a PI controller using pole-zero cancellation for a closed-loop time constant of 0.1s. What are Kp and Ki?",
        "correct_answer": "Kp = 3.33, Ki = 6.67",
        "grading_patterns": [r"K_?p\s*=\s*(?:3\.33|3\.3\d)", r"K_?i\s*=\s*(?:6\.67|6\.6\d)"]
    },
    {
        "id": 5,
        "category": "Stability",
        "question": "A closed-loop system has characteristic equation s^3 + 6s^2 + 11s + 6 = 0. Is this system stable? What are the roots?",
        "correct_answer": "Stable. Roots: s = -1, -2, -3.",
        "grading_patterns": [r"stable", r"-1", r"-2", r"-3"]
    },
    {
        "id": 6,
        "category": "Stability",
        "question": "A system has open-loop transfer function L(s) = 10 / (s(s+1)(s+5)). Is this system stable in closed-loop (with unity feedback)?",
        "correct_answer": "Yes, it is stable. PM is positive (around 50 degrees).",
        "grading_patterns": [r"(?:system is |system\s+is\s+)stable|(?:positive\s+phase\s+margin)"]
    },
    {
        "id": 7,
        "category": "Time Domain",
        "question": "A 2nd-order system has wn = 10 rad/s and zeta = 0.7. What is the approximate percent overshoot and settling time (2% criterion)?",
        "correct_answer": "Overshoot ~ 4.6%. Settling time ~ 0.57s.",
        "grading_patterns": [r"(?:4\.6|4\.5|5\.0|5\.06|4\.9)\s*%", r"0\.57"]
    },
    {
        "id": 8,
        "category": "Time Domain",
        "question": "If I want less than 5% overshoot in a 2nd-order system, what is the minimum damping ratio required?",
        "correct_answer": "zeta >= 0.69 (approximately 0.7)",
        "grading_patterns": [r"(?:0\.69|0\.7|0\.70)"]
    },
    {
        "id": 9,
        "category": "Nonlinear",
        "question": "What is the specific name of the self-sustaining oscillation that occurs when a PID controller with integral action controls a plant through a gearbox with backlash? Name the analysis method used to predict its amplitude and frequency.",
        "correct_answer": "Limit cycle oscillation. Analysis method: Describing Function analysis.",
        "grading_patterns": [r"limit\s*cycle", r"describing\s*function"]
    },
    {
        "id": 10,
        "category": "Nonlinear (Backlash)",
        "question": "An N20 motor with 100:1 gearbox has 3 degrees of backlash at the output. What is the backlash at the motor shaft side?",
        "correct_answer": "3 * 100 = 300 degrees at the motor shaft.",
        "grading_patterns": [r"300\s*(?:degrees|deg)"]
    },
    {
        "id": 11,
        "category": "Discrete Time",
        "question": "If the desired control bandwidth is 50 Hz, what is the minimum acceptable sampling frequency according to the Nyquist criterion? What is the practical engineering rule-of-thumb minimum?",
        "correct_answer": "Nyquist: 100 Hz. Engineering: 500-1000 Hz (10x-20x).",
        "grading_patterns": [r"100\s*(?:Hz|hz)", r"(?:10|20)\s*(?:x|times)"]
    },
    {
        "id": 12,
        "category": "Discrete Time",
        "question": "What discretization method preserves frequency response characteristics best: Forward Euler, Backward Euler, or Tustin (Bilinear)? Answer in one word.",
        "correct_answer": "Tustin",
        "grading_patterns": [r"[Tt]ustin"]
    },
    {
        "id": 13,
        "category": "N20 Motor",
        "question": "An N20 motor has stall current 600mA at 6V. What is the winding resistance? If the motor constant is Kt = 0.01 Nm/A, what is the stall torque?",
        "correct_answer": "R = 10 ohm. Stall torque = 0.006 Nm.",
        "grading_patterns": [r"(?:R|resistance)\s*=?\s*10\s*(?:ohm|\\Omega|\u03a9)", r"0\.006\s*(?:Nm|N\\.m|N\\cdot m)"]
    },
    {
        "id": 14,
        "category": "N20 Motor",
        "question": "For an N20 motor with 100:1 gear ratio, if the motor-side inertia is J_m = 1e-7 kg.m^2 and the load inertia is J_L = 5e-4 kg.m^2, what is the total inertia reflected to the motor shaft?",
        "correct_answer": "J_total = 1.5e-7 kg.m^2",
        "grading_patterns": [r"1\.5\s*(?:\\times|x|\*|e-?)\s*10\^?\{?-?7\}?"]
    },
    {
        "id": 15,
        "category": "Conceptual",
        "question": "Why is pole-zero cancellation considered risky in practice even though it simplifies controller design on paper? Give the specific technical reason.",
        "correct_answer": "Plant parameters drift, cancellation becomes imperfect, hidden mode reappears.",
        "grading_patterns": [r"(?:parameter|model)\s*(?:drift|variation|mismatch|uncertainty)", r"(?:imperfect|incomplete|inexact)\s*cancel"]
    }
]

def run_full_validation():
    if not os.path.exists(AGENT_FILE):
        print(f"Error: {AGENT_FILE} not found.")
        return

    with open(AGENT_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    system_prompt = config['system_prompt']

    report = f"# Hannah Full Validation Report (V5 - Regex Grading)\n\n"
    report += f"**Model:** {MODEL}\n"
    report += f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n"
    report += f"**Total Questions:** {len(TESTS)}\n\n---\n\n"

    conn = http.client.HTTPConnection(OLLAMA_IP, OLLAMA_PORT, timeout=180)
    passed = 0
    failed = 0

    for test in TESTS:
        print(f"[{test['id']}/{len(TESTS)}] {test['category']}: Running...")
        start = time.time()

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test['question']}
            ],
            "options": {"num_ctx": 65536, "temperature": 0.3},
            "stream": False
        }

        try:
            conn.request("POST", "/api/chat", json.dumps(payload), {"Content-Type": "application/json"})
            response = conn.getresponse()
            data = json.loads(response.read().decode())
            content = data['message']['content']
            elapsed = round(time.time() - start, 1)

            # Regex grading
            hits = 0
            hit_details = []
            for pattern in test['grading_patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    hits += 1
                    hit_details.append(f"MATCH: {pattern}")
                else:
                    hit_details.append(f"MISS: {pattern}")

            total_keys = len(test['grading_patterns'])
            score = f"{hits}/{total_keys}"

            if hits == total_keys:
                verdict = "PASS"
                passed += 1
            else:
                verdict = "FAIL"
                failed += 1

            report += f"## Q{test['id']} [{test['category']}] - {verdict} ({score}) - {elapsed}s\n\n"
            report += f"**Question:** {test['question']}\n\n"
            report += f"**Expected:** {test['correct_answer']}\n\n"
            report += f"**Hannah said:**\n{content}\n\n"
            grading_str = "\n".join(hit_details)
            report += f"**Grading Detail:**\n```\n{grading_str}\n```\n\n---\n\n"

        except Exception as e:
            report += f"## Q{test['id']} [{test['category']}] - ERROR\n\n**Error:** {e}\n\n---\n\n"
            failed += 1

    conn.close()

    # Summary at the end
    report += f"## SUMMARY\n\n"
    report += f"| Metric | Value |\n|---|---|\n"
    report += f"| Passed | {passed}/{len(TESTS)} |\n"
    report += f"| Failed | {failed}/{len(TESTS)} |\n"
    report += f"| Accuracy | {round(passed/len(TESTS)*100, 1)}% |\n\n"

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[DONE] Validation complete: {passed}/{len(TESTS)} passed ({round(passed/len(TESTS)*100,1)}%)")
    print(f"Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    run_full_validation()
