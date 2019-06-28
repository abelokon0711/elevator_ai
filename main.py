import gym
import numpy
import random
import os, sys
import atexit
import time
import random
import queue
import statistics
import json

from gym.envs.registration import registry, register, make, spec

from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM, Embedding
from keras.optimizers import SGD, Adam


def build_model(input_size, output_size):
    model = Sequential()
    # model.add(Dense(128, input_dim=input_size, activation='relu',
    #                 kernel_initializer='random_uniform', bias_initializer='zeros'))
    # model.add(Dense(52, activation='relu',
    #                 kernel_initializer='random_uniform', bias_initializer='zeros'))
    # model.add(Dense(output_size, activation='sigmoid',
    #                 kernel_initializer='random_uniform', bias_initializer='zeros'))
    # model.compile(loss='mse', optimizer=Adam(lr=0.1, beta_1=0.9,
    #                                          beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False))
    model.add(Dense(128, input_dim=input_size, activation='relu',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(64, activation='relu',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(64, activation='relu',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))
    #model.add(LSTM(1))
    model.add(Dense(output_size, activation='softmax',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.01))#Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False))
    return model

def load_model_and_weights(name):
    path = "models\\" + name
    model_path = path + "\\model.json"
    architecture = None
    with open(model_path, 'r') as json_file:
        architecture = json.load(json_file)
    model = model_from_json(json.dumps(architecture))

    weight_path = path+'\\model_weights.h5'
    model.load_weights(weight_path)
    model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.1))
    return model

# https://machinelearningmastery.com/save-load-keras-deep-learning-models/


# id damit wird episoden und model unterscheiden können nach ausführung des skripts
execution_id = hash(time.time())

def exit_handler():
    # save model and weights
    print('Saving model...')

    if not os.path.isdir("results/"):
        os.mkdir("results/")

    if not os.path.isdir("models/"):
        os.mkdir("models/")

    model_json = neural_network.to_json()
    os.mkdir("models/"+str(execution_id))
    with open("models/" + str(execution_id) + "/model.json", "w") as json_file:
        json_file.write(model_json)
    neural_network.save_weights(
        "models/" + str(execution_id) + "/model_weights.h5")

    # Write observationz to file
    print("Saving episodes")

    os.mkdir("results/"+str(execution_id))
    for i in range(aufzeichnungen):
        numpy.savetxt('results/'+str(execution_id)+'/observations_episode_' + str(i) +
                      '.txt', observationz[i], delimiter=',')
        numpy.savetxt('results/'+str(execution_id)+'/actions_episode_' + str(i) +
        '.txt', actionz[i], delimiter=',')
        numpy.savetxt('results/'+str(execution_id)+'/rewards_episode_' + str(i) +
                      '.txt', rewardz[i], delimiter=',')


atexit.register(exit_handler)


register(
    id='Elevator-v0',
    entry_point='gym_environment:ElevatorEnv',
)

episoden = 1000000
schritte = 20
zustandvektor_laenge = 72
aktionvektor_laenge = 3**2


# Training the model
env = gym.make('Elevator-v0')

neural_network = None
train = True
if len(sys.argv) == 1:
    neural_network = build_model(zustandvektor_laenge, aktionvektor_laenge)
else:
    neural_network = load_model_and_weights(sys.argv[1])
    train = (sys.argv[2] == 'True')


aufzeichnungen = 100
start_recording_at = episoden - aufzeichnungen
observationz = numpy.zeros((aufzeichnungen, schritte, zustandvektor_laenge))
actionz = numpy.zeros((aufzeichnungen, schritte, 1))
rewardz = numpy.zeros((aufzeichnungen, schritte, aktionvektor_laenge))

replay_buffer_X = []
replay_buffer_y = []

last_episode = -1
high_score = -100000

movingAverage = queue.Queue(maxsize=1000)

for i_episode in range(episoden):
    observation = env.reset()
    # reinit random
    random.seed()

    memories = []
    sum_reward = 0
    steps = 0

    while True:
        if i_episode >= start_recording_at:
            observationz[i_episode - start_recording_at][steps] = numpy.copy(observation)
        
        prediction = neural_network.predict(observation.reshape(-1, len(observation)))[0]
        
        rewards = [0]*aktionvektor_laenge
        for i in range(aktionvektor_laenge):
            rewards[i] = env.eval(i)[1]
        
        # Memorize actual rewards training
        best_predicted_action = rewards.index(max(rewards))
        best_output = [0]*aktionvektor_laenge
        best_output[best_predicted_action] = 1
        #memories.append([observation, best_output])

        action = numpy.argmax(prediction)
        # Random change of data
        if random.random() < 0.1:
           action = random.randint(0,aktionvektor_laenge-1)

        #print(action, observation[0], best_predicted_action)
        observation, reward, done, info = env.step(action)

        #if reward > 0:
        memories.append([observation, best_output])
            #neural_network.fit([[observation]], [[best_output]], verbose=0)

        sum_reward += reward
        # print(observation[0])
        # Record current action
        if i_episode >= start_recording_at:
            actionz[i_episode - start_recording_at][steps] = action
            rewardz[i_episode - start_recording_at][steps] = rewards
            

        if done or sum_reward < -1000 or steps ==20:
            #print("Episode finished after {} timesteps".format(steps))
            break
        else:
            steps += 1

    # if movingAverage.full():
    #     movingAverage.get()
    # movingAverage.put(sum_reward)
    high_score = max([high_score, sum_reward])

    # Adjust network after steps
    X = list()
    y = list()
    # for i in range(len(memories)):
    #     X.append(memories[i][0])
    #     y.append(memories[i][1])

    for i in range(len(memories)):
        X.append(numpy.array(memories[i][0]))
        y.append(numpy.array(memories[i][1]))

    # for i in range(zustandvektor_laenge):
    #     state_i = numpy.zeros(len(memories))
    #     for j in range(len(memories)):
    #         state_i[j]= memories[j][0][i]
    #     X.append(state_i)
    # for i in range(aktionvektor_laenge):
    #     action_i = numpy.zeros(len(memories))
    #     for j in range(len(memories)):
    #         state_i[j]= memories[j][1][i]
    #     y.append(state_i)
    # for i in range(len(memories)):
    #     print(X[0][i])
    
    # if i_episode == 0:
    #     for i in range(len(memories)):
    #         replay_buffer_X.append(memories[i][0])
    #         replay_buffer_y.append(memories[i][1])
    # else:
    #     for i in range(len(memories)):
    #         if random.random() > 0.5:
    #             j = random.randint(0,len(replay_buffer_X)-1)
    #             replay_buffer_X[j] = memories[i][0]
    #             replay_buffer_y[j] = memories[i][1]
    #         elif random.random() < 0.1:
    #             replay_buffer_X.append(memories[i][0])
    #             replay_buffer_y.append(memories[i][1])
    if sum_reward >= -1000 or i_episode%100==0:
        print("Highscore: ",high_score,"|   Sum of Rewards at Episode", i_episode, ':', sum_reward)#, "   |  Moving Average:", statistics.mean(list(movingAverage.queue)))
    # Train model
    neural_network.fit([X], [y], verbose=0)  # ,epochs=10, batch_size=1)
    last_episode += 1
    #neural_network.fit([replay_buffer_X], [replay_buffer_y], verbose=0)  # ,epochs=10, batch_size=1)
env.close()



    # for t in range(schritte):
    #     # env.render()
    #     if i_episode >= start_recording_at:
    #         observationz[i_episode -
    #                      start_recording_at][t] = numpy.copy(observation)

    #     # Predict the rewards for each action
    #     prediction = neural_network.predict(
    #         observation.reshape(-1, len(observation)))[0]

    #     # Calculate the actual rewards
    #     rewards = [0]*aktionvektor_laenge
    #     for i in range(aktionvektor_laenge):
    #         rewards[i] = env.eval(i)[1]

    #     # Memorize actual rewards training
    #     best_predicted_action = rewards.index(max(rewards))
    #     best_output = [0]*aktionvektor_laenge
    #     best_output[best_predicted_action] = 1
    #     memories.append([observation, best_output])

    #     # print("Actions:")
    #     # for i in range(aktionvektor_laenge):
    #     #     print(i, "ith probability of ", prediction[i])

    #     # if i_episode == 99:
    #     #     print(rewards)
    #     #     print(prediction)
    #     #     print(best_output)

    #     action = numpy.argmax(prediction)
    #     #if random.random() < 0.1:
    #     #    action = random.randint(0,2)
    #     # print(action, observation[0], best_action)
    #     # action = env.action_space.sample()
    #     observation, reward, done, info = env.step(action)

    #     sum_reward += reward
    #     # print(observation[0])
    #     # Record current action
    #     if i_episode >= start_recording_at:
    #         actionz[i_episode - start_recording_at][t] = action
    #         rewardz[i_episode - start_recording_at][t] = rewards
    #     #print("Prediciton for best Action", prediction,"but should be", best_output,"and actual rewards for actions", rewards)
            

    #     if done:# or reward > -90000:
    #         #print("Episode finished after {} timesteps".format(t))
    #         break