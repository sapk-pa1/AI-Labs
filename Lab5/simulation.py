import random
from collections import deque

from wumpus_env import WumpusEnvironment 
from agent import LogicalAgent 

def run_lab_simulation():
    env = WumpusEnvironment()
    agent = LogicalAgent(size=env.size)
    
    print("STARTING WUMPUS WORLD SIMULATION")
    env.print_state()
    
    max_steps = 50
    steps = 0
    
    while env.is_alive and steps < max_steps:
        # 1. Agent senses
        percepts = env.get_percepts()
        print(f"Percepts: {percepts}")
        
        # 2. Agent thinks
        agent.update_kb(env.agent_pos, percepts)
        agent.current_dir = env.agent_dir # Sync direction
        
        # 3. Agent acts
        action = agent.get_action(percepts)
        print(f"Agent Action: {action}")
        
        # 4. Environment Updates
        reward, status = env.step(action)
        
        env.print_state()
        
        if status == "Terminated":
            break
            
        steps += 1

    print(f"Game Over. Final Score: {env.score}")

if __name__ == "__main__":
    run_lab_simulation()