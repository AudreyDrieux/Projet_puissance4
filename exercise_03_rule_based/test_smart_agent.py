import smart_agent as smart
import random_agent as rd
import numpy as np
import random
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode = "human")
env.reset(seed=42)

smart_agent = smart.SmartAgent(env)

# Tests unitaires de la méthode _get_valid_actions

mask = [1, 1, 1, 1, 1, 1, 1]  # Toutes les colonnes sont jouables
assert smart_agent._get_valid_actions(mask) == [0, 1, 2, 3, 4, 5, 6]

mask = [0, 1, 0, 1, 0, 1, 0]  # Seuls les indices impairs des colonnes sont jouables
assert smart_agent._get_valid_actions(mask) == [1, 3, 5]

mask = [1, 0, 1, 0, 1, 0, 1] # Seuls les indices pairs des colonnes sont jouables
assert smart_agent._get_valid_actions(mask) == [0, 2, 4, 6]

# Tests unitaires de la méthode _get_next_row

# Plateau vide : la pièce insérée ira à la dernière ligne
board = np.zeros((6, 7, 2))
assert smart_agent._get_next_row(board, 3) == 5

# Le joueur dont c'est le tour de jouer a inséré son jeton dans la colonne 3.
# Si au prochain tour, l'adversaire décide aussi de placer son jeton dans la 
# colonne 3 alors celui-ci ira au dessus du jeton placé précédemment.

board[5, 3, 0] = 1
assert smart_agent._get_next_row(board, 3) == 4

# Tests unitaires de la méthode _check_win_from_position

# Plateau vide
board = np.zeros((6, 7, 2))

# Le joueur dont c'est le tour de jouer a trois jetons dans la dernière ligne et
# qui sont dans les colonnes 1, 2, 4.
board[5,1,0] = 1
board[5,2,0] = 1
board[5,4,0] = 1

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

# Le joueur dont c'est le tour de jouer gagne s'il choisit d'insérer son jeton dans 
# la colonne 3. Un autre choix de colonne ne le fera pas gagner.
assert smart_agent._check_win_from_position(board,5,3,0) == True
assert smart_agent._check_win_from_position(board,4,4,0) == False

# Plateau vide 
board = np.zeros((6, 7, 2))

# L'adversaire a trois jetons dans la dernière ligne et qui sont dans les colonnes 0, 1 et 2.
board[5,0,1] = 1
board[5,1,1] = 1
board[5,2,1] = 1

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

# Si le joueur dont c'est le tour de jouer n'insère pas son jeton dans la colonne 3 
# alors au prochain tour, l'adversaire gagne.
assert smart_agent._check_win_from_position(board, 5, 3, 1) == True

# Test unitaire de la méthode _find_winning_move

# Plateau vide
board = np.zeros((6, 7, 2))
board[5,2,0] = 1
board[5,4,0] = 1
board[5,5,0] = 1

board[5,1,1] = 1
board[4,2,1] = 1
board[4,4,1] = 1

# Le joueur dont c'est le tour de jouer a trois jetons dans la dernière ligne et 
# qui sont dans les colonnes 2, 4 et 5.
# L'adversaire a un jeton dans la dernière ligne et qui est dans la colonne 1. Il a
# par ailleurs deux jetons dans l'avant dernière ligne et qui sont dans les colonnes 2 et 4.

# Visualisation du plateau 
smart_agent.print_board(board)
print("\n")

# Toutes les colonnes sont jouables
valid_actions = [0, 1, 2, 3, 4, 5, 6]

# Parmi les colonnes jouables, l'indice de la colonne qui permettra au joueur dont c'est le tour
# de jouer de gagner est le 3.
assert smart_agent._find_winning_move(board, valid_actions, 0) == 3

# Tests unitaires de la méthode _creates_double_threat 

# Plateau vide
board = np.zeros((6,7,2))

# Le joueur dont c'est le tour de jouer a deux jetons dans la dernière ligne et qui 
# sont dans les colonnes 2 et 3.
board[5,2,0] = 1
board[5,3,0] = 1

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

assert smart_agent._creates_double_threat(board, 1, 0) == True
assert smart_agent._creates_double_threat(board, 4, 0) == True

# Plateau vide
board = np.zeros((6,7,2))
board[5,3,0] = 1
board[5,4,0] = 1
board[4,4,0] = 1
board[4,5,0] = 1
board[3,6,0] = 1
board[2,6,0] = 1

board[4,3,1] = 1
board[3,4,1] = 1
board[3,5,1] = 1
board[5,5,1] = 1
board[5,6,1] = 1
board[4,6,1] = 1

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

assert smart_agent._creates_double_threat(board, 5, 1) == True

# Tests unitaires de la méthode _find_double_threat

# Plateau vide
board = np.zeros((6,7,2))
board[5,2,0] = 1
board[5,3,0] = 1

board[4,3,1] = 1
board[3,3,1] = 1

# Le joueur dont c'est le tour de jouer a deux jetons dans la dernière ligne et qui 
# sont dans les colonnes 2 et 3.
# L'adversaire a deux jetons dans la colonne 3 et qui sont dans les lignes 3 et 4.

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

# Toutes les colonnes sont jouables
valid_actions = [0, 1, 2, 3, 4, 5, 6]

assert smart_agent._find_double_threat(board,valid_actions,0) == [1, 4]

# Plateau vide
board = np.zeros((6,7,2))
board[5,3,0] = 1
board[5,4,0] = 1

board[5,0,1] = 1
board[5,1,1] = 1

# Le joueur dont c'est le tour de jouer a deux jetons dans la dernière ligne et qui
# sont dans les colonnes 3 et 4.
# L'adversaire a deux jetons dans la dernière ligne et qui sont dans les colonnes 0 et 1.

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

# Toutes les colonnes sont jouables
valid_actions = [0, 1, 2, 3, 4, 5, 6]

assert smart_agent._find_double_threat(board, valid_actions, 0) == [5]

# Test unitaire de la méthode _check_threat_from_position

# Plateau vide
board = np.zeros((6,7,2))
board[5,2,0] = 1
board[5,4,0] = 1
board[4,3,0] = 1
board[2,3,0] = 1
board[1,3,0] = 1
board[0,3,0] = 1

board[5,1,1] = 1
board[5,3,1] = 1
board[5,5,1] = 1
board[4,1,1] = 1
board[4,2,1] = 1
board[4,4,1] = 1
board[3,3,1] = 1

# Visualisation du plateau
smart_agent.print_board(board)
print("\n")

assert smart_agent._check_threat_from_position(board,2,1) == True
assert smart_agent._check_threat_from_position(board,4,1) == True

# Test unitaire de la méthode _find_threat

# Toutes les colonnes sont jouables sauf celle du milieu
valid_actions = [0, 1, 2, 4, 5, 6]

assert smart_agent._find_threat(board,valid_actions,channel=1) == [2, 4]

# Test de l'agent intelligent contre l'agent aléatoire

random_agent = rd.RandomAgent(env, 'player_0')
smart_agent = smart.SmartAgent(env, 'player_1')

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1 and env.agents[0] == 'player_0':
            print("Random Agent wins !")

        elif reward == 1 and env.agents[0] == 'player_1':
            print("Smart Agent wins !")

        elif reward == 0:
            print("It's a draw !")
    
    else:
        observation_array = observation['observation']
        action_mask = observation['action_mask']
        if agent == env.agents[0]:
            action = random_agent.choose_action_manual(observation_array, reward, termination, truncation, info, action_mask)
            print(f"Random Agent plays column {action}")
        else:
            action = smart_agent.choose_action(observation_array, reward, termination, truncation, info, action_mask)
            print(f"Smart Agent plays column {action}")
    
        smart_agent.print_board(observation_array)
    env.step(action)

env.close()

def multiple_games(num_games):
    """
    Fonction qui fait jouer l'agent intelligent contre l'agent aléatoire plusieurs fois

    Argument : 
        un entier num_games qui correspond au nombre de parties jouées par les deux agents

    Sortie:
        un dictionnaire dont les clés sont random_agent, smart_agent, draw, winning_move, blocking_move et choice_3
        les valeurs associées aux clés random_agent et smart_agent sont respectivement le nombre de parties gagnées par l'agent
        aléatoire et par l'agent intelligent
        la valeur associée à la clé draw est le nombre total de matchs nuls
        la valeur associée à la clé winning_move est le nombre de fois où l'agent intelligent a joué le coup gagnant
        la valeur associée à la clé blocking_move est le nombre de fois où l'agent intelligent a bloqué l'adversaire lorsque celui-ci 
        pouvait gagner  
        la valeur associée à la clé choice_3 est le nombre de fois où l'agent intelligent a choisi la colonne 3

    """
    results = {'random_agent' : 0, 'smart_agent' : 0, 'draw' : 0, 'winning_move' : 0, 'blocking_move' : 0, 'choice_3' : 0}
    
    for game in range(1,num_games+1):

        env = connect_four_v3.env(render_mode=None)
        env.reset(seed=42)
        random_agent = rd.RandomAgent(env, 'player_0')
        smart_agent = smart.SmartAgent(env, 'player_1')
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                action = None
                if reward == 1 and env.agents[0] == 'player_0':
                    results['random_agent'] += 1

                elif reward == 1 and env.agents[0] == 'player_1':
                    results['smart_agent'] += 1

                elif reward == 0:
                    results['draw'] += 1            
           
            else:
                observation_array = observation['observation']
                action_mask = observation['action_mask']
                if agent == env.agents[0]:
                    action = random_agent.choose_action_manual(observation_array, reward, termination, truncation, info, action_mask)
           
                else:
                    action = smart_agent.choose_action(observation_array, reward, termination, truncation, info, action_mask)
                    if action == 3:
                        results['choice_3'] += 1
                    
                    else:
                        valid_actions = smart_agent._get_valid_actions(action_mask)
                        winning_move = smart_agent._find_winning_move(observation_array, valid_actions, 0)
                        blocking_move = smart_agent._find_winning_move(observation_array, valid_actions, 1)
            
                        if winning_move is not None:
                            results['winning_move'] += 1

                        elif blocking_move is not None:
                            results['blocking_move'] += 1
           
            env.step(action) 
        
        env.close()
  
    return results

# Exécution de 100 parties

print(multiple_games(100))

