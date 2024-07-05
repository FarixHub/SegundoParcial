import pygame
import sys
import random
import csv
import json
from modules import Player, Enemy, PowerUp, load_image, load_sound, Button

# Inicializar Pygame
pygame.init()

# Configuraciones del juego
#ANCHO, PESO
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Game")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar recursos
background = load_image('assets/Background.png')
player_image = load_image('assets/Player.png')
enemy_image = load_image('assets/Enemigo.png')
powerup_image = load_image('assets/Powerup.png')
shoot_image = load_image('assets/LaserFoto.png')
shoot_sound = load_sound('assets/Laser.wav')
pygame.mixer.music.load('assets/MusicaFondo.ogg')

# Fuente
font = pygame.font.Font(None, 36)

# Cargar configuración desde JSON
with open('data/config.json') as f:
    config = json.load(f)

# Pantallas del juego
#BOTON DE START, OPCIONES, SALIR
def show_start_screen():
    screen.fill(WHITE)
    title = font.render("SKILL SECTION", True, BLACK) #NOMBRE Y COLOR DEL TITULO DEL JUEGO
    start_button = Button(screen, "Start", (WIDTH//2 - 50, HEIGHT//2 - 25, 100, 50), WHITE, BLACK) #ANCHO, ALTURA Y COLOR DEL BOTON DE INICIO
    options_button = Button(screen, "Options", (WIDTH//2 - 50, HEIGHT//2 + 50, 100, 50), WHITE, BLACK) #ANCHO, ALTURA Y COLOR DEL BOTON DE OPCIONES
    quit_button = Button(screen, "Quit", (WIDTH//2 - 50, HEIGHT//2 + 125, 100, 50), WHITE, BLACK) #ANCHO, ALTURA Y COLOR DEL BOTON DE SALIR 
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4)) #ANCHO Y ALTURA DE LA PANTALLA DONDE APARECERAN LOS BOTONES 
    pygame.display.flip()
    
#Mientras se este esperando en la pantalla de espera
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Usuario clickea el boton de iniciar
                if start_button.is_clicked(event.pos):
                    waiting = False
                #Usuario clickea el boton de opciones
                elif options_button.is_clicked(event.pos):
                    show_options_screen()
                #Usuario clickea el boton de salir
                elif quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
#Definimos una función de opciones del juego
def show_options_screen():
    screen.fill(WHITE) #COLOR DEL FONDO DE LA PANTALLA
    options_title = font.render("Options", True, BLACK) #TITULO Y COLOR DEL MISMO
    back_button = Button(screen, "Back", (WIDTH//2 - 50, HEIGHT//2 + 125, 100, 50), WHITE, BLACK) #BOTON DE REGRESO DENTRO DE OPCIONES
    screen.blit(options_title, (WIDTH//2 - options_title.get_width()//2, HEIGHT//4)) #ANCHO Y ALTURA DEL BOTON DE OPCIONES
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.is_clicked(event.pos):
                waiting = False
#Definimos una función para cuando el juego se termina
def show_game_over_screen(score):
    screen.fill(WHITE)
    game_over_title = font.render("Game Over", True, BLACK) #MUESTRA TITULO DE QUE TERMINO EL JUEGO
    score_text = font.render(f"Score: {score}", True, BLACK) #MUESTRA EL PUNTAJE DEL JUGADOR
    restart_button = Button(screen, "Restart", (WIDTH//2 - 50, HEIGHT//2 - 25, 100, 50), WHITE, BLACK) #BOTON DE REINICIAR EL JUEGO
    quit_button = Button(screen, "Quit", (WIDTH//2 - 50, HEIGHT//2 + 50, 100, 50), WHITE, BLACK) #BOTON DE SALIR DEL JUEGO 
    screen.blit(game_over_title, (WIDTH//2 - game_over_title.get_width()//2, HEIGHT//4)) #ANCHO Y ALTURA DEL TEXTO "GAME OVER"
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//6)) #ANCHO Y ALTURA DEL TEXTO DEL PUNTAJE OBTENIDO
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    main()
                elif quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

# Juego principal
def main():
    pygame.mixer.music.play(-1)
    player = Player(player_image, WIDTH // 9, HEIGHT - 50)
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    score = 0
    lives = 3
    
    max_enemies = 5  # Número máximo de enemigos permitidos en la pantalla

    for _ in range(max_enemies):
        enemy = Enemy(enemy_image)
        enemies.add(enemy)
        all_sprites.add(enemy)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        # Colisiones
        hits = pygame.sprite.groupcollide(enemies, player.bullets, True, True)
        for hit in hits:
            score += 10
            hit_sound.play()
            enemy = Enemy(enemy_image)
            enemies.add(enemy)
            all_sprites.add(enemy)

        if pygame.sprite.spritecollideany(player, enemies):
            lives -= 1
            if lives == 0:
                save_score(score)
                show_game_over_screen(score)
                running = False

        if random.random() < 0.01:
            powerup = PowerUp(powerup_image)
            powerups.add(powerup)
            all_sprites.add(powerup)

        if pygame.sprite.spritecollide(player, powerups, True):
            player.power_up()
            
        background_rect = background.get_rect()
        screen.blit(background, background_rect.topleft)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 18, WIDTH // 2, 10)
        draw_text(screen, f"Lives: {lives}", 18, WIDTH // 2, 40)
        pygame.display.flip()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
#Cuando el usuario suma 1 punto se crea una nueva linea en el csv de score
def save_score(score):
    with open('data/scores.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([score])

if __name__ == "__main__":
    show_start_screen()
    main()
