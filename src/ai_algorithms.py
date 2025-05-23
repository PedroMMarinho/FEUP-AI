import copy
import time
import random
import math
from board import BoardPhase

class Node:
    def __init__(self, state):
        self.state = state  # The game state at this node
        self.parent = None  # The parent node
        self.children = []  # List of child nodes
        self.visits = 0  # Number of visits to this node
        self.wins = 0  # Number of wins for this node

    def uct_value(self, total_visits, exploration_constant=1.41):
        if self.state.board.phase == BoardPhase.PREP:
             exploration_constant = 2
        else:
            exploration_constant = 0.7
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration_constant * (math.sqrt(math.log(total_visits) / self.visits))
    
    def __str__(self):
        return f"Visits: {self.visits}, Wins: {self.wins}"


class MonteCarlo:

    def monte_carlo(simulated_state,time_limit, stop_flag=lambda: False):
        root_node = Node(simulated_state)

        start_time = time.time()
        counter = 0
        while time.time() - start_time < time_limit and not stop_flag():
            node = root_node
            # Selection phase: Traverse the tree using UCT
            while node.children:  
                node = max(node.children, key=lambda n: n.uct_value(root_node.visits))

            # Expansion phase: Add a child node
            if not node.state.check_game_over():  # Node not terminal
                for move in node.state.legal_moves():
                    simulated_node_state = copy.deepcopy(node.state)
                    if node.state.active_connect5:
                        child_state = simulated_node_state.handle_action(seq=move)
                    else:
                        child_state = simulated_node_state.handle_action(pos=move)
                    child_node = Node(child_state)
                    child_node.parent = node
                    node.children.append(child_node)
            
            # Simulation phase: Simulate a random game from the child node
            if not node.state.check_game_over():
                child_node = random.choice(node.children)
                copy_node_state = copy.deepcopy(child_node.state)
                node = child_node
                result = MonteCarlo.simulate(copy_node_state)
            else:
                result = node.state.get_result()
            
            
            # Backpropagation phase: Update the node statistics
            while node:
                node.visits += 1
                node.wins += result  # result could be 1 for win, 0 for loss/draw
                node = node.parent
            counter += 1
        if stop_flag():
            return None
        best_node = max(root_node.children, key=lambda n: n.wins // n.visits if n.visits > 0 else n.visits)
        return best_node.state  # Return the best state (next move)
    

    def simulate(state):
        # Randomly play until the game is over
        while not state.check_game_over():
            legal_moves = state.legal_moves()

            if not legal_moves:
                return 0 

            # Randomly select a move
            move = random.choice(legal_moves)

            if state.active_connect5:
                state.handle_action(seq=move, simul=True)
            else:
                state.handle_action(pos=move, simul=True)


        # Return the result of the game (win or loss)
        return state.get_result()
    


class MiniMax:

    def best_move(state,depth,stop_flag=lambda: False):
        best_move_2 = None
        if stop_flag():
            return None
        best_val = float('-inf')
        best_move = None
        alpha, beta = float('-inf'), float('inf')
        start = time.time()
        for move in state.legal_moves():
            if stop_flag():
                return None
            copy_state = copy.deepcopy(state)
            # Double movement - remove markers, remvove ring
            if state.active_connect5:
                copy_state.handle_action(seq=move, simul=True)
                (move_val,move_2) = MiniMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True, double_move=True)
            # Double movemente - place marker, move ring
            elif state.board.phase == BoardPhase.GAME and not state.board.marker_placed and not state.board.remove_ring_phase:
                copy_state.handle_action(pos=move, simul=True)
                (move_val,move_2) = MiniMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True, double_move=True)
            elif state.board.phase == BoardPhase.PREP: 
                move_val = state.eval_prep_move_ai(move)
                if move_val == best_val and random.random() < 0.85:
                    best_move = move
                move_2 = None
            else:
                copy_state.handle_action(pos=move, simul=True)
                (move_val,move_2) = MiniMax.minimax_alpha_beta(copy_state, depth - 1, alpha, beta, False)
            if move_val > best_val:
                best_val = move_val
                best_move = move
                best_move_2 = move_2
            alpha = max(alpha, best_val)
        end = time.time()
        while end - start < 1: # Min 1 sec play
            end = time.time()

        if best_move_2: # Double movement case, return both moves since they are in the same turn
            return best_move, best_move_2,end - start
        else:
            return best_move, None,end - start


    def minimax_alpha_beta(state, depth, alpha, beta, maximizing, double_move=False, prev_eval=None, streak=0):
        eval = state.evaluate()  # Evaluate at every step
        if depth == 0 or state.check_game_over():
            return eval, None  # Terminal node, return eval
        
        if maximizing:
            max_eval = float('-inf')
            for move in state.legal_moves():
                copy_state = copy.deepcopy(state)

                if state.active_connect5:
                    copy_state.handle_action(seq=move, simul=True)
                    next_eval,_ = MiniMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True, eval, streak)
                elif state.board.phase == BoardPhase.GAME and not state.board.marker_placed and not state.board.remove_ring_phase:
                    copy_state.handle_action(pos=move, simul=True)
                    next_eval,_ = MiniMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True, eval, streak)
                else:
                    copy_state.handle_action(pos=move, simul=True)
                    next_eval,_ = MiniMax.minimax_alpha_beta(copy_state, depth - 1, alpha, beta, False, eval, streak)

                # Stability check
                if prev_eval is not None:
                    if next_eval > prev_eval:
                        streak += 1
                        if streak >= 2:
                            next_eval += 100
                    else:
                        streak = 0

                max_eval = max(max_eval, next_eval)
                if double_move and max_eval == next_eval:
                    best_move = move
                alpha = max(alpha, next_eval)
                if beta <= alpha:
                    break
            if double_move: # Double movement case, return both moves since they are in the same turn
                return max_eval, best_move
            else:  
                return max_eval, None
        else:
            min_eval = float('inf')
            for move in state.legal_moves():
                copy_state = copy.deepcopy(state)

                if state.active_connect5:
                    copy_state.handle_action(seq=move, simul=True)
                    next_eval,_ = MiniMax.minimax_alpha_beta(copy_state, depth, alpha, beta, False, eval, streak)
                elif state.board.phase == BoardPhase.GAME and not state.board.marker_placed and not state.board.remove_ring_phase:
                    copy_state.handle_action(pos=move, simul=True)
                    next_eval,_ = MiniMax.minimax_alpha_beta(copy_state, depth, alpha, beta, False, eval, streak)
                else:
                    copy_state.handle_action(pos=move, simul=True)
                    next_eval,_ = MiniMax.minimax_alpha_beta(copy_state, depth - 1, alpha, beta, True, eval, streak)

                # Instability penalty
                if prev_eval is not None:
                    if next_eval < prev_eval - 100:
                        streak += 1
                        if streak >= 2:
                            next_eval -= 100
                    else:
                        streak = 0

                min_eval = min(min_eval, next_eval)
                if double_move and min_eval == next_eval:
                    best_move = move
                beta = min(beta, next_eval)
                if beta <= alpha:
                    break  
            if double_move: # Double movement case, return both moves since they are in the same turn
                return min_eval, best_move
            else:  
                return min_eval, None