import pygame

from config import Config
from player import Player
from ui import Ui

SCREEN_MARGIN = 100


class Game:
    def __init__(self, config: Config):
        self.running = False
        self.config = config

        self.game_over = False

    def __enter__(self):
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512,
            allowedchanges=pygame.AUDIO_ALLOW_ANY_CHANGE,
        )
        pygame.init()
        pygame.mixer.set_num_channels(16)

        self.flags = 0
        if self.config.fullscreen:
            self.flags |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height),
            flags=self.flags,
        )
        pygame.display.set_caption("Ron's brain")

        self.clock = pygame.time.Clock()

        self.world_bounds = pygame.Rect(
            0, 0, self.config.window_width, self.config.window_height
        ).inflate(SCREEN_MARGIN, SCREEN_MARGIN)

        self.dt = 0.0

        self.score = 0
        self.keys = pygame.key.get_pressed()

        self._load_font()
        self._load_images()
        self._load_sounds()

        player_pos = pygame.Vector2(
            self.screen.get_rect().centerx, self.config.window_height - 200
        )

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.ui_sprites = pygame.sprite.LayeredUpdates()

        self.player = Player(
            player_pos,
            self.player_image,
            self.config.speed,
        )
        self.all_sprites.add(self.player, layer=3)

        self.ui = Ui(
            self.config.window_width,
            self.config.window_height,
            self.font,
            self.config.gui_text_color,
        )
        self.ui_sprites.add(self.ui, layer=10)

        self.running = True

        self.is_paused = False

        return self

    def __exit__(self, *args):
        pygame.quit()

    def _load_font(self) -> None:
        self.font = pygame.font.Font(
            "fonts/BlackOpsOne-Regular.ttf", self.config.gui_font_size
        )

    def _load_images(self) -> None:
        self.player_image = pygame.transform.scale(
            pygame.image.load("images/owl.svg").convert_alpha(),
            (self.config.tile_size, self.config.tile_size),
        )

    def _load_sounds(self) -> None:
        pygame.mixer.music.load("sounds/theme.mp3")
        pygame.mixer.music.play(-1)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.config.fps) / 1000
            self.watch_for_events()

            self.update()

            self.draw()

    def watch_for_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

        self.keys = pygame.key.get_pressed()

    def update(self):
        self.ui_sprites.update(self.dt)
        self.all_sprites.update(self.dt, screen_rect=self.screen.get_rect())

    def draw(self):
        self.screen.fill("#006699")

        self.all_sprites.draw(self.screen)
        self.ui_sprites.draw(self.screen)

        pygame.display.flip()
