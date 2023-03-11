from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.15)
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render("YOU WIN !!!", True, (255,255,255))
lose = font2.render("YOU LOSE !!!", True, (200, 0, 0))


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

score = 0 #кількість збитих ворогів
lost = 0 #кількість пропущених ворогів
goal = 10 #кількість ворогів, яких потрібно збити
max_lost = 5 #максимально можлива кількість пропущених ворогів
life = 3 #кількість життів корабля

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-15)
        bullets.add(bullet)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width,win_height))

ship = Player(img_hero, 5, win_height-100,80,100,10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid(img_ast, randint(30, win_width-30), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)

bullets = sprite.Group()
run = True
finish = False

rel_time = False #прапор, що контролює перезаряджання
num_fire = 0 #підрахунок пострілів

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<5 and rel_time==False:
                    num_fire+=1
                    fire_sound.play()
                    ship.fire()
                if num_fire>=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))
        
        text = font1.render("Рахунок: "+str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font1.render("Пропущено: "+str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render("Wait, reloading...", 1, (150,0,0))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score = score + 1
            asteroid = Enemy(img_ast, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            life -= 1

        if life == 0 or lost>= max_lost:
            finish = True
            window.blit(lose, (200,200))
            refresh = font1.render("Restarting the game...", 1, (150, 0, 0))
            window.blit(refresh, (250, 450))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))
            refresh = font1.render("Restarting the game...", 1, (150, 0, 0))
            window.blit(refresh, (250, 450))

        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        elif life == 1:
            life_color = (150, 0, 0)

        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        for i in range(1,3):
            asteroid = Asteroid(img_ast, randint(30, win_width-30), -40, 80, 50, randint(1,5))
            asteroids.add(asteroid)

    time.delay(50)