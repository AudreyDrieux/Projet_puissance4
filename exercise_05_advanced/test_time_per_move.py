import time
import numpy as np
from pettingzoo.classic import connect_four_v3
from minimax_agent import MinimaxAgent

def test_time_per_move():
    """
    Test the time per move of MinimaxAgent
    """
    np.random.seed(42)
    env = connect_four_v3.env(render_mode=None)
    env.reset()

    agent0 = MinimaxAgent(env, player_name="Minimax P0")
    agent1 = MinimaxAgent(env, player_name="Minimax P1")

    decision_times = []
    for agent_name in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            env.step(None)
            continue

        board = observation["observation"]
        action_mask = observation["action_mask"]

        start = time.time()
        if agent_name == "player_0":
            action = agent0.choose_action(board,reward=reward,terminated=termination,truncated=truncation,info=info,action_mask=action_mask,)
        else:
            action = agent1.choose_action(board,reward=reward,terminated=termination,truncated=truncation,info=info,action_mask=action_mask,)
        end = time.time()

        decision_times.append(end - start)
        env.step(action)

    env.close()

    avg_time = sum(decision_times) / len(decision_times)
    max_time = max(decision_times)
    print(f"Average decision time per move: {avg_time:.4f} s")
    print(f"Max decision time per move:{max_time:.4f} s")

    assert max_time < 3.0


if __name__ == "__main__":
    test_time_per_move()
