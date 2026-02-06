from collections import deque 


class LogicalAgent:
    def __init__(self, size=4):
        self.size = size
        self.kb_visited = set()
        self.kb_safe = set()
        self.kb_breezy = set() # Places where we felt breeze
        self.kb_stenchy = set() # Places where we smelt stench
        self.plan = deque() # Queue of actions to execute
        self.current_pos = (0, 0)
        self.current_dir = 0
        self.has_gold = False
        
        # Mark start as safe
        self.kb_safe.add((0, 0))

    # LAB 3: Logic / Inference
    def update_kb(self, pos, percepts):
        self.current_pos = pos
        self.kb_visited.add(pos)
        self.kb_safe.add(pos) # If we are here and alive, it is safe
        
        if percepts['Breeze']:
            self.kb_breezy.add(pos)
        if percepts['Stench']:
            self.kb_stenchy.add(pos)
            
        # DEDUCTION ENGINE
        # If a cell has NO Breeze and NO Stench, all neighbors are SAFE
        if not percepts['Breeze'] and not percepts['Stench']:
            neighbors = self.__get_neighbors(pos)
            for n in neighbors:
                self.kb_safe.add(n)
        
    def __get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                neighbors.append((nr, nc))
        return neighbors

    # Planning (Search)
    def get_action(self, percepts):
        # 1. Check Glitter
        if percepts['Glitter']:
            self.has_gold = True
            # Clear plan and route home
            self.plan.clear()
            path_home = self.__bfs_path(self.current_pos, (0, 0))
            self.__create_actions_from_path(path_home)
            self.plan.append('Climb')
            return 'Grab'

        # 2. Execute existing plan
        if self.plan:
            return self.plan.popleft()

        # 3. Plan new move: Find nearest SAFE unvisited cell
        target = self.__find_nearest_safe_unvisited()
        
        if target:
            path = self.__bfs_path(self.current_pos, target)
            self.__create_actions_from_path(path)
            if self.plan:
                return self.plan.popleft()

        # 4. If no safe unvisited cells, go home (Give up safely)
        if not self.has_gold:
            path_home = self.__bfs_path(self.current_pos, (0, 0))
            if path_home:
                self.__create_actions_from_path(path_home)
                self.plan.append('Climb') # End game
                if self.plan:
                    return self.plan.popleft()
        
        return 'Climb' # Default fallback

    def __find_nearest_safe_unvisited(self):
        # Simple BFS to find closest target
        queue = deque([self.current_pos])
        seen = {self.current_pos}
        
        while queue:
            curr = queue.popleft()
            if curr in self.kb_safe and curr not in self.kb_visited:
                return curr
            
            for n in self.__get_neighbors(curr):
                if n not in seen and n in self.kb_safe: # Only traverse through known safe cells
                    seen.add(n)
                    queue.append(n)
        return None

    def __bfs_path(self, start, goal):
        # Returns list of coordinates
        queue = deque([(start, [])])
        seen = {start}
        while queue:
            curr, path = queue.popleft()
            if curr == goal:
                return path
            
            for n in self.__get_neighbors(curr):
                if n not in seen and n in self.kb_safe: # Stay in safe zone
                    seen.add(n)
                    queue.append((n, path + [n]))
        return []

    def __create_actions_from_path(self, path):
        # Converts coordinate path to Agent Actions (TurnLeft, Move, etc.)
        # This is a mini-state machine simulation
        curr_r, curr_c = self.current_pos
        curr_dir = self.current_dir # 0:R, 1:D, 2:L, 3:U
        
        for (next_r, next_c) in path:
            # Determine required direction
            req_dir = -1
            if next_c > curr_c: req_dir = 0 # Right
            elif next_r > curr_r: req_dir = 1 # Down
            elif next_c < curr_c: req_dir = 2 # Left
            elif next_r < curr_r: req_dir = 3 # Up
            
            # Turn logic
            diff = (req_dir - curr_dir) % 4
            if diff == 1: self.plan.append('TurnRight')
            elif diff == 2: 
                self.plan.append('TurnRight')
                self.plan.append('TurnRight')
            elif diff == 3: self.plan.append('TurnLeft')
            
            self.plan.append('Forward')
            
            # Update virtual state for next step calculation
            curr_r, curr_c = next_r, next_c
            curr_dir = req_dir
            
        # Update agent real internal state to match end of plan
        # Note: real state updates happen in update_kb, this is just for action queue generation
