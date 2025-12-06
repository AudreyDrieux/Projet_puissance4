# Test minimax vs smart agent
from tournament_smart_agent_improved import run_tournament
from smart_agent_improved import SmartAgent
from minimax_agent import MinimaxAgent

agents = [SmartAgent, MinimaxAgent]
A = agents[0]
B = agents[1]

print(f"\nGame 1: A is first")
results1 = run_tournament([A,B], num_games=10)
print(results1)
print(f"\nGame 2: B is first")
results2 = run_tournament([B,A], num_games=10)
print(results2)