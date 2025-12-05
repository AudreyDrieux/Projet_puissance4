import smart_agent as smart
import random_agent as rd
import time
import tracemalloc
import numpy as np
from pettingzoo.classic import connect_four_v3

# Tests fonctionnels 

# Sélection d'un coup valide et d'un coup légal
def test_choose_action():
    env = connect_four_v3.env()
    env.reset(seed=42)
    smart_agent = smart.SmartAgent(env)

    # Plateau vide
    observation = np.zeros((6,7,2))

    # Toutes les colonnes sont jouables 
    action_mask = [1, 1, 1, 1, 1, 1, 1]

    action = smart_agent.choose_action(observation,reward=0.0,terminated=False,truncated=False,info=None,action_mask=action_mask)
    assert 0 <= action and action <= 6

    # Plateau vide 
    observation = np.zeros((6,7,2))
    observation[4,3,0] = 1
    observation[2,3,0] = 1
    observation[0,3,0] = 1

    observation[5,3,1] = 1
    observation[3,3,1] = 1
    observation[1,3,1] = 1

    # Toutes les colonnes sont jouables sauf celle du milieu car elle est pleine
    action_mask = [1, 1, 1, 0, 1, 1, 1]

    action = smart_agent.choose_action(observation,reward=0.0,terminated=False,truncated=False,info=None,action_mask=action_mask)
    assert action != 3

# Tests de performance

# Temps mis par l'agent pour faire un coup
def test_time_per_move():
    average_time_per_move_rd = 0
    average_time_per_move_smart = 0
    nb_moves_rd = 0
    nb_moves_smart = 0

    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    random_agent = rd.RandomAgent(env, 'player_0')
    smart_agent = smart.SmartAgent(env, 'player_1')
        
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            break          
           
        else:
            observation_array = observation['observation']
            action_mask = observation['action_mask']
            if agent == env.agents[0]:
                start = time.time()
                action = random_agent.choose_action_manual(observation_array, reward, termination, truncation, info, action_mask)
                end = time.time()
                average_time_per_move_rd += end-start
                nb_moves_rd += 1
           
            else:
                start = time.time()
                action = smart_agent.choose_action(observation_array, reward, termination, truncation, info, action_mask)
                end = time.time()
                average_time_per_move_smart += end-start
                nb_moves_smart += 1
           
        env.step(action) 
        
    env.close()
    average_time_per_move_rd /= nb_moves_rd
    average_time_per_move_smart /= nb_moves_smart
    print("Average time per move for random agent:", average_time_per_move_rd)
    print("Average time per move for smart agent:", average_time_per_move_smart)

    assert average_time_per_move_rd < 3 and average_time_per_move_smart < 3 

# Espace mémoire utilisé
def test_space_memory():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    random_agent = rd.RandomAgent(env, 'player_0')
    smart_agent = smart.SmartAgent(env, 'player_1')

    tracemalloc.start()    
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            break          
           
        else:
            observation_array = observation['observation']
            action_mask = observation['action_mask']
            if agent == env.agents[0]:
                action = random_agent.choose_action_manual(observation_array, reward, termination, truncation, info, action_mask)
           
            else:
                action = smart_agent.choose_action(observation_array, reward, termination, truncation, info, action_mask)
           
        env.step(action) 
    env.close()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f'Current: {current} bytes, Peak: {peak} bytes')
    assert peak < 10000000

# Tests stratégiques

# Détecter une victoire immédiate
def test_find_winning_move():
    env = connect_four_v3.env()
    env.reset(seed=42)
    smart_agent = smart.SmartAgent(env)

    # Plateau vide 
    observation = np.zeros((6,7,2))
    observation[5,0,0] = 1
    observation[5,1,0] = 1
    observation[5,2,0] = 1

    # Toutes les colonnes sont jouables 
    valid_actions = [0, 1, 2, 3, 4, 5, 6]

    assert smart_agent._find_winning_move(observation,valid_actions,channel=0) == 3
    
# Bloquer la victoire de l'adversaire 
def test_blocking_winning_move():
    env = connect_four_v3.env()
    env.reset(seed=42)
    smart_agent = smart.SmartAgent(env)

    # Plateau vide 
    observation = np.zeros((6,7,2))
    observation[5,0,1] = 1
    observation[5,1,1] = 1
    observation[5,2,1] = 1

    # Toutes les colonnes sont jouables 
    valid_actions = [0, 1, 2, 3, 4, 5, 6]

    assert smart_agent._find_winning_move(observation,valid_actions,channel=1) == 3

# Bloquer une double menace de l'adversaire
def test_blocking_double_threat():
    env = connect_four_v3.env()
    env.reset(seed=42)
    smart_agent = smart.SmartAgent(env)

    # Plateau vide
    observation = np.zeros((6,7,2))
    observation[4,3,0] = 1 

    observation[5,2,1] = 1
    observation[5,3,1] = 1

    # Toutes les colonnes sont jouables 
    valid_actions = [0, 1, 2, 3, 4, 5, 6]

    assert smart_agent._find_double_threat(observation,valid_actions,channel=1) == [1, 4]

# Créer une double menace
def test_creates_double_threat():
    env = connect_four_v3.env()
    env.reset(seed=42)
    smart_agent = smart.SmartAgent(env)

    # Plateau vide 
    observation = np.zeros((6,7,2))
    observation[5,3,0] = 1
    observation[5,4,0] = 1

    observation[5,0,1] = 1
    observation[4,3,1] = 1

    # Toutes les colonnes sont jouables 
    valid_actions = [0, 1, 2, 3, 4, 5, 6]

    assert smart_agent._find_double_threat(observation,valid_actions,channel=0) == [2, 5]

# Eviter une colonne qui donnerait l'opportunité à l'adversaire de gagner à son prochain tour
def test_find_threat():
    env = connect_four_v3.env()
    env.reset(seed=42)
    smart_agent = smart.SmartAgent(env)

    # Plateau vide
    observation = np.zeros((6,7,2))
    observation[5,1,0] = 1
    observation[5,3,0] = 1
    observation[4,2,0] = 1
    observation[2,2,0] = 1
    observation[1,2,0] = 1
    observation[0,2,0] = 1

    observation[5,0,1] = 1
    observation[5,2,1] = 1
    observation[5,4,1] = 1
    observation[4,1,1] = 1
    observation[4,3,1] = 1
    observation[3,2,1] = 1

    # Toutes le colonnes sont jouables sauf la colonne 2 car elle est pleine  
    valid_actions = [0, 1, 3, 4, 5, 6]

    assert smart_agent._find_threat(observation,valid_actions,channel=1) == [1, 3]

if __name__ == "__main__":
    test_choose_action()

if __name__ == "__main__":
    test_time_per_move()

if __name__ == "__main__":
    test_space_memory()

if __name__ == "__main__":
    test_find_winning_move()

if __name__ == "__main__":
    test_blocking_winning_move()

if __name__ == "__main__":
    test_blocking_double_threat()

if __name__ == "__main__":
    test_creates_double_threat()

if __name__ == "__main__":
    test_find_threat()









