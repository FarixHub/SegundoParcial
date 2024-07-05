import pygame
import random
import os

# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 0
        self.bullets = pygame.sprite.Group()
        self.powered_up = False
        self.shoot_sound = load_sound

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0

        self.bullets.update()

    def shoot(self):
        if not self.powered_up:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
        else:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            self.bullets.add(bullet1, bullet2)
        self.shoot_sound.play()

    def power_up(self):
        self.powered_up = True
        pygame.time.set_timer(pygame.USEREVENT, 5000)

    def power_down(self):
        self.powered_up = False

# Clase Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Clase Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800 - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 8)
        self.speedx = random.randint(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > 600 or self.rect.left < -25 or self.rect.right > 825:
            self.rect.x = random.randint(0, 800 - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 8)

# Clase PowerUp
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800 - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 600:
            self.kill()

# Función para cargar imágenes
def load_image(path):
    return pygame.image.load(os.path.join(path))

# Función para cargar sonidos
def load_sound(path):
    return pygame.mixer.Sound(os.path.join(path))

# Clase Button
class Button:
    def __init__(self, surface, text, rect, color, text_color):
        self.surface = surface
        self.text = text
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
