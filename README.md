# Python Roguelike Framework [![Build Status](https://travis-ci.org/jpalladino84/Python-Roguelike-Framework.svg?branch=master)](https://travis-ci.org/jpalladino84/Python-Roguelike-Framework) [![Documentation Status](https://readthedocs.org/projects/python-roguelike-framework/badge/?version=latest)](http://python-roguelike-framework.readthedocs.io/en/latest/?badge=latest)
### >>>>> WARNING This is a Alpha release. WARNING <<<<<
#### Version: 2.0.0a

Online Documentation:
http://python-roguelike-framework.readthedocs.io/en/latest/

## Description
A Python framework for developing Roguelikes.
It is built using the TDL library which is a port of the c/c++ libtcod library.
- TDL documentation: http://pythonhosted.org/tdl/
- libtcod documentation: http://doryen.eptalys.net/data/libtcod/doc/1.5.1/index2.html

## Installation
#### Git
```
git clone https://github.com/jpalladino84/roguelike-game.git

cd roguelike-game

pip install -r requirements.txt
```



## Running
The framework starts with 5 levels for you to play around with. Run the game with:

`python2.7 run.py`

## Configure
The true power of this framework is the ability to configure the game to your liking.
Each module has a `config.py` file where various settings can be modified to craft a unique experience.


## Contributing
Contributions are welcomed!

Keep in mind when contributing that the goal of this framework is that it should be easy to
use and configure for newcomers, but also powerful for advanced users.
- Any new features added should be made available to configure through a `config.py`
- Features should be well documented

## Further Reading
There is some boiler plate code from the Roguebasin's libtcod tutorial which I had to adapt to fit with the TDL library.
- tutorial link: http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

Good read on dungeon generation: http://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
