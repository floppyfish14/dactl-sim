# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
 
import pygame, random
pygame.init()

 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
SKY = (101, 202, 246)
DKGREEN = (0, 100, 0)

# create the stickman kill counter
enemies_killed = 0
 
# This class represents the player
# It derives from the "Sprite" class in Pygame
class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Variables to hold the height and width of the block
        width = 20
        height = 15
 
        # Create an image of the player, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('dactl.png')
 
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
    
    def turn_around(self):
        global direction
        self.image = pygame.transform.flip(self.image, True, False)
        if direction:
            direction = False
        else:
            direction = True
    # Update the position of the player
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
 
        # Fetch the x and y out of the list, just like we'd fetch letters out
        # of a string.
        # NOTE: If you want to keep the mouse at the bottom of the screen, just
        # set y = 380, and not update it with the mouse position stored in
        # pos[1]
        x = pos[0]
        y = pos[1]
 
        # Set the attribute for the top left corner where this object is
        # located
        self.rect.x = x
        self.rect.y = y

        self.collision = pygame.sprite.spritecollide(self, weapon_sprite_list, True)
        if self.collision:
            global start
            global done
            if start == True:
                clear_data()

        self.rect.clamp_ip(0, 0, screen_width, screen_height-60)

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Variables to hold the height and width of the block
        width = 10
        height = 2

        global direction


        # make it look like it is coming out of dactl's face
        if direction:
            x = pos[0]+45
            y = pos[1]+14
        else:
            x = pos[0]-45
            y = pos[1]+14

        self.image = pygame.image.load('laser.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.direction = direction

    def update(self):

        if self.direction:
            self.rect.x += 20
        else:
            self.rect.x -= 20
            


class Poop(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Variables to hold the height and width of the block
        width = 20
        height = 15

        # make it look like it is coming out of dactl's butt
        x = pos[0]+22
        y = pos[1]+19

        self.image = pygame.image.load('poop.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):

        self.rect.y += 3
        if self.rect.y >= screen_height:
            self.kill()

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        width = 2
        height = 2

        self.image = pygame.image.load('spear.png')
        self.rect = self.image.get_rect()

        self.speed_x = random.randint(-2,2)
        self.speed_y = random.randint(1,3)

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y



class Stickman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Variables to hold the height and width of the block
        width = 20
        height = 15

        # make it look like it is coming out of dactl's butt
        x = random.randint(0,screen_width)
        y = screen_height-100

        self.image = pygame.image.load('stickman.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed_x = random.randint(-2, 2)

    def attack(self):
        spear = Spear(self.rect.x,self.rect.y)
        # add the spear to the list of sprites

    def update(self):

        self.collision = pygame.sprite.spritecollide(self, poop_sprite_list, True)
        self.rect.x += self.speed_x

        self.rect.clamp_ip(0, 0, screen_width-20, screen_height-60)

        if self.rect.x == 0 or self.rect.right >= screen_width-20:
            self.speed_x = -self.speed_x

        if self.collision:
            self.kill()
            global enemies_killed 
            global start
            if not start:
                pass
            elif start:
                enemies_killed = enemies_killed + 1

        if random.randint(0,3000) > 2965:
            spear = Spear(self.rect.x, self.rect.y)
            weapon_sprite_list.add(spear)

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Variables to hold the height and width of the block
        width = 20
        height = 15

        x = random.randint(0,screen_width)
        y = random.randint(300,screen_height)

        self.image = pygame.image.load('plane.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed_x = random.randint(-5, 5)

    def update(self):

        self.collision = pygame.sprite.spritecollide(self, [poop_sprite_list,laser_sprite_list], True)
        self.rect.x += self.speed_x

        self.rect.clamp_ip(0, 0, screen_width-20, screen_height-60)

        if self.rect.x == 0 or self.rect.right >= screen_width-20:
            self.speed_x = -self.speed_x

        if self.collision:
            self.kill()
            global enemies_killed 
            global start
            if not start:
                pass
            elif start:
                enemies_killed = enemies_killed + 1

def updateKillCount():
    font = pygame.font.Font('freesansbold.ttf', 32)
 
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Kill Count: %i' % enemies_killed, True, BLACK)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (screen_width // 2, screen_height // 2)

    screen.blit(text, textRect)
    # pygame.display.update()

def splash_screen():
    start_game = pygame.image.load('start.png')
    screen.blit(start_game, (screen_width // 2.85, screen_height // 2.75))
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Press spacebar to start...', True, BLACK)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (screen_width // 2, screen_height // 1.5)

    screen.blit(text, textRect)

    # pygame.display.update()

def clear_data():
    global done
    global start
    global enemies_killed
    global enemy_sprite_list
    global player_sprite_list
    global poop_sprite_list
    global weapon_sprite_list

    enemies_killed = 0
    done = False
    start = False

    enemy_sprite_list.empty()
    weapon_sprite_list.empty()
    poop_sprite_list.empty()
    pygame.display.update()

# Set the height and width of the screen
size = [1400, 800]
screen = pygame.display.set_mode(size)

screen_width = size[0]
screen_height = size[1]
 
# Don't display the mouse pointer
pygame.mouse.set_visible(False)
 
# Loop until the user clicks the close button.
done = False
start = False
direction = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# This is a list of 'sprites.' Each sprite in the program (there is only 1) is
# added to this list. The list is managed by a class called 'Group.'
player_sprite_list = pygame.sprite.Group()
poop_sprite_list = pygame.sprite.Group()
enemy_sprite_list = pygame.sprite.Group()
weapon_sprite_list = pygame.sprite.Group()
plane_sprite_list = pygame.sprite.Group()
laser_sprite_list = pygame.sprite.Group()


# This represents the ball controlled by the player
player = Player()

# Add the ball to the list of player-controlled objects
player_sprite_list.add(player)    

# -------- Main Program Loop -----------
while not done:
    cursor_pos = pygame.mouse.get_pos()

    while len(enemy_sprite_list) < 5:
        stickman = Stickman()
        enemy_sprite_list.add(stickman)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            poop_sprite_list.add(Poop(cursor_pos))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
            if event.key == pygame.K_a:
                laser_sprite_list.add(Laser(cursor_pos))
            if event.key == pygame.K_f:
                player.turn_around()
        # detect letter a or j
        # shoot laser based on letter

    # --- Game logic
    player_sprite_list.update()
    poop_sprite_list.update()
    enemy_sprite_list.update()
    weapon_sprite_list.update()
    plane_sprite_list.update()
    laser_sprite_list.update()
 
    # --- Display / Drawing code
 
    # Clear the screen
    screen.fill(SKY)

    # draw the ground
    ground = pygame.draw.rect(screen, DKGREEN, pygame.Rect(0, screen_height-60, screen_width, 60))

    if start == False:
        splash_screen()
 
    # Update the position of the sprites and draw them
    player_sprite_list.draw(screen)
    poop_sprite_list.draw(screen)
    enemy_sprite_list.draw(screen)
    weapon_sprite_list.draw(screen)
    plane_sprite_list.draw(screen)
    laser_sprite_list.draw(screen)

    if start == True:
        updateKillCount()

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()