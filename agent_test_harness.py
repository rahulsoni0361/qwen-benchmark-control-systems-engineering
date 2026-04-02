import requests
import json
import os

# --- SETTINGS ---
OLLAMA_URL = "http://192.168.1.136:11434/api/chat"
MODEL = "qwen2.5:14b"
AGENTS_DIR = "agents"
RESULTS_FILE = "agent_test_results.md"

# --- THE TEST PAPER (Complex Problem) ---
TEST_CHALLENGE = """
SCENARIO: 
An N20 100:1 Gearmotor is being used for a precision pointing task. 
- Problem 1: Sudden 12Hz oscillation appearing during steady-state hold.
- Problem 2: Current draw is 450mA (rated is 200mA, stall is 650mA).
- Problem 3: Encoder (7 PPR magnetic) shows 'phantom' steps when motor starts.
- Hardware: DRV8833 driver, STM32 MCU, 12-bit ADC.

TASK: Provide a specific technical diagnosis and one immediate action from your domain perspective.
"""

def get_agent_response(agent_file, challenge):
    with open(os.path.join(AGENTS_DIR, agent_file), 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    system_prompt = config['system_prompt']
    name = config['display_name']
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": challenge}
        ],
        "options": {
            "num_ctx": 32768
        },
        "stream": False
    }

    print(f"Testing {name}...")
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return name, response.json()['message']['content']
    except Exception as e:
        return name, f"ERROR: {e}"

def run_test():
    report = f"# 🧪 Agent Capability Test Report\n\n**Model:** {MODEL}\n**Challenge:** {TEST_CHALLENGE}\n\n---\n"
    
    # Test lead experts
    for agent_file in ['hannah.json', 'sophie.json', 'marco.json']:
        name, content = get_agent_response(agent_file, TEST_CHALLENGE)
        report += f"## 👤 Agent: {name}\n\n### Response:\n{content}\n\n---\n"
    
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Test complete. Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    if not os.path.exists(AGENTS_DIR):
        print(f"Error: {AGENTS_DIR} folder not found.")
    else:
        run_test()
