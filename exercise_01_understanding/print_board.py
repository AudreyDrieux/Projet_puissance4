from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation):
    """
    Print a human-readable version of the board

    observation: numpy array of shape (6, 7, 2)
        observation[:,:,0] = current player's pieces
        observation[:,:,1] = opponent's pieces
    """
    # TODO: Implement this function
    # Hint: Loop through rows and columns
    # Use symbols like 'X', 'O', and '.' for current player, opponent, and empty

    nb_row = 6
    nb_column = 7

    for r in range(nb_row):
        for c in range(nb_column):
            if observation[r,c,0] != 0:
                print('X', end = " ")
                
            elif observation[r,c,1] != 0:
                print('O', end = " ")

            else:
                print('.', end = " ")

        print("\n")

    pass

# Test your function
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Make a few moves to see the board change
    env.step(3)
    if agent == env.agents[1]:
        break

env.close()