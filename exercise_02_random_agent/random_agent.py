"""
My Random Agent for Connect Four

This agent chooses moves randomly from the available (valid) columns.
"""

import random


class RandomAgent:
    """
    A simple agent that plays randomly
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the random agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent (for display)
        """
        # TODO
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "RandomAgent"
        pass

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose a random valid action

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            reward: float - reward from previous action
            terminated: bool - is the game over?
            truncated: bool - was the game truncated?
            info: dict - additional info
            action_mask: numpy array (7,) - which columns are valid (1) or full (0)

        Returns:
            action: int (0-6) - which column to play
        """
        # TODO: Implement random action selection
        action = self.action_space.sample(action_mask)
        return action
        pass

    def choose_action_manual(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose a random valid action without using .sample()

        This is a learning exercise to understand what action_mask does
        """
    
        # TODO: Get list of valid actions from action_mask
        valid_actions = []  # Fill this list, liste qui contient les indices des colonnes qui sont jouables
        nb_column = 7
        for i in range(nb_column):
            if action_mask[i]:
                valid_actions.append(i)

        # TODO: If no valid actions, return None (shouldn't happen in Connect Four)
        if not valid_actions:
            return None

        nb_valid_actions = len(valid_actions) # nombre d'actions valides
        index = random.randint(0,nb_valid_actions-1) # choix d'un indice de manière aléatoire et sans préférence parmi {0,1,...,nb_valid_actions-1}

        # TODO: Choose randomly from valid actions
        return valid_actions[index]  # Retourne l'indice de la colonne qui se trouve à la position index dans valid_actions
    
    def print_board(self, observation):
        """
         Affiche l'état du plateau du Puissance 4

        Arguments:
            observation : tableau de taille (6,7,2)
            observation[:,:,0] : tableau de taille 6x7 qui indique à l'agent dont 
                                 c'est le tour de jouer où sont ses pièces
            observation[:,:,1] : tableau de taille 6x7 qui indique à l'agent dont
                                 c'est le tour de jouer où sont les pièces de l'adversaire
        """

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

