import asyncio
import httpx
import json

# --- CONFIGURATION ---
OLLAMA_URL = "http://192.168.1.136:11434/api/chat"
MODEL = "qwen2.5:14b" # Using 14b for parallel stability. Switch to 27b if server is powerful.

# --- PERSONA AGENTS ---
AGENTS = {
    "Hannah": "Control Systems Engineer (Germany). Focus on math and stability. No-nonsense.",
    "Sophie": "Embedded/Electronics Engineer. Focus on PWM/ADC noise and hardware limits.",
    "Elena": "Systems Debugger (Italy). Focus on root causes and cross-domain bugs.",
    "Walter": "RF/EMI Engineer (Heisenberg). Focus on signal integrity and interference.",
    "George": "Tech Lead. Focus on integration and final direction.",
    "Tom": "The Intern. Focus on curiosity and 'why' questions."
}

async def consult_agent(name, role, problem):
    """Fires an independent request for one specific agent."""
    system_prompt = f"YOU ARE {name}: {role}. Provide your analysis for the following engineering challenge. Keep it technical and short.\n\nCHALLENGE: {problem}"
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": problem}
        ],
        "options": {
            "num_ctx": 32768
        },
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            print(f"[SYSTEM] Summoning {name}...")
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            
            content = result['message']['content']
            print(f"\n--- {name.upper()} ---")
            print(content)
            return {name: content}
            
    except Exception as e:
        print(f"[ERROR] {name} failed to respond: {e}")
        return {name: "Failed to connect."}

async def run_parallel_brainstorm(problem):
    """Orchestrates all agents simultaneously."""
    tasks = []
    for name, role in AGENTS.items():
        tasks.append(consult_agent(name, role, problem))
    
    print(f"\n🧠 STARTING PARALLEL BRAINSTORM: {problem}\n")
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    challenge = "N20 motor oscillating at low speed with random encoder jitter."
    asyncio.run(run_parallel_brainstorm(challenge))
