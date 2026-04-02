import requests
import json
import os
from datetime import datetime

# --- SETTINGS ---
OLLAMA_URL = "http://192.168.1.136:11434/api/chat"
MODEL = "qwen-64k"
AGENTS_DIR = "agents"
LOGS_DIR = "logs"

class EngineeringTeam:
    def __init__(self, shared_mode=True):
        self.memories = {}  # { 'hannah': [messages], 'sophie': [messages] }
        self.shared_history = [] # For Shared Mode
        self.shared_mode = shared_mode
        
        # Ensure logs directory exists
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

    def log_interaction(self, agent_name, user_input, response):
        """Append this interaction to a local log file for future RAG usage."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = os.path.join(LOGS_DIR, f"chat_log_{datetime.now().strftime('%Y-%m-%d')}.txt")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] RAHUL -> {agent_name.upper()}\n")
            f.write(f"QUERY: {user_input}\n")
            f.write(f"RESPONSE from {agent_name.upper()}:\n{response}\n")
            f.write("-" * 50 + "\n")

    def load_agent(self, agent_name):
        filename = f"{agent_name.lower()}.json"
        path = os.path.join(AGENTS_DIR, filename)
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        if agent_name not in self.memories:
            self.memories[agent_name] = [
                {"role": "system", "content": config['system_prompt']}
            ]
        return config['display_name']

    def ask(self, agent_name, user_input):
        if agent_name not in self.memories:
            self.load_agent(agent_name)
        
        if self.shared_mode:
            system_msg = self.memories[agent_name][0] 
            messages = [system_msg] + self.shared_history + [{"role": "user", "content": f"Rahul -> {agent_name.upper()}: {user_input}"}]
        else:
            self.memories[agent_name].append({"role": "user", "content": user_input})
            messages = self.memories[agent_name]

        payload = {
            "model": MODEL,
            "messages": messages,
            "options": {
                "num_ctx": 65536, # Push context to 64k for RTX 3090
                "temperature": 0.7
            },
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=600) # Increased timeout for large context
            response.raise_for_status()
            message = response.json()['message']['content']
            
            # Update Shared History
            if self.shared_mode:
                self.shared_history.append({"role": "user", "content": f"Rahul -> {agent_name.upper()}: {user_input}"})
                self.shared_history.append({"role": "assistant", "content": f"{agent_name.upper()}: {message}"})
            else:
                self.memories[agent_name].append({"role": "assistant", "content": message})
            
            # LOG FOR RAG
            self.log_interaction(agent_name, user_input, message)
            
            return message
        except Exception as e:
            return f"ERROR: {e}"

def start_interactive_session():
    team = EngineeringTeam()
    print("--- 🧠 Engineering Team: 64k Context + Logging Active ---")
    current_agent = "hannah"
    team.load_agent(current_agent)
    
    while True:
        user_input = input(f"\nRahul -> {current_agent.upper()}: ")
        
        if user_input.lower().startswith("/switch "):
            new_agent = user_input.split(" ")[1].lower()
            if team.load_agent(new_agent):
                current_agent = new_agent
                print(f"--- Switched to {current_agent.upper()} ---")
            continue

        if user_input.lower() in ['exit', 'quit']:
            break

        response = team.ask(current_agent, user_input)
        print(f"\n{current_agent.upper()}: {response}")

if __name__ == "__main__":
    start_interactive_session()
