import smart_agent as smart
import random_agent as rd
from pettingzoo.classic import connect_four_v3

# Mesure des pourcentages de victoire
def tournoi_smart_vs_random(num_games):
    """
    Fonction qui fait jouer l'agent intelligent contre l'agent aléatoire plusieurs fois

    Argument:
        un entier num_games qui correspond au nombre de parties jouées par les deux agents

    Sortie:
        un dictionnaire dont les clés sont random_agent, smart_agent et draw
        les valeurs associées aux clés random_agent et smart_agent sont respectivement
        le nombre de parties gagnées par l'agent aléatoire et par l'agent intelligent
        La valeur associée à la clé draw est le nombre total de matchs nuls
    """

    results = {'random_agent' : 0, 'smart_agent' : 0, 'draw' : 0}
    
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
           
            env.step(action) 
        
        env.close()
  
    return results

# Exécution de 100 et de 200 parties 

print(tournoi_smart_vs_random(100))
print(tournoi_smart_vs_random(200))
