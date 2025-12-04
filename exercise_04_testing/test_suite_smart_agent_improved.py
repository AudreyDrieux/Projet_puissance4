import time
import tracemalloc
import numpy as np
from pettingzoo.classic import connect_four_v3
from loguru import logger
from random_agent_copy2 import RandomAgent
from smart_agent_improved import SmartAgent

def to_board(matrix, channel=0):
    board = np.zeros((6,7,2))
    for r in range(6):
        for c in range(7):
            if matrix[r][c] == 1:
                board[r,c,channel] = 1
    return board

#### Tests fonctionnels ####

# Sélection de coup valide
def test_valid_move():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    agent = SmartAgent(env)

    matrix = [
        [1,1,1,0,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
    ]
    observation = to_board(matrix, channel=0)
    action_mask = np.array([0, 0, 0, 1, 0, 0, 0], dtype=int)
    assert agent.choose_action(observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=action_mask) == 3

# Respect du masque d'action
def test_respect_action_mask():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    agent = SmartAgent(env)

    matrix = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    observation = to_board(matrix, channel=0)
    action_mask = np.array([1, 0, 0, 0, 0, 0, 1], dtype=int)
    col = agent.choose_action(observation=observation,reward=0.0,terminated=False,truncated=False,info=None,action_mask=action_mask)
    assert action_mask[col] == 1
    assert col in (0, 6)

# Gestion de la fin de partie
def test_handles_terminated_game():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    agent = SmartAgent(env)

    matrix = [
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],
    ]
    observation = to_board(matrix, channel=0)
    action_mask = np.ones(7, dtype=int)

    action = agent.choose_action(
        observation=observation,
        reward=1.0,
        terminated=True,
        truncated=False,
        info={"reason": "game_over"},
        action_mask=action_mask,
    )

    assert action is None

#### Tests de performance ####

# Temps par coup
def test_time_per_move():
    env = connect_four_v3.env()
    env.reset()
    agent = SmartAgent(env)

    board = np.zeros((6,7,2), dtype=int) # 空棋盘
    start = time.time()
    for _ in range(200):      # 调用 200 次
        agent.choose_action(board,reward=0.0,terminated=False,truncated=False,info=None,action_mask=np.ones(7, dtype=int))
    end = time.time()
    avg = (end - start) / 200
    print("Average time:", avg)
    assert avg < 0.02

# Utilisation de la mémoire  
def test_memory():
    env = connect_four_v3.env()
    env.reset()
    agent = SmartAgent(env)

    board = np.zeros((6,7,2), dtype=int)
    tracemalloc.start()
    for _ in range(200):
        agent.choose_action(board,reward=0.0,terminated=False,truncated=False,info=None,action_mask=np.ones(7, dtype=int))
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("Peak memory:", peak)
    assert peak < 10 * 1024 * 1024 # 10MB(1 MB = 1024 KB = 1024 × 1024 bytes = 1,048,576 bytes)





if __name__ == "__main__":
    test_valid_move()

if __name__ == "__main__":
    test_respect_action_mask()

if __name__ == "__main__":
    test_handles_terminated_game()

if __name__ == "__main__":
    test_time_per_move()

if __name__ == "__main__":
    test_memory()