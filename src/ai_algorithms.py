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

    def monte_carlo(simulated_state,time_limit):
        root_node = Node(simulated_state)

        start_time = time.time()
        counter = 0
        while time.time() - start_time < time_limit:
            node = root_node
            #print(f"CURRENT NODE: {node}")
            # Selection phase: Traverse the tree using UCT
            while node.children:  
                # print("SELCTION")
                #print(f"VISITS: {root_node.visits}")
                node = max(node.children, key=lambda n: n.uct_value(root_node.visits))

            # Expansion phase: Add a child node
            if not node.state.check_game_over():  # Node not terminal
                #  print("EXPANSION")
                for move in node.state.legal_moves():
                    #print(f"VALID MOVE: {move}")
                    simulated_node_state = copy.deepcopy(node.state)
                    if node.state.active_connect5:
                        child_state = simulated_node_state.handle_action(seq=move)
                    else:
                        child_state = simulated_node_state.handle_action(pos=move)
                    child_node = Node(child_state)
                    child_node.parent = node
                    node.children.append(child_node)
                    #print(f"CHILD NODE ADD: {child_node}")
            
            # Simulation phase: Simulate a random game from the child node
            if not node.state.check_game_over():
                # print("SIMULATION")
                child_node = random.choice(node.children)
                #print(child_node)
                #print(child_node.state)
                copy_node_state = copy.deepcopy(child_node.state)
                node = child_node
                result = MonteCarlo.simulate(copy_node_state)
            else:
                result = node.state.get_result()
            
            #print(f"RESULT: {result}")
            
            # Backpropagation phase: Update the node statistics
            while node:
                # print("BACKPROP")
                node.visits += 1
                node.wins += result  # result could be 1 for win, 0 for loss
                #print(node.parent)
                node = node.parent
                #print("END BACKPROP")
            counter += 1
        best_node = max(root_node.children, key=lambda n: n.wins // n.visits if n.visits > 0 else n.visits)
        # print(f"COUNTER: {counter}")
        # print(f"VV: {best_node.visits, best_node.wins}")
        # for child in root_node.children:
            #  print(f"{child}\n")
        return best_node.state  # Return the best state (next move)
    

    def simulate(state):
        # Randomly play until the game is over
        while not state.check_game_over():
            legal_moves = state.legal_moves()

            # If no legal moves, return a draw (or handle as necessary)
            if not legal_moves:
                return 0  # Draw, or whatever result you define

            # Randomly select a move
            move = random.choice(legal_moves)

            if state.active_connect5:
                state.handle_action(seq=move, simul=True)
            else:
                state.handle_action(pos=move, simul=True)


        # Return the result of the game (win or loss)
        return state.get_result()
    


class MinMax:

    def best_move(state,depth):
        best_val = float('-inf')
        best_move = None
        alpha, beta = float('-inf'), float('inf')
        start = time.time()
        for move in state.legal_moves():
            copy_state = copy.deepcopy(state)
            # Double movement - remove markers, remvove ring
            if state.active_connect5:
                copy_state.handle_action(seq=move, simul=True)
                move_val = MinMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True)
            # Double movemente - place marker, move ring
            elif state.board.phase == BoardPhase.GAME and not state.board.marker_placed and not state.board.remove_ring_phase:
                copy_state.handle_action(pos=move, simul=True)
                move_val = MinMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True)
            else:
                copy_state.handle_action(pos=move, simul=True)
                move_val = MinMax.minimax_alpha_beta(copy_state, depth - 1, alpha, beta, False)
            if move_val > best_val:
                best_val = move_val
                best_move = move
            alpha = max(alpha, best_val)
        end = time.time()
        while end - start < 2: # Min 2 sec play
            end = time.time()
        return best_move

    def minimax_alpha_beta(state, depth, alpha, beta, maximizing):
        if depth == 0 or state.check_game_over():
            return state.evaluate()

        if maximizing:
            max_eval = float('-inf')
            for move in state.legal_moves():
                copy_state = copy.deepcopy(state)
                # Double movement - remove markers, remvove ring
                if state.active_connect5:
                    copy_state.handle_action(seq=move, simul=True)
                    eval = MinMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True)
                # Double movemente - place marker, move ring
                elif state.board.phase == BoardPhase.GAME and not state.board.marker_placed and not state.board.remove_ring_phase:
                    copy_state.handle_action(pos=move, simul=True)
                    eval = MinMax.minimax_alpha_beta(copy_state, depth, alpha, beta, True)
                else:
                    copy_state.handle_action(pos=move, simul=True)
                    eval = MinMax.minimax_alpha_beta(copy_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
            return max_eval
        else:
            min_eval = float('inf')
            for move in state.legal_moves():
                copy_state = copy.deepcopy(state)
                # Double movement - remove markers, remvove ring
                if state.active_connect5: 
                    copy_state.handle_action(seq=move, simul=True)
                    eval = MinMax.minimax_alpha_beta(copy_state, depth, alpha, beta, False)
                # Double movemente - place marker, move ring
                elif state.board.phase == BoardPhase.GAME and not state.board.marker_placed and not state.board.remove_ring_phase:
                    copy_state.handle_action(pos=move, simul=True)
                    eval = MinMax.minimax_alpha_beta(copy_state, depth, alpha, beta, False)
                else:
                    copy_state.handle_action(pos=move, simul=True)
                    eval = MinMax.minimax_alpha_beta(copy_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  
            return min_eval