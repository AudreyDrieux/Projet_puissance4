import random_agent as rd
from pettingzoo.classic import connect_four_v3

# Test de l'agent créé et des méthodes choose_action et choose_action_manual
env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

random_agent = rd.RandomAgent(env)
choose_methode = 0 # variable égale à 1 si la méthode choisie est choose_action et 0 si la méthode choisie est choose_action_manual

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
        elif reward == 0:
            print("It's a draw!")
    else:
        # Take a random valid action
        observation_array = observation['observation']
        action_mask = observation['action_mask']
        if choose_methode:
            action = random_agent.choose_action(observation_array,reward,termination,truncation,info,action_mask)

        else:
            action = random_agent.choose_action_manual(observation_array,reward,termination,truncation,info,action_mask)
        print(f"{agent} plays column {action}")

        random_agent.print_board(observation_array)
    env.step(action)

env.close()

def multiple_games(num_games):
    """
    Fonction qui fait jouer deux agents aléatoires au puissance 4 plusieurs fois

    Argument: 
        un entier num_games qui correspond au nombre de parties jouées par les deux agents

    Sortie:
        un dictionnaire dont les clés sont player_0, player_1, draw, min_nb_actions, mean_nb_actions et max_nb_actions
        les valeurs associées aux clés player_0 et player_1 sont respectivement le nombre de parties gagnées par l'agent
        player_0 et par l'agent player_1
        la valeur associée à la clé draw est le nombre total de matchs nuls
        les valeurs associées aux clés min_nb_actions, mean_nb_actions et max_nb_actions sont respectivement le nombre minimal,
        moyen et maximal de coups joués

    """
    results = {'player_0' : 0, 'player_1' : 0, 'draw' : 0, 'min_nb_actions' : 0, 'mean_nb_actions' : 0, 'max_nb_actions' : 0}
    choose_methode = 0 # variable égale à 1 si la méthode choisie est choose_action et 0 si la méthode choisie est choose_action_manual
    array_nb_actions_per_games = [] # tableau dont chaque élément est le nombre de coups joués dans une partie
    
    for game in range(1,num_games+1):
        nb_actions = 0
        env = connect_four_v3.env(render_mode=None)
        env.reset(seed=42)
        random_agent = rd.RandomAgent(env)
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            
            if termination or truncation:
                action = None
                if reward == 1:
                    results[agent] += 1
                    
                elif reward == 0:
                    results['draw'] += 1
                    
            else:
                # Take a random valid action
                observation_array = observation['observation']
                action_mask = observation['action_mask']
                if choose_methode:
                    action = random_agent.choose_action(observation_array,reward,termination,truncation,info,action_mask)
                    nb_actions = nb_actions + 1

                else:
                    action = random_agent.choose_action_manual(observation_array,reward,termination,truncation,info,action_mask)
                    nb_actions = nb_actions + 1
    
            env.step(action)
        
        array_nb_actions_per_games.append(nb_actions)

        env.close()
    results['min_nb_actions'] = min(array_nb_actions_per_games)

    nb_total_actions = 0 # nombre total de coups joués 
    for nb_actions in array_nb_actions_per_games:
        nb_total_actions = nb_total_actions + nb_actions

    results['mean_nb_actions'] = nb_total_actions/num_games

    results['max_nb_actions'] = max(array_nb_actions_per_games)

    return results

# Execution de 100 parties

print(multiple_games(100))