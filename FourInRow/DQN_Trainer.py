from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Env import Env
from ReplayBuffer import ReplayBuffer
from State import State
import torch 

epochs = 100000
C = 500
batch = 64
learning_rate = 0.1
path = "Data\DQN_PARAM_100K.pth"

def main ():
    env = Env()
    player1 = DQN_Agent(1, env=env)
    player2 = Random_Agent(2, env=env)
    replay = ReplayBuffer()
    Q = player1.DQN
    Q_hat :DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.SGD(Q.parameters(), lr=learning_rate)
       
    for epoch in range(epochs):
        print (epoch, end="\r")
        state = State()
        while not env.end_of_game(state):
            action = player1.get_action(state, epoch=epoch)
            after_state, reward = env.next_state(state, action)
            if env.end_of_game(after_state):
                replay.push(state, action, reward, after_state, env.end_of_game(after_state))
                break
            after_action = player2.get_action_state(state=after_state)
            next_state, reward = env.next_state(after_state, after_action)
            replay.push(state, action, reward, next_state, env.end_of_game(next_state))
            state = next_state

        if epoch < batch:
            continue
        states, actions, rewards, next_states, dones = replay.sample(batch)
        Q_values = Q(states, actions)
        next_actions = player1.get_actions(next_states, dones)
        next_actions = next_actions.reshape(-1,1)
        with torch.no_grad():
            Q_hat_Values = Q_hat(next_states, next_actions)
        
        loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
        loss.backward()
        optim.step()
        optim.zero_grad()
        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())
            

    player1.save_param(path)

if __name__ == '__main__':
    main()