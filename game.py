import pygame

from config import Config
from scenes import (
    GameOverScene,
    GameScene,
    MainMenuScene,
    SceneManager,
    VictoryScene,
)


class Game:
    def __init__(self, config: Config):
        self.running = False
        self.config = config

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

        self.dt = 0.0

        self.score = 0
        self.keys = pygame.key.get_pressed()

        self._load_font()
        self._load_images()
        self._load_sounds()

        self.manager = SceneManager()
        self.manager.register(
            "menu",
            MainMenuScene(
                self.manager,
                self.config,
                self.font,
                self.menu_image,
            ),
        )
        self.manager.register(
            "game",
            GameScene(
                self.manager,
                self.config,
                self.player_image,
                self.memory_image,
                self.enemy_image,
                self.obstacle_image,
                self.font,
            ),
        )
        self.manager.register(
            "gameover",
            GameOverScene(
                self.manager,
                self.config,
                self.font,
            ),
        )
        self.manager.register(
            "victory",
            VictoryScene(
                self.manager,
                self.config,
                self.font,
            ),
        )
        self.manager.switch("menu")

        self.running = True

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
        self.enemy_image = pygame.transform.scale(
            pygame.image.load("images/dementor.svg").convert_alpha(),
            (self.config.tile_size * 0.5, self.config.tile_size * 0.5),
        )
        self.memory_image = pygame.transform.scale(
            pygame.image.load("images/memory.svg").convert_alpha(),
            (self.config.tile_size * 0.5, self.config.tile_size * 0.5),
        )
        self.obstacle_image = pygame.transform.scale(
            pygame.image.load("images/cloud.svg").convert_alpha(),
            (self.config.tile_size, self.config.tile_size),
        )
        self.menu_image = pygame.image.load(
            "images/menu_image.svg"
        ).convert_alpha()

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
                case _:
                    self.manager.handle_event(event)

        self.keys = pygame.key.get_pressed()

    def update(self):
        self.manager.update(self.dt, screen_rect=self.screen.get_rect())

    def draw(self):
        self.screen.fill("#006699")

        self.manager.draw(self.screen)

        pygame.display.flip()
