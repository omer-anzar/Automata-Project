from window_functions import *
from decimal import DivisionByZero
import pygame
import time
import math

class MovableObject:

    def __init__(self,window:Window,x,y,fps,radius,color) -> None:
        #REFERENCE WINDOW OBJECT
        self.window = window

        #COORDINATES,RADIUS,COLOR,FRAME PER SECOND
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.fps = fps

        # DIRECTION FACTORS
        self.horizontal_factor = 0
        self.vertical_factor = 0



class User(MovableObject):

    def __init__(self,window,x,y,fps,radius,color) -> None:
        #CALLING OBJECT CONSTRUCTOR
        super().__init__(window,x,y,fps,radius,color)

        #SPRINT
        self.sprint_time_on = 0
        self.sprint_time_off = 0
        self.sprint_time_delay = 3
        self.sprint_time_duration = 0.3
        self.sprint_factor = 3


        #DOMAIN OF KEYS ACCEPTED
        self.domain = { }

        #SET OF KEY which are pressed and haven't release
        self.pressed = set([])

        # INITIAL AND CURRENT STATE
        self.current = 0

        # FUNCTIONS OF EACH STATE
        self.statesFunctionArr = [self.S0,self.S1,self.S2,self.S3,self.S4,self.S5]

        # TRANSITION TABLE DFA of User actions
        self.TransitionsTable = [
            [1,2,3,4,5],    #initial    0
            [1,1,3,4,5],    #right      1
            [2,2,3,4,5],    #left       2
            [1,2,3,3,5],    #up         3
            [1,2,4,4,5],    #down       4
            [1,2,3,4,5]     #sprint     5
        ]

        self.init()



    #DRAW USER ON WINDOW
    def init(self):
        pygame.draw.circle(self.window.screen,pygame.Color(self.color),(self.x,self.y),self.radius)
        pygame.draw.circle(self.window.screen,pygame.Color(self.color),(self.x,self.y),self.radius+4,width=2)


    #STOPS USER FROM CROSSING BOUNDARY
    def user_boundary(self,x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        if self.x < x_lower_bound:
            self.x = x_lower_bound + 1
        elif self.x > x_upper_bound:
            self.x = x_upper_bound - 1
        elif self.y < y_lower_bound:
            self.y = y_lower_bound
        elif self.y > y_upper_bound:
            self.y = y_upper_bound


    #TRANSTITION FROM ONE STATE TO ANOTHER ON KEY PRESS AND RELEASE
    def transition(self,event):
            # if event is pressed or release key
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                
                try:
                    index = self.domain[event.key]
                    key = event.key


                    
                    if event.type == pygame.KEYUP:
                        #if key is release
                        try:
                            #remove the key from set which is release and comes to initial state
                            self.pressed.remove(key)
                            self.current = 0
                            self.statesFunctionArr[self.current]()

                            #Then transition to those states which are presently pressed 
                            for action in self.pressed:
                                self.current = self.TransitionsTable[self.current][self.domain[action]]
                                self.statesFunctionArr[self.current]()

                        except KeyError as e:
                            pass

                    else:
                        #if key is pressed

                        #add presently pressed keys in set() and do transition
                        self.pressed.add(key)
                        self.current = self.TransitionsTable[self.current][index]
    
                    #Run the function accordingly to the current state
                    self.statesFunctionArr[self.current]()

                except Exception as e:
                    #return if keys other than action keys
                    pass
            
            else:
                return


    #APPLY MOVING MOTION
    def move(self):

        #HANDLE DIAGONAL SPEED (SAME AS ONLY X OR Y AXIS SPEED)
        if abs(self.horizontal_factor) == 1 and abs(self.vertical_factor) == 1:
            fps = ( (self.fps**2) /2)**(1/2)
        else:
            fps = self.fps

        #FOR SPRINTING WITH DURATION
        if abs(self.sprint_time_on - time.time()) < self.sprint_time_duration:
            fps = fps * self.sprint_factor

        self.x += self.horizontal_factor * fps
        self.y += self.vertical_factor * fps


    #PAUSE(INITIAL)
    def S0(self):
        self.horizontal_factor,self.vertical_factor = 0,0
    #RIGHT
    def S1(self):
        self.horizontal_factor = 1
    #LEFT
    def S2(self):
        self.horizontal_factor= -1
    #UP
    def S3(self):
        self.vertical_factor = -1
    #DOWN
    def S4(self):
        self.vertical_factor = 1
    #SPRINT
    def S5(self):
        #RUNS WHEN TIME IS MORE THAN SPRINT DELAY TIME
        if abs(self.sprint_time_off - time.time()) > self.sprint_time_delay :
            self.sprint_time_off = time.time()
            self.sprint_time_on = self.sprint_time_off

class Player(User):

    def __init__(self,window,x,y,fps,radius,color,domain):
        #CALLING USER CONSTRUCTOR
        super().__init__(window,x,y,fps,radius,color)

        #TO RESPAWN
        self.spawn_location = (x,y)

        
        self.domain = domain
        # DOMAIN OF KEYS ACCEPTED
        #self.domain = { }
                        # K_RIGHT:0,
                        # K_LEFT:1,
                        # K_UP:2,
                        # K_DOWN:3,
                        # K_SPACE:4}
    
    def respawn(self):
        self.x, self.y = self.spawn_location
        self.init()


class Ball(MovableObject):

    def __init__(self,window,x,y,fps,radius,color) -> None:
        #CALLING OBJECT CONSTRUCTOR
        super().__init__(window,x,y,fps,radius,color)

                
        #ON HIT
        try:
            with open("onHitSpeed.txt",'r') as file:
                self.onHitspeed = int(eval(file.read()))
        except Exception:
            self.onHitspeed = 2
        print("On hit speed set to: ",self.onHitspeed)

        
        self.init()


    #DRAW BALL ON WINDOW
    def init(self):
        pygame.draw.circle(self.window.screen, pygame.Color(self.color), (self.x,self.y), self.radius)

    #movement of ball
    def move(self):

        if self.fps > 0:
            self.fps = self.fps - 0.1
        if self.fps <= 0:
            self.fps = 0
            self.horizontal_factor = 0
            self.vertical_factor = 0


        fps = self.fps
        self.x += self.horizontal_factor * fps
        self.y += self.vertical_factor * fps



    #Window Boundary reflection
    def ball_boundary(self,x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        if self.x < x_lower_bound or  self.x > x_upper_bound:
            self.horizontal_factor = self.horizontal_factor * -1

        if self.y < y_lower_bound or self.y > y_upper_bound:
            self.vertical_factor = self.vertical_factor * -1

    def bring_in_center(self):
        self.x = self.window.screen.get_width() // 2
        self.y = self.window.screen.get_height() // 2
        self.fps = 0

    def out_of_boundary(self,x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        if (self.x < x_lower_bound - self.radius or  
            self.x > x_upper_bound + self.radius or 
            self.y < y_lower_bound - self.radius or 
            self.y > y_upper_bound + self.radius):

            self.bring_in_center()

    #WHEN PLAYER HITS THE BALL
    def on_hit(self,player:Player):
        player_x_bound = player.x
        player_y_bound = player.y
        ball_x_bound = self.x
        ball_y_bound = self.y
        distance = math.sqrt( ( (player_x_bound - ball_x_bound)**2 + (player_y_bound - ball_y_bound)**2 ) )

        #if ball is near the player
        if distance > 0 and distance < self.radius + player.radius:

            # if player isn't moving
            if player.horizontal_factor == 0 and player.vertical_factor == 0:
                if self.vertical_factor == 0:
                    self.horizontal_factor *= -1
                else:
                    self.vertical_factor *= -1


            else:

                try:
                    '''
                        gradient converts into degree of 0-90
                        degree is then normalize 0-1
                        due to absoulute value of gradient we need to handle the negative side movment of the ball
                    '''
                    gradient = abs( (self.y - player.y) / (self.x - player.x) )
                    normalize_degree = math.degrees(math.atan( gradient ) / 90) 

                except DivisionByZero as e:
                    # if gradient is infinity
                    normalize_degree = 1
                

                '''
                    y componenet is set to normalize degree
                    x componenet is set to 1-normalize degree 
                '''
                self.horizontal_factor = (1 - normalize_degree) #* player.horizontal_factor
                self.vertical_factor = normalize_degree #* player.vertical_factor

                '''
                    if player is coming from right or top to the ball then movment of ball is reverse
                '''
                if player.x > self.x:
                    self.horizontal_factor *= -1
                if player.y > self.y:
                    self.vertical_factor *= -1



            self.fps = player.fps * self.onHitspeed

        







'''
        self.TransitionsTable = [
            [[(K_RIGHT,0),(K_LEFT,0),(K_UP,0),(K_DOWN,0),(K_SPACE,0)],  [(K_RIGHT,1),   (K_LEFT,2), (K_UP,3),   (K_DOWN,4), (K_SPACE,5)]],
            [[(K_RIGHT,0),(K_UP,0),(K_DOWN,0)],                         [(K_RIGHT,1),   (K_UP,3),   (K_DOWN,4), (K_SPACE,5)]],
            [[(K_LEFT,0),(K_UP,0),(K_DOWN,0)],                          [(K_LEFT,2),    (K_UP,3),   (K_DOWN,4), (K_SPACE,5)]],
            [[(K_UP,0),(K_RIGHT,0),(K_LEFT,0)],                         [(K_UP,3),      (K_LEFT,2), (K_RIGHT,1),(K_SPACE,5)]],
            [[(K_DOWN,0),(K_RIGHT,0),(K_LEFT,0)],                       [(K_DOWN,4),    (K_LEFT,2), (K_RIGHT,1),(K_SPACE,5)]],
            [[],[]]
        ]

        self.domain = [K_RIGHT,K_LEFT,K_UP,K_DOWN,K_SPACE]
        self.TransitionTable = [
            [(K_RIGHT,1),   (K_LEFT,2), (K_UP,3),   (K_DOWN,4), (K_SPACE,5)],
            [(K_RIGHT,1),   (K_UP,3),   (K_DOWN,4), (K_SPACE,5)],
            [(K_LEFT,2),    (K_UP,3),   (K_DOWN,4), (K_SPACE,5)],
            [(K_UP,3),      (K_LEFT,2), (K_RIGHT,1),(K_SPACE,5)],
            [(K_DOWN,4),    (K_LEFT,2), (K_RIGHT,1),(K_SPACE,5)],
            [(K_SPACE,5)]
        ]
        
        
        def transition(self,event):
            # if event is pressed or release key
            if event.type == KEYUP or event.type == KEYDOWN:
                key = event.key

                #if key is release
                if event.type == KEYUP:
                    if key in self.domain:
                        try:
                            self.pressed.remove(key)
                            self.current = 0
                            self.statesFunctionArr[self.current]()
                            for action in self.pressed:
                                for connection in self.TransitionTable[self.current]:
                                    if action == connection[0]:
                                        self.current = connection[1]
                                        self.statesFunctionArr[self.current]()
                        except:
                            pass
                else:
                    #if key is pressed
                    for connection in self.TransitionTable[self.current]:
                        if key == connection[0]:
                            self.current = connection[1]
                            self.pressed.add(key)
                            break
                
                self.statesFunctionArr[self.current]()
            
            else:
                pass

        def user_boundary(self,x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
            if self.x < x_lower_bound or self.x > x_upper_bound:
                self.horizontal_factor = 0
            if self.y < y_lower_bound or self.y > y_upper_bound:
                self.vertical_factor = 0
            
        '''


'''
    def on_hit(self,player:Player):
        player_x_bound = player.x
        player_y_bound = player.y
        ball_x_bound = self.x
        ball_y_bound = self.y
        distance = math.sqrt( ( (player_x_bound - ball_x_bound)**2 + (player_y_bound - ball_y_bound)**2 ) )

        
        if distance > 0 and distance < self.radius+player.radius:
            self.horizontal_factor = player.horizontal_factor
            self.vertical_factor = player.vertical_factor
            self.fps = player.fps * 2
'''
