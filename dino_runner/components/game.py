import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.obstacles.shield import Shield
from dino_runner.components.powerups.power_up_manager import PowerUpManager
from dino_runner.components.score import Score
from dino_runner.components import text_utils

from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, SMALL_CACTUS, TITLE, FPS

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

        self.death_count = 0
        self.score = Score()
        self.power_up_manager = PowerUpManager()

   
    
    def execute(self):
        self.executing = True

        while self.executing:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.score.reset()
        self.game_speed = 20
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.score.update(self)
        self.power_up_manager.update(self.game_speed, self.player, self.score.score)
 


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #white
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_activate()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        #dibujar la ventana *
        self.screen.fill((255,255,255))
        #Mostrar un mensaje de bienvenida*
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:

            text, text_rect = text_utils.get_centered_message('Press any Key to Start')
            self.screen.blit(text, text_rect)
            #font = pygame.font.Font(FONT_STYLE, 30)
            #text_component = font.render("Press any key to play", True, (0,0,0))
            #text_rect = text_component.get_rect()
            #text_rect.center = (half_screen_width, half_screen_height)
            #self.screen.blit(text_component,text_rect)
        else:
            text, text_rect = text_utils.get_centered_message('Press any Key to Restart')
            score, score_rect = text_utils.get_centered_message('Your Score: ' + str(self.score.score),
                                                                height=half_screen_height + 50)
            
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count),
                                                                height=half_screen_height + 100)
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(death, death_rect)
            #Mostrar mensaje de volver a jugar ()
            # MOstrar total de muertes
            # MOstrar el puntaje
        #Mostrar imagen en el menu*

        self.screen.blit(RUNNING[0], (half_screen_width - 30, half_screen_height + 140))
        #actulizar ventana*
        pygame.display.update()
        #escuchar eventos
        self.handle_key_events_on_menu()
    
    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:

                self.run()

    def on_death (self):
        is_invencible = self.player.type == SHIELD_TYPE
        if not is_invencible:
            self.playing = False
            self.death_count += 1
        return is_invencible

    def draw_power_up_activate (self):
        
        if self.player.has_power_up:
            time_to_show = round ((self.player.power_up_time_up - pygame.time.get_ticks())) / 1000
            if time_to_show >= 0:
                pass
                #pantalla
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE