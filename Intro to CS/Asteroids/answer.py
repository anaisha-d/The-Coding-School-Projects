import arcade
import random


# GAME CONSTANTS - change to change difficulty
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

RECT_WIDTH = 50
RECT_HEIGHT = 50

LASER_SCALE = 0.5
SPRITE_SCALE = 0.5

PLAYER_SPEED = 5
PLAYER_LASER_SPEED = 6
ENEMY_SPEED = -2.5
ENEMY_LASER_SPEED = -6
METEOR_SPEED = -2


# Top portion of code is classes for all of our 'sprites' or objects in the game
# (enemy ships, meteors, lasers, etc.)

'''
Enemy makes use of inheritance by taking in arcade.Sprite as a parameter
'Sprite' is the parent class, which includes many more fields and funcions than 
we need. But, because the Sprite class isn't defined in this file, we use the 
module name 'arcade' which holds the Sprite class. Now, we can call 
super().__init__() in the constructor for these classes to invoke the 
constructor of the Sprite class.
'''

class Enemy(arcade.Sprite):

    def __init__(self):
        super().__init__("PNG/Enemies/enemyBlack1.png",
                         SPRITE_SCALE)

    def update(self):
        # Only change y position (enemy can't move side to side)
        self.center_y += ENEMY_SPEED

        # If enemy flies below screen, remove it
        if self.top < 0:
            self.kill()

class Meteor(arcade.Sprite):

    def __init__(self):
        super().__init__("PNG/Meteors/meteorBrown_big1.png", 
                         SPRITE_SCALE)

    def update(self):
        # Meteor can also only move side to side
        self.center_y += METEOR_SPEED

        # If meteor flies below screen, remove it
        if self.top < 0:
            self.kill()

class Player_Laser(arcade.Sprite):

    def __init__(self):
        super().__init__("PNG/Lasers/laserBlue01.png", 
                         LASER_SCALE)

    def update(self):
        self.center_y += PLAYER_LASER_SPEED

        # If laser flies off top of screen, remove it
        if self.bottom > 600:
            self.kill()

class Enemy_Laser(arcade.Sprite):

    def __init__(self):
        super().__init__("PNG/Lasers/laserRed01.png", 
                         LASER_SCALE)

    def update(self):
        self.center_y += ENEMY_LASER_SPEED

        # If laser flies off bottom of screen, remove it
        if self.top < 0:
            self.kill()

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("PNG/playerShip1_orange.png", 
                         SPRITE_SCALE)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 30
        self.delta_x = 0
        self.laser_list = arcade.SpriteList()

    def update(self):
        # Only change x position
        self.center_x += self.delta_x

        # See if we've gone beyond the border. If so, reset our position back 
        # to the border.
        if self.center_x < RECT_WIDTH // 2:
            self.center_x = RECT_WIDTH // 2
        if self.center_x > SCREEN_WIDTH - (RECT_WIDTH // 2):
            self.center_x = SCREEN_WIDTH - (RECT_WIDTH // 2)


'''
Game class. Responsible for all of the game logic.
'''
class Game(arcade.Window):

    def __init__(self, width, height):

        # Initialize the window using the parent class and set the 
        # background color
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK)

        # Initialize game information
        self.score = 0 # Score starts at 0
        self.game_over = False

        # Initialize sprites here
        self.player = Player()
        self.enemy_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()

    '''
    Holds all of the game logic. Check for target hits and object collisions 
    with the player.
    '''
    def update(self, delta_time):

        if not self.game_over:
            # Call update on the player and all the sprites already existing
            self.player.update()
            self.all_sprites_list.update()

            # Randomly create meteors
            if random.randrange(200) == 0: # once in every 200 updates
                meteor = Meteor()
                meteor.center_x = random.randint(1, 600)
                meteor.bottom = self.height
                self.meteor_list.append(meteor)
                self.all_sprites_list.append(meteor)

            # Randomly create enemies
            if random.randrange(100) == 0: # once in every 100 updates
                enemy = Enemy()
                enemy.center_x = random.randint(1, 600)
                enemy.bottom = self.height
                self.enemy_list.append(enemy)
                self.all_sprites_list.append(enemy)

            # Loop through enemies and randomly shoot lasers
            for enemy in self.enemy_list:
                # Decrease 100 for more frequent lasers
                if random.randrange(0, 100) == 0:
                    laser = Enemy_Laser()
                    laser.center_x = enemy.center_x
                    laser.angle = 180
                    laser.top = enemy.bottom
                    self.all_sprites_list.append(laser)

            # Check if any player's lasers collided with any objects
            for laser in self.player.laser_list:
                # Create lists of the objects hit by the player's lasers
                meteor_hit_list = arcade.check_for_collision_with_list(laser, self.meteor_list)
                enemy_hit_list = arcade.check_for_collision_with_list(laser, self.enemy_list)

                # For every meteor we hit, add 1 to the score and remove 
                # the meteor, laser
                for meteor in meteor_hit_list:
                    meteor.kill()
                    laser.kill()
                    self.score += 1

                # For every enemy we hit, add 3 to the score and remove the 
                # enemy, laser
                for enemy in enemy_hit_list:
                    enemy.kill()
                    laser.kill()
                    self.score += 3

            # Check if any objects hit the player
            for sprite in self.all_sprites_list:
                collision = arcade.check_for_collision(sprite, self.player)
                if collision:
                    self.player.kill()
                    self.game_over = True
                    # Print the player's final score to the terminal
                    print("Game over! Your score was " + str(self.score))

    '''
    Draw the screen (after updating).
    '''
    def on_draw(self):

        # start_render() should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on the player and the all_sprites_list 
        # (which holds everything besides the player)
        self.player.draw()
        self.all_sprites_list.draw()

        # Print out the score
        arcade.draw_text(f"Score: {self.score}", 20, 570, arcade.color.WHITE, 12)

    '''
    Called whenever a key on the keyboard is pressed.
    '''
    def on_key_press(self, key, key_modifiers):

        if key == arcade.key.LEFT:
            self.player.delta_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.delta_x = PLAYER_SPEED
        elif key == arcade.key.SPACE:
            # Create laser
            laser = Player_Laser()
            laser.center_x = self.player.center_x
            laser.angle = 0
            laser.bottom = self.player.top

            # Add laser to player's laser list AND sprite list
            self.player.laser_list.append(laser)
            self.all_sprites_list.append(laser)

    '''
    Called whenever the user releases a left or right key. Stops player's movement.
    '''
    def on_key_release(self, key, key_modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.delta_x = 0


# Set up the window and run the game
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()