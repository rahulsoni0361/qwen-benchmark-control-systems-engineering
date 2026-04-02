import http.client
import json
import os

# --- SETTINGS ---
OLLAMA_IP = "192.168.1.136"
OLLAMA_PORT = 11434
MODEL = "qwen-64k" 
AGENT_FILE = "agents/hannah.json"

# --- THE BENCHMARK QUESTIONS ---
TEST_QUESTIONS = [
    {
        "type": "INTUITION",
        "question": "In an N20 motor control loop, what is the physical consequence of a pole moving from the left-half-plane across the jw-axis into the right-half-plane? Explain it without using the word 'unstable'."
    },
    {
        "type": "MATHEMATICS",
        "question": "Assume an N20 motor plant: G(s) = 1.5 / (0.1s + 1). Design a Proportional-Integral (PI) controller such that the closed-loop system has a time constant of 0.05 seconds. Show the derivation of Kp and Ki."
    },
    {
        "type": "STRATEGY (BACKLASH)",
        "question": "If our 100:1 N20 gearbox has 2.5 degrees of backlash at the output, and I am using a pure PID controller for position hold, what specific physical phenomenon will I observe? How should I modify my control logic to mitigate this?"
    }
]

def run_benchmark():
    if not os.path.exists(AGENT_FILE):
        print(f"Error: {AGENT_FILE} not found.")
        return

    with open(AGENT_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    system_prompt = config['system_prompt']
    results = ""
    
    conn = http.client.HTTPConnection(OLLAMA_IP, OLLAMA_PORT, timeout=120)

    for test in TEST_QUESTIONS:
        print(f"--- Running {test['type']} test...")
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test['question']}
            ],
            "options": {"num_ctx": 65536},
            "stream": False
        }

        try:
            conn.request("POST", "/api/chat", json.dumps(payload), {"Content-Type": "application/json"})
            response = conn.getresponse()
            if response.status != 200:
                results += f"### TEST: {test['type']}\n**ERROR:** Server returned {response.status}\n\n---\n"
                continue
            
            data = json.loads(response.read().decode())
            content = data['message']['content']
            
            results += f"### TEST: {test['type']}\n**Question:** {test['question']}\n\n**Hannah's Response:**\n{content}\n\n---\n"
            
        except Exception as e:
            results += f"### TEST: {test['type']}\n**ERROR:** {e}\n\n---\n"

    conn.close()

    with open("hannah_benchmark_results.md", "w", encoding="utf-8") as f:
        f.write(f"# 📊 Hannah Agent Benchmark Results (Clean Run)\n\nModel: {MODEL}\n\n" + results)
    
    print("\n[DONE] Benchmark complete. Results saved to hannah_benchmark_results.md")

if __name__ == "__main__":
    run_benchmark()
