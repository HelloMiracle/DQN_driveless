"""
Author: Richard Cai
Description: PySprites module, contains all sprites for Getaway game
Date: 5/29/2015 
"""

#Importing
import pygame,random
screen = pygame.display.set_mode((72, 653))

class player_car(pygame.sprite.Sprite):
    """Player class car"""
    def __init__(self):
        """Parent init method"""
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("Images/car32.gif")
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.top = 600
        self.rect.centerx = 52
        self.uper = 0
        self.lower = 0
        self.__right = 0
        self.__left = 0
        self.__up = 0
        self.__down = 0
        self.speed = 90
        self.road = 2
        self.__colour = False
        self.counter = 0
    
    def move_right(self,value):
        """Move the sprite up"""
        self.__right = value
    
    def move_left(self,value):
        """Move the sprite left"""
        self.__left = -value
        
    def move_up(self,value):
        """Move the sprite right"""
        #self.__up = -value
        self.upper = value
        
    def move_down(self,value):
        """Move the sprite down"""
        #self.__down = value
        self.lower = value
    
    def speed_colour(self,flag):
        """Change car color"""
        self.__colour = flag
        
    def update(self, speed):
        """Moves the car corresponding to pressed buttons, cannot move outside of the screen area"""
        if self.rect.top > 0:
            self.rect.top += self.__up
            
        if self.rect.bottom < screen.get_height():
            self.rect.bottom += self.__down
            
        if self.rect.right < screen.get_width():
            self.rect.right += self.__right
            self.__right = 0
        if self.rect.left > 0:
            self.rect.left += self.__left
            self.__left = 0
        
        if self.__colour:
            self.image = pygame.image.load("Images/speed_car.gif")
        else:
            self.image = pygame.image.load("Images/car32.gif")
            
class road(pygame.sprite.Sprite):
    """Road - Moving background"""
    def __init__(self,screen):
        """Init method"""
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("Images/road_fin.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = 653
        self.upper = 0
        self.__dy = 20

    def update(self, speed):
        """Moves the road at a constant speed and resets it the top rect becomes greater than 0"""
        self.rect.top += round(speed * 0.833)
        
        if self.rect.top >= 0:
            self.rect.bottom = 653
            
        
class road_blocks(pygame.sprite.Sprite):
    """Road blocks, move with the screen"""
    def __init__(self):
        """Sprite Init method"""
        pygame.sprite.Sprite.__init__(self)
        '''
        self.image = pygame.image.load("Images/block.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.rect.top = -40
        self.rect.centerx = 279
        '''
        
    def reset(self):
        """Reset the block at the top of the screen at a random x location"""
        '''
        self.rect.top = -100
        
        #Determine the x location, 3 random choices
        x_random = random.randint(1,3)
                    
        if x_random == 1:
            x_value = 279
        elif x_random == 2:
            x_value = 490
        elif x_random == 3:
            x_value = 40
               
        self.rect.centerx = x_value        
        '''
    def update(self):
        """Moves the road block at the same speed of the screen"""
        self.rect.centery += 12
        
        if self.rect.top > screen.get_height():
            self.reset()
        
class other_cars(pygame.sprite.Sprite):
    """Opposing cars, player must avoid them"""
    def __init__(self):
        self.time = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/op_van.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 51
        self.road = 2 
        self.upper = 0
        self.init_speed = 120
        self.speed = 10*round(random.randint(40,70)/10)
    def car_upper(self, value):
        self.upper -= value
        
    def car_lower(self, value):
        self.upper += value
        
    def reset(self):
        """reset the car at a the top of the screen at a random x value"""
        self.rect.bottom = 0
        self.upper = 0
        x_random = random.randint(1,2)
        self.speed = 10*round(random.randint(40,70)/10)         
        if x_random == 1:
            x_value = 19
            self.road = 1
        elif x_random == 2:
            x_value = 51
            self.road = 2
                    
        self.rect.centerx = x_value        
    
        car_choice = random.randint(0,2)
        if car_choice == 0:
            self.image = pygame.image.load("Images/op_van.gif")
        elif car_choice == 1:
            self.image = pygame.image.load("Images/op_audi.gif")
        elif car_choice == 2:
            self.image = pygame.image.load("Images/op_pickup.gif")
            
    def update(self, speed):
        """Moves the car by updating the y value. Adding values to the self.rect.top. Calls reset if moves out of screen."""
        self.rect.top += round((speed - self.speed) * 0.8333)
        self.time += 1
        if self.time > 1000:
            self.speed -= 10
            self.time = 0
        if self.rect.bottom < -20:
            self.reset()
        if self.rect.top > screen.get_height()+400:
            self.reset()
            
                
class neirong(object):
    def __init__(self):
        self.bian = "kong"
class showbian(pygame.sprite.Sprite):
    """This class defines a label sprite to display the score"""
    def __init__(self, car, height, name):
        '''This initializer loads a new font, and
        sets the default lives and score and tracker'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.neirong = car
        self.height = height
        self.name = name
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("game_font.otf", 25)
        self.__lives = 5
        self.__points = 0
        
        #Keeps track of when to add new obstacles & powerups
        self.__tracker = 0 
        
    def death(self):
        """Takes away a life from the player"""
        self.__lives -= 1
        
    def increase_tracker(self):
        """Increases the meteres every second"""
        self.__tracker += 1

    def increase_points(self,value):
        """Increases the points by the value given"""
        self.__points += value
    
    def increase_lives(self):
        """Increase the life when the health powerup is picked up"""
        self.__lives += 1
        
    def game_over(self):
        """Checks if the player is out of lives, ends the game if true"""
        if self.__lives <= 0:
            return True
        
    def get_points(self):
        """Returns the value of points"""
        return self.__points
    
    def get_tracker(self):
        """Returns the value of tracker"""
        return self.__tracker
    

    def update(self,speed):
        """This method will be called automatically to display 
        the current score at the top of the game window."""
        try:
            score_file = open("score.txt","r")
            self.__high_score = int(score_file.readline())
            score_file.close()
        except IOError:
            self.__high_score = 0
        
        message = "%s:%s" % (self.name,self.neirong.bian)
        
        self.image = self.__font.render(message,1,(237,255,237))
        self.rect = self.image.get_rect()
        self.rect.center = (200,self.height)

class ScoreKeeper(pygame.sprite.Sprite):
    """This class defines a label sprite to display the score"""
    def __init__(self, car, height, name):
        '''This initializer loads a new font, and
        sets the default lives and score and tracker'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.car = car
        self.height = height
        self.name = name
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("game_font.otf", 25)
        self.__lives = 5
        self.__points = 0
        
        #Keeps track of when to add new obstacles & powerups
        self.__tracker = 0 
        
    def death(self):
        """Takes away a life from the player"""
        self.__lives -= 1
        
    def increase_tracker(self):
        """Increases the meteres every second"""
        self.__tracker += 1

    def increase_points(self,value):
        """Increases the points by the value given"""
        self.__points += value
    
    def increase_lives(self):
        """Increase the life when the health powerup is picked up"""
        self.__lives += 1
        
    def game_over(self):
        """Checks if the player is out of lives, ends the game if true"""
        if self.__lives <= 0:
            return True
        
    def get_points(self):
        """Returns the value of points"""
        return self.__points
    
    def get_tracker(self):
        """Returns the value of tracker"""
        return self.__tracker
    

    def update(self,speed):
        """This method will be called automatically to display 
        the current score at the top of the game window."""
        try:
            score_file = open("score.txt","r")
            self.__high_score = int(score_file.readline())
            score_file.close()
        except IOError:
            self.__high_score = 0
        
        message = "%s:%d" % (self.name,self.car.speed)
        
        self.image = self.__font.render(message,1,(237,255,237))
        self.rect = self.image.get_rect()
        self.rect.center = (200,self.height)
        

        
