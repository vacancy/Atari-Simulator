# Atari-Simulator
Atari simulator using python lib `gym`

## Requirements
Due to the dependency opencv, the program is developed under PYTHON2.

This package depends on the following packages:
- gym
- gym[atari]
- opencv2
- numpy
- PIL
- PIL.ImageTk

## Usage
First, create your cfg file via:

`python2 gen_cfg.py cfg/<some_file_name>.py <game_name>`

where `<game_name>` is the game's name in OpenAI's Gym. (e.g. Enduro-v0)

In this step, you need to follow the instructions and create the key mapping for your game.
E.g. when the program asks you to input a key for 'DOWN' action, you may probabily press '<DOWN>' bottun on your keyboard.

A tricky thing is that after mapping all game-related actions, you need to map a special action 'quit', which can be used to stop the game while playing.

Now it's time to play the game. Use:

`python2 main.py cfg/<some_file_name>.py --fps <fps>`

Note at any time you can use 'quit' action to quit your play. After you press the 'quit' button or when the game normally ends, a replay pickle will placed in the replay folder.

One tricky thing is that you can adjust the fps for the game if you want to play it in a slower mode.

## Dumped replays
The replay file can be loaded by module `pickle` without any dependency (oh, `numpy` is needed). The only tricky thing in the replay file is that for easier usage, the observation in each 'step' actually refer to the last observation. That is, for a dict in `replay['steps']`, `action` (and `reward`) is the `action` (and `reward`) human expert plays after seeing `observation`.
