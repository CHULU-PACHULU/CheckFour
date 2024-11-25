from Env import Env
from State import State
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent

PATH = "Data\DQN_PARAM_100K.pth"
# PATH=None
env = Env(State())
player1 = DQN_Agent(1, env=env, parametes_path=PATH, train=False)
# player1 = Random_Agent(1, env,graphics=None)
player2 = Random_Agent(2, env)
num = 1000

def main ():

    red_win = 0
    yellow_win = 0
    tie = 0
        
    for n in range(num):
        state = State()
        player = player1
        while not env.end_of_game(state):
            action = player.get_action(state=state)
            state, _ = env.next_state(state,action)
            player = switch_players(player)
        if state.end_of_game == 1:
            red_win +=1
        elif state.end_of_game == -1:
            yellow_win += 1
        else:
            tie +=1
        state.reset()    
        print(n, end = "\r")
    print()
    print(red_win, yellow_win, tie) 

def switch_players(player):
    if player == player1:
        return player2
    else:
        return player1

if __name__ == '__main__':
    main()