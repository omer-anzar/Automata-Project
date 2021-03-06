# Automata-Project
> - By **Muhammad Umar Anzar**
> - Seat No. **B19102104**
> - University Of Karachi 
> - UBIT department of computer science
> - Semester 5
> - Subject Computer Theory (Automata)

## Finite ball

A basic two-player 2D soccer game created in Python with the Pygame framework. 

## Purpose

The goal was to include a finite state machine in a project.

## Overall Description

- Language: python3
- Library: pygame
- requirements to play : Two user and only one keyboard

## Features, Functions

1. Python `pygame` is used to make the entire GUI game, and `auto-py-to-exe` is used to make the executable file.

2. The player's entire movement is controlled by a finite state machine (Deterministic Finite Automata). To handle the movement `key release ` and `key pressed` events, a new condition and additional `set array` are introduced. When a user presses numerous keys and only one or two of them are released, the unique condition causes the transition to return to the initial state and utilizing the set array, the keys that haven’t been released yet cause the transition to new states following the keys that are already pressed.<img src='Finite States\finite_states_diagram.png' alt="DFA of motion" width=75%>

```py
self.TransitionsTable = [
            [1,2,3,4,5],    #initial    0
            [1,1,3,4,5],    #right      1
            [2,2,3,4,5],    #left       2
            [1,2,3,3,5],    #up         3
            [1,2,4,4,5],    #down       4
            [1,2,3,4,5]     #sprint     5
        ]  
```
3. The concept of Inheritance is used a little. <img src="Finite States\uml_diagram.png" alt="uml diagram" width="75%">

4. Controlled the increase in diagonal speed as a result of the horizontal and vertical motions. <img src='Finite States\diagonal_speed.png' alt='diagonal speed' width=75%>

5. In-Elastic Collisions physics is applied with true angles between the user and the ball, as well as between the ball and the window boundaries. <img src='Finite States\collisionBallHit.png' alt='collision' width=75%>


## Game Screenshots
<img src='game screen shot\a.jpg' alt="game screenshot" width=75%>
<img src='game screen shot\b.jpg' alt="game screenshot" width=75%>
<img src='game screen shot\c.jpg' alt="game screenshot" width=75%>


