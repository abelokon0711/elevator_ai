import gym
import numpy
import random
import os
import atexit
import time

from gym.envs.registration import registry, register, make, spec

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


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
    model.add(Dense(64, input_dim=input_size, activation='relu',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(64, activation='relu',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))

    model.add(Dense(output_size, activation='sigmoid',
                    kernel_initializer='random_uniform', bias_initializer='zeros'))

    model.compile(loss='mse', optimizer=Adam(lr=0.0001, beta_1=0.9,
                                             beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False))
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


atexit.register(exit_handler)


register(
    id='Elevator-v0',
    entry_point='gym_environment:ElevatorEnv',
)

episoden = 100
schritte = 200
zustandvektor_laenge = 61
aktionvektor_laenge = 3


# Training the model
env = gym.make('Elevator-v0')

neural_network = build_model(zustandvektor_laenge, aktionvektor_laenge)

aufzeichnungen = 100
start_recording_at = episoden - aufzeichnungen
observationz = numpy.zeros((aufzeichnungen, schritte, zustandvektor_laenge))


for i_episode in range(episoden):
    observation = env.reset()

    memories = []
    sum_reward = 0

    for t in range(schritte):
        # env.render()
        if i_episode >= start_recording_at:
            observationz[i_episode -
                         start_recording_at][t] = numpy.copy(observation)

        # print(action)

        prediction = neural_network.predict(
            observation.reshape(-1, len(observation)))[0]

        # Action mit höchtstem reward finden
        rewards = [0, 0, 0]
        for i in range(aktionvektor_laenge):
            rewards[i] = env.eval(i)[1]

        # Beste Aktion speichern fürs training
        best_action = rewards.index(max(rewards))
        best_output = [0, 0, 0]
        best_output[best_action] = 1
        memories.append([observation, best_output])

        # print("Actions:")
        # print("1 with probability of ", prediction[0])
        # print("2 with probability of ", prediction[1])
        # print("3 with probability of ", prediction[2])
        # if i_episode == 99:
        #     print(rewards)
        #     print(prediction)
        #     print(best_output)
        action = numpy.argmax(prediction)
        # print(action, observation[0], best_action)
        # action = env.action_space.sample()
        observation, reward, done, info = env.step(action)

        sum_reward += reward
        # print(observation[0])

        if done or reward == -1000000:
            #print("Episode finished after {} timesteps".format(t))
            break
    # Adjust network after training

    X = []
    y = []
    for i in range(len(memories)):
        X.append(memories[i][0])
        y.append(memories[i][1])
    if sum_reward >= -1000:
        print("Sum of Rewards at Episode ", i_episode, ': ', sum_reward)
    # Train model
    neural_network.fit([X], [y], verbose=0)  # ,epochs=10, batch_size=1)
env.close()
