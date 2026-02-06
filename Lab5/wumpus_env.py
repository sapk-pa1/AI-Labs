import random 

class WumpusEnvironment:
    def __init__(self, size=4, p_pit=0.2):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0, 0)
        self.agent_dir = 0 # 0:Right, 1:Down, 2:Left, 3:Up
        self.score = 0
        self.is_alive = True
        self.has_gold = False
        self.gold_grabbed = False
        
        # Wumpus & Arrow Mechanics
        self.wumpus_alive = True
        self.arrows = 1
        self.scream_heard = False # Tracks if Wumpus screamed this turn
        
        # Object locations
        self.wumpus_pos = None
        self.gold_pos = None
        self.pits = set()
        
        self.__initialize_world(p_pit)

    def __initialize_world(self, p_pit):
        cells = [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) != (0, 0)]
        self.gold_pos = random.choice(cells)
        self.wumpus_pos = random.choice(cells)
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) != (0, 0) and random.random() < p_pit:
                    self.pits.add((r, c))

    def get_percepts(self):
        stench = False
        breeze = False
        glitter = False
        scream = self.scream_heard 
        bump = False 
        # Reset scream after one turn
        self.scream_heard = False 
        
        r, c = self.agent_pos
        adj_cells = self.__get_adjacent_cells(r, c)
        
        for ar, ac in adj_cells:
            # Stench is only present if Wumpus is alive
            if (ar, ac) == self.wumpus_pos and self.wumpus_alive:
                stench = True
            if (ar, ac) in self.pits:
                breeze = True
                
        if self.agent_pos == self.gold_pos and not self.gold_grabbed:
            glitter = True
            
        return {'Stench': stench, 'Breeze': breeze, 'Glitter': glitter, 'Scream': scream}

    def __get_adjacent_cells(self, r, c):
        valid = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                valid.append((nr, nc))
        return valid

    def step(self, action):
        """
        Actions: 'Forward', 'TurnLeft', 'TurnRight', 'Grab', 'Shoot', 'Climb'
        """
        reward = -1 # Default cost of living
        
        if not self.is_alive:
            return reward, "Dead"

        # --- MOVEMENT ---
        if action == 'Forward':
            dr, dc = [(0, 1), (1, 0), (0, -1), (-1, 0)][self.agent_dir]
            nr, nc = self.agent_pos[0] + dr, self.agent_pos[1] + dc
            
            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.agent_pos = (nr, nc)
                # Check Death
                if self.agent_pos == self.wumpus_pos and self.wumpus_alive:
                    self.is_alive = False
                    reward -= 1000
                    print("--> DIED: Eaten by Wumpus!")
                elif self.agent_pos in self.pits:
                    self.is_alive = False
                    reward -= 1000
                    print("--> DIED: Fell in Pit!")
            else:
                print("--> BUMP! Hit a wall.")

        # --- TURNS ---
        elif action == 'TurnLeft':
            self.agent_dir = (self.agent_dir - 1) % 4
        elif action == 'TurnRight':
            self.agent_dir = (self.agent_dir + 1) % 4
            
        # --- GRAB ---
        elif action == 'Grab':
            if self.agent_pos == self.gold_pos:
                self.gold_grabbed = True
                print("--> GOLD GRABBED!")

        # --- SHOOT (New Logic) ---
        elif action == 'Shoot':
            if self.arrows > 0:
                self.arrows -= 1
                reward -= 9 # -1 base -9 extra = -10 total cost for shooting
                print("--> Swooosh... Arrow fired!")
                
                # Check if Wumpus is in the line of fire
                wr, wc = self.wumpus_pos
                ar, ac = self.agent_pos
                
                # Check alignment based on direction
                hit = False
                if self.agent_dir == 0: # Facing Right
                    if wr == ar and wc > ac: hit = True
                elif self.agent_dir == 1: # Facing Down
                    if wc == ac and wr > ar: hit = True
                elif self.agent_dir == 2: # Facing Left
                    if wr == ar and wc < ac: hit = True
                elif self.agent_dir == 3: # Facing Up
                    if wc == ac and wr < ar: hit = True
                
                if hit and self.wumpus_alive:
                    self.wumpus_alive = False
                    self.scream_heard = True
                    print("--> SCREAM!! You killed the Wumpus!")
            else:
                print("--> Click. No arrows left.")

        # --- CLIMB (Scoring Fix) ---
        elif action == 'Climb':
            if self.agent_pos == (0, 0):
                if self.gold_grabbed:
                    reward += 1000
                    print("--> ESCAPED WITH GOLD! VICTORY!")
                else:
                    print("--> Escaped without gold.")
                
                # CRITICAL FIX: Add reward to score BEFORE returning
                self.score += reward
                return reward, "Terminated"

        self.score += reward
        return reward, "Running"
    def print_state(self):
        print(f"\n--- World State (Score: {self.score}) ---")
        for r in range(self.size):
            line = "|"
            for c in range(self.size):
                cell_content = []
                if (r, c) == self.agent_pos:
                    dirs = ['>', 'v', '<', '^']
                    cell_content.append(dirs[self.agent_dir])
                if (r, c) == self.wumpus_pos and self.wumpus_alive: cell_content.append("W")
                if (r, c) == self.gold_pos and not self.gold_grabbed: cell_content.append("G")
                if (r, c) in self.pits: cell_content.append("P")
                
                line += f" {''.join(cell_content):^3} |"
            print(line)
        print("-" * (self.size * 6 + 1))