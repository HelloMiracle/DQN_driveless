"""
Author: Richard Cai
Description: Getaway (summative game)
Date: 5/29/2015

       Versions:
       V1.0 - Moving car sprite
       
       v1.1 - Infinite road background
       
       v1.2 - Road block obstacles, moving at the same speed as the road
       
       v1.3 - Incoming cars
       
       v1.4 - Unit collision 
       
       v1.5 - ScoreKeeper
       
       v1.6 - Coins for points
       
       v1.7 - Powerups
       
       v1.8 - Sprites and Sounds
       
       v1.9 - Menu
       """

# I - Import and Initialize
import pygame,pySprites,random
from net import dqn
pygame.init()
pygame.mixer.init()

def change(car, allspi, obstacles):
    crashh = 0
    if car.road == 1:
        for i in range(8):
            car.rect.centerx += 4
            for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
                obstacle.reset()
                crashh = 1
            allspi.update(car.speed)
        car.road = 2
    else:
        for i in range(8):
            car.rect.centerx -= 4
            for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
                obstacle.reset()
                crashh = 1
            allspi.update(car.speed)
        car.road = 1
    return crashh
def keepgo(car, car1, vfree):
    a1 = 3
    a2 = 6
    v0 = round(car.speed/3.6)
    v1 = round(car1.speed/3.6)
    dfflow = round(v0*v0/(2*a1) + v0 + 5)
    demer = round(v0*v0/(2*a2) - v1*v1/(2 * a2) + v1 + 10)
    d1 = round((car.rect.top - car1.rect.bottom)/3)
    if car.road == car1.road:
        if  d1 - dfflow > 50 and d1 > demer:
            if abs(v1-v0) >= 3.6:
                v0 = v0 + 0.25*(d1 - dfflow) + 1.5 * ( v1 - v0)
            else:
                v0 = v0 + 0.25* (d1 - dfflow) + (v1 - v0)
        elif 50 >= d1-dfflow >- 20 and d1>demer:
            if abs(v1 - v0) >= 3.6:
                v0 = v0 + 0.5*(d1 - dfflow) + 1.5 * ( v1 - v0)
            else:
                v0 = v0 + 0.5* (d1 - dfflow) + ( v1 - v0)
        elif d1 - dfflow <= -20and d1 > demer :
            if abs(v1 - v0) >= 3.6:
                v0 = v0 + (d1 - dfflow) + 1.5 * ( v1 - v0)
            else:
                v0 = v0 + (d1 - dfflow) + ( v1 - v0)
        else:
            v0 = 0
    else:
        v0 = vfree/3.6
    if v0 > car.speed / 3.6:
        if v0 - car.speed / 3.6 > 6:
            car.speed += round(3.6 * 6)
            vdf = 6
        else:
            vdf = round(v0 - car.speed/3.6)
            car.speed = round(v0 * 3.6)
            
    else:
        if round(car.speed/3.6) - v0 > 6:
            car.speed -= round(3.6*6)
            vdf = 6
        else:
            vdf = round(car.speed/3.6 - v0)
            car.speed = round(v0 * 3.6)
    return vdf
def main():
    agent = dqn()
    agent.restore('save/ckpt')
    chao = 0
    gen = 0
    """Mainline logic for Getaway"""
    # D - Display configuration
    screen = 0
    #Road Background
    road = pySprites.road(screen)

    #Scorekeeper

    #Car sprite
    car = pySprites.player_car()


    
    #Obstacles
    opposing_cars_group = []
    car1 = pySprites.other_cars()
    opposing_cars_group.append(car1)
    obstacles = pygame.sprite.Group(opposing_cars_group,[])
    coin_group = []
    road_block_group = []
    speed_boost = []
    life_boost = []
    #allSprites Group
    allSprites = pygame.sprite.OrderedUpdates(road,car,opposing_cars_group,road_block_group)

 

    keepGoing = True

    move_up = False
    move_down = False
    move_left = False
    move_right = False
    counter = 0 

    speedboost = False
    boostcounter = 0
    invincibility_flag = False
    inv_counter = 0
    need_car = []
    vfree = 140
    vdf = 0
    state = [vfree, car.road,car1.road,10 * round(car.speed / 10), car1.speed, 10 * round((car.rect.top - car1.rect.bottom)/30)
             ]
    # L - Loop
    h = 0
    crashh = 0
    total_time = 0
    distance = 0
    huandao = 0
    chaoover = 0
    while keepGoing:
        total_time += 1
        if total_time%1000== 0:
            print(distance)
            print(h)
            vfree = 10 * (round(random.randint(80, 140)/10))
            agent.save_net('save/ckpt')
            h = 0
            distance = 0
        action = agent.egreedy_action(state)
        
    # T - Timer

        #Ingame clock counter
        
        # E - Event handling

        if action == 1:
            if car.road == 1:
                vdf = keepgo(car,car1,vfree)
            else:
                crashh = change(car, allSprites, obstacles)
        else:
            if car.road == 2:
                vdf = keepgo(car,car1,vfree)
            else:
                crashh = change(car, allSprites,obstacles)
        #Collision detection
        for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
            obstacle.reset()
            crashh = 1
        if crashh == 1:
            h += 1
        
        
        # R - Refresh display

        allSprites.update(car.speed)
        if crashh == 1:
            reward = -1000
        else:
            if car.road == 2:
                reward = car.speed/3.6 - vfree/3.6 - 0.1 * vdf - 0.2
            else:
                reward = car.speed/3.6 - vfree/3.6 - 0.1 * vdf
        distance += car.speed
        next_state = [vfree, car.road,car1.road,10 * round(car.speed / 36), round(car1.speed/3.6), 10 * round((car.rect.top - car1.rect.bottom)/30)
                      ]
        agent.preceive(state, action, round(reward), next_state, 0)
        crashh = 0
        state = next_state
def high_score(Scorekeeper):
    """Checks to see if the current score is higher than the old high score, if so, it rewrites the file with the new score"""
    
    #Try to open file, if it does not exist, write high score in new file
    try:
        score_file_r = open("score.txt","r")
        highscore = int(score_file_r.readline())
        score_file_r.close()
                    
        #If current points is higher than high score, current points becomes high score
        if Scorekeeper.get_points() > highscore:
            score_file = open("score.txt","w")
            score_file.write(str(Scorekeeper.get_points()))
            score_file.close()
                            
    except IOError:
        score_file = open("score.txt","w")
        score_file.write(str(Scorekeeper.get_points()))
        score_file.close()
        
        
    

#Run menu
main()
