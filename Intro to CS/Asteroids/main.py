import arcade
import math
import random

SPRITE_SCALE = 0.5
width = 600
height = 600
MOVEMENT_SPEED = 10
L_SPEED = 5
class Spaceship(arcade.Sprite):
    def __init__(self):
        super().__init__("PNG/playerShip1_orange.png", SPRITE_SCALE)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > width - 1:
            self.right = width -1
        
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > height - 1:
            self.top = height - 1

class Astroids(arcade.Sprite):
    def __init__(self):
        super().__init__("PNG/Meteors/meteorBrown_med1.png", SPRITE_SCALE)
        speed = 1
        self.change_x = random.randint(-speed, speed)
        self.change_y = random.randint(-speed, speed)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.change_x *= -1
        if self.right > width:
            self.change_x *= -1
        if self.bottom < 0:
            self.change_y *= -1
        if self.top > height:
            self.change_y *= -1

class Laser(arcade.Sprite):
    def __init__(self):
        super().__init__("PNG/Lasers/laserRed14.png", SPRITE_SCALE)
    def update(self):
        self.center_y += self.change_y
        if self.top > height -1:
            self.kill()
    
class Game(arcade.Window):
    def __init__(self):
        super().__init__(width, height)
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.astroids_list = arcade.SpriteList()
        self.player_sprite = Spaceship()
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 300
        self.score = 0
        self.game_over = False

        for i in range(10):
            a = Astroids()
            a.center_x = random.randrange(width)
            a.center_y = random.randrange(height)
            self.astroids_list.append(a)
    def on_draw(self):
        if self.game_over == False:
            arcade.start_render()
            self.player_sprite.draw()
            self.bullet_list.draw()
            self.astroids_list.draw()
        else:
            if self.astroids_list == 0:
                arcade.draw_text(f"YOU WIN! \n Score {self.score}", 0, 300, arcade.color.BABY_BLUE,50, font_name='ariel')
            else:
                arcade.draw_text(f"GAME OVER!\n Score {self.score}", 0, 300, arcade.color.WHITE,50, font_name='ariel')
    def update(self, delta_time):
        if self.game_over == False:
            self.player_sprite.update()
            self.bullet_list.update()
            self.astroids_list.update()
            if len(self.astroids_list) == 0:
                self.game_over = True
            h_list = arcade.check_for_collision_with_list(self.player_sprite, self.astroids_list)
            if len(h_list) > 0:
                self.game_over = True
            for bullet in self.bullet_list:
                bullet.update()
                hit_list = arcade.check_for_collision_with_list(bullet, self.astroids_list)
                if len(hit_list) > 0:
                    bullet.kill()
                for astroid in hit_list:
                    astroid.kill()
                    self.score += 50
                
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
    #def on_mouse_motion(self, x, y, dx, dy):
    #    self.player_sprite.center_x = x
        """    def on_mouse_press(self, x , y, button, modifiers):
        print("HELLLLLOOOOO")
        l = Laser()
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        l.center_x = start_x
        l.bottom = self.player_sprite.top

        dest_x = x
        dest_y = y

        diff_x = dest_x - start_x
        diff_y = dest_y - start_y
        angle = math.atan2(diff_y, diff_x)
        l.angle = math.degrees(angle)
        print(f"Bullet Angle: {l.angle:.2f}")
        l.change_x = math.cos(angle) * L_SPEED
        l.change_y = math.sin(angle) * L_SPEED
        self.bullet_list.append(l)"""

    def on_mouse_release(self, x, y, button, modifiers):
        l = arcade.Sprite("PNG/Lasers/laserRed14.png", SPRITE_SCALE)
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        l.center_x = start_x
        l.bottom = self.player_sprite.top

        dest_x = x
        dest_y = y

        diff_x = dest_x - start_x
        diff_y = dest_y - start_y
        angle = math.atan2(diff_y, diff_x)
        l.angle = math.degrees(angle) + 90
        print(f"Bullet Angle: {l.angle:.2f}")
        l.change_x = math.cos(angle) * L_SPEED
        l.change_y = math.sin(angle) * L_SPEED
        self.bullet_list.append(l)
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

        
        

def main():
    window = Game()
    window.on_draw()
    arcade.run()

if __name__ == "__main__":
    main()
