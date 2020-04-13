"""
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
def change(car, allspi, screen, background, clock, obstacles, Scorekeeper):
    if car.road == 1:
        for i in range(8):
            car.rect.centerx += 4
            for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
                obstacle.reset()
                print('peng')
            allspi.clear(screen,background)
            allspi.update(car.speed)
            allspi.draw(screen)
            pygame.display.flip()
            clock.tick(30)
        car.road = 2
    else:
        for i in range(8):
            car.rect.centerx -= 4
            for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
                obstacle.reset()
                print('peng')
            allspi.clear(screen,background)
            allspi.update(car.speed)
            allspi.draw(screen)
            pygame.display.flip()
            
            clock.tick(30)
        car.road = 1

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
        elif 50 >= d1-dfflow >-20 and d1>demer:
            if abs(v1 - v0) >= 3.6:
                v0 = v0 + 0.5*(d1 - dfflow) + 1.5 * ( v1 - v0)
            else:
                v0 = v0 + 0.5* (d1 - dfflow) + ( v1 - v0)
        elif d1 - dfflow <= -20 and d1 > demer :
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
            vdf = v0 - car.speed/3.6
            car.speed = round(v0 * 3.6)
            
    else:
        if round(car.speed/3.6) - v0 > 6:
            car.speed -= round(3.6*6)
            vdf = 6
        else:
            vdf = car.speed/3.6 - v0
            car.speed = round(v0 * 3.6)
            
    return vdf  
def main():
    agent = dqn()
    agent.restore('save/ckpt')
    """Mainline logic for Getaway"""
    # D - Display configuration
    screen = pygame.display.set_mode((300, 700),0, 32)
    pygame.display.set_caption("DISPLAY!")

    # E - Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    #Sounds
    pygame.mixer.music.load("Sounds/bgm.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    crash = pygame.mixer.Sound("Sounds/crash.wav")
    crash.set_volume(0.3)
    
    coin = pygame.mixer.Sound("Sounds/coin.wav")
    coin.set_volume(0.3)
    
    power_up = pygame.mixer.Sound("Sounds/power_up.wav")
    power_up.set_volume(0.3)
    

    #Road Background
    road = pySprites.road(screen)

    #Scorekeeper


    #Car sprite
    car = pySprites.player_car()


    
    #Obstacles
    opposing_cars_group = []
    car1 = pySprites.other_cars()
    opposing_cars_group.append(car1)
    Scorekeeper = pySprites.ScoreKeeper(car, 100, 'speed')
    otherspeed = pySprites.ScoreKeeper(car1, 150, 'other_speed')

    #car2 = pySprites.other_cars()
             
    #opposing_cars_group.append(car2)
    obstacles = pygame.sprite.Group(opposing_cars_group,[])
    coin_group = []
    road_block_group = []
    speed_boost = []
    life_boost = []
    #allSprites Group

    # A - Action
 
      # A - Assign values
    clock = pygame.time.Clock()
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
    vfree = 90
    current_state = pySprites.neirong()
    current_state.bian = "side road"
    chedao = pySprites.showbian(current_state, 200,'Road')
    Vtree = pySprites.neirong()
    Vtree.bian = vfree
    zhuangtai = pySprites.showbian(Vtree, 50,'expect')
    allSprites = pygame.sprite.OrderedUpdates(chedao,zhuangtai,road,car,otherspeed,opposing_cars_group,road_block_group,Scorekeeper)

    # L - Loop
    h = 0
    vdf = 0
    crashh = 0
    distance = 0
    total_time = 0
    state = [vfree, car.road,car1.road,10 * round(car.speed / 36), round(car1.speed/3.6), 10 * round((car.rect.top - car1.rect.bottom)/30)
                      ]
    while keepGoing:
        total_time += 1
        if total_time%1000 == 0:
            agent.restore('save/ckpt')
            print(distance)
            print(h)
            h = 0
        action = agent.action(state)
    # T - Timer
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    vfree -= 5
                    Vtree.bian = vfree
                if event.key == pygame.K_UP:
                    vfree += 5
                    Vtree.bian = vfree
        #Ingame clock counter

        if action == 1:
            if car.road == 1:
                vdf = keepgo(car,car1,vfree)
            else:
                current_state.bian = "changing"
                crashh = change(car, allSprites, screen, background, clock,obstacles, Scorekeeper)
                current_state.bian = "main road"
        else:
            if car.road == 2:
                vdf = keepgo(car,car1,vfree)
            else:
                current_state.bian = "changing"
                crashh = change(car, allSprites,screen, background, clock,obstacles, Scorekeeper)
                current_state.bian = "over road"
 

            
            
        #Collision detection
        for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
            obstacle.reset()
            Scorekeeper.death()
            crashh = 1
            h += 1
            crash.play()
        
        if crashh == 1:
            reward = -1000
        else:
            if vdf > 3:
                reward = -150
            else:
                if car.road == 2:
                    reward = car.speed/3.6 - vfree/3.6 - 0.1 * vdf - 2
                else:
                    reward = car.speed/3.6 - vfree/3.6 - 0.1 * vdf
               # R - Refresh display
        
        allSprites.clear(screen,background)
        allSprites.update(car.speed)
        allSprites.draw(screen)
        if crashh == 1:
            reward = -1000
        else:
            if vdf > 3:
                reward = -150
            else:
                if car.road == 2:
                    reward = car.speed/3.6 - vfree/3.6 - 0.1 * vdf - 2
                else:
                    reward = car.speed/3.6 - vfree/3.6 - 0.1 * vdf       
        next_state = [vfree,car.road,car1.road,10 * round(car.speed / 36), round(car1.speed/3.6), 10 * round((car.rect.top - car1.rect.bottom)/30)
                      ]
        #agent.preceive(state, action, reward, next_state, 0)
        state = next_state
        distance += car.speed
        pygame.display.flip()
    # Close the game window
    pygame.quit()
    
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
        
        
def menu():
    """Menu program for Getaway"""
    
    # D - Menu Display
    screen = pygame.display.set_mode((558, 558))
    pygame.display.set_caption("Getaway Menu!")
 
    # E - Entities
    
    #Display the menu background
    background = pygame.image.load("Images/menu.gif")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    #A - Action
    #Assign
   
    keepGoing = True
 
    # L - Loop
    while keepGoing:
 
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            #Pressing space starts the game ( runs main )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    main() 
                    
    pygame.quit()

#Run menu
main()
