# ElevatorAI

The project ElevatorAI aims for the goal to train software agents, used for control and coordination of multiple elevators.
This project originates from the lecture Applied Artifical Intelligence taught at the University of Applied Sciences Hochschule Esslingen, which was developed by team No. 3.

## Team No. 3:
 * Alexander Putin
 * Mohamed Karim Ben Dhifallah
 * Max Haussch
 * Oleg Tovarish
 * Firat Susan

## Getting Started
These instruction will briefly explain how to setup the project on a local machine.

### Setup on local machine
Create a directoy for this project and clone it via git
```sh
git clone https://github.com/abelokon955/elevator_ai.git
cd ./elevator_ai
```
Next the required packages have to be installed
```sh
pip install -r requirements.txt
```

### Defining a model
The first thing to do is the definition of a model.
There are two options available:
 * Creating a new model on startup
 * Loading an exisiting model

#### Defining a new model
When the training is initiated and no paramters are specified for the main.py script, a new model will be automatically generated according to the build_model function inside main.py.
```py
def build_model(input_size, output_size):
    model = ...Keras Model...
    model.add(...)
    ...
    model.add(...)
    model.compile(...)
    return model
```
For a custom definition just change this section of code to your desires.

### Using an existing model
To use an exisiting model you need to provide the model inside a seperate direcotry in `.\models\<model_name>\`. There the model defintion has to be contained inside a file named `model.json`, which should be loadable by keras. The weights need to be provided aswell, as a file named `model_weights.h5`.

When starting execution of the main.py you have to provided via arguments the `<model_name>` as shown.
```sh
python main.py <model_name> <True|False>
```
Additionaly you have to provide an argument if you want to train this model.

# Settings
In order to setup the environment for your needs, you have to take a at some specific values.

In gym_environment.py:
```py
class ElevatorEnv(gym.Env):
    def __init__(self):
        self.elevator_num = # Number of elevators in the environment
        self.elevator_limit = # Capacity for each elevator
        self.floor_num = # Number of floors in the environment
        self.floor_limit = # Capacity for each floor
        self.waiting_passangers = # Waiting passengers in environnment
```

In main.py:
```py
episoden = # Number of episodes for training
schritte = # Number of maximums steps in each episode
zustandvektor_laenge = # Length of the state vector
aktionvektor_laenge = # Length of the action vector
```

# Viewing result
The main.py scripts stores the latest 100 episodes inside the `\results\` folder. In that will be a folder named after the execution id. For each execution there will be an execution id generated from the hash of the time of exeuction.
Using the simulator.py you can render a series of the last 100 episodes and watch the agent interact with the environment.
```sh
python simulator.py <execution id> <startEpisode> --speed <speed> --end_episode <lastEpisode>
```
Note: The --speed requires an floating point value greater 0.
