import numpy as np
from loguru import logger
from pettingzoo.classic import connect_four_v3

def run_tournament(agent_classes, num_games):
    """
    agent_classes: [AgentClassPlayer0, AgentClassPlayer1]
    """
    Agent0, Agent1 = agent_classes

    results = {
        "player_0_wins": 0,
        "player_1_wins": 0,
        "draws": 0,
        "games": num_games
    }

    for g in range(num_games):
        env = connect_four_v3.env(render_mode=None)
        env.reset()

        agent0 = Agent0(env, player_name="player_0")
        agent1 = Agent1(env, player_name="player_1")

        total_rewards = {"player_0": 0, "player_1": 0}

        for agent_name in env.agent_iter():
            obs, reward, termination, truncation, info = env.last()
            total_rewards[agent_name] += reward

            if termination or truncation:
                env.step(None)
                continue

            observation = obs["observation"]
            action_mask = obs["action_mask"]

            if agent_name == "player_0":
                action = agent0.choose_action(observation, reward, termination, truncation, info, action_mask)
            else:
                action = agent1.choose_action(observation, reward, termination, truncation, info, action_mask)

            env.step(action)

        if total_rewards["player_0"] == 1:
            results["player_0_wins"] += 1
        elif total_rewards["player_1"] == 1:
            results["player_1_wins"] += 1
        else:
            results["draws"] += 1

        env.close()

    return results
