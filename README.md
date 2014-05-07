# Mockingjay

This project is a fork of a class project that I and some group members, listed below, made for the final assignment of
Georgia Tech's Game AI course. The purpose of this project is to create an interactive simulation of The Hunger Games,
a fight to the death of various "tributes" detailed in Suzanne Collins' eponymous novel. One of the hopes of this
project is to create an AI system that consistently produces interesting and sometimes surprising results. As of now,
there is a lot to do.

## Contributors
- Whitney Henderson
- Nathan Korzekwa
- Nathan Eppinger

## Libraries and Platforms
- Python 2.7.6
- Pygame
- PIL (or Pillow)


## Running
```
python main.py
```

## Controls
- Click on Tributes on Map to read their stats (a little slow, so give it a moment)
- OR Click on their name in the bottom left (admittedly, this function is a little buggy
- Press q to pause game
- Press q to unpause game
- Press w to give the currently selected tribute a weapon
- Press f to give the currently selected tribute some food
- Press d to give the currently selected tribute some water/a drink

## Changing Maps
- Look at the maps in the map file and pick one.
- Open engine.py
- Change line 79 to the appropriate map file
- TADA!

## Endgame
When you get down to the last tribute, the winner will be announced at the bottom of the screen.