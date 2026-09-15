import pygame

from config import Config
from enemy import Enemy
from memory import Memory
from obstacle import Obstacle
from player import Player
from scenes.scene import AbstractScene
from scenes.scene_manager import SceneManager

LEVELS = [
    {
        "threshold": 99,
        "bg_color": "#55ddffff",
        "enemy_speed": (79, 160),
        "enemies": 2,
        "memories": 4,
        "obstacles": -1,
        "spawn_interval": 4.0,
    },
    {
        "threshold": 200,
        "bg_color": "#00c4efff",
        "enemy_speed": (119, 220),
        "enemies": 3,
        "memories": 5,
        "obstacles": 2,
        "spawn_interval": 3.0,
    },
    {
        "threshold": 300,
        "bg_color": "#4d7a83ff",
        "enemy_speed": (159, 280),
        "enemies": 4,
        "memories": 6,
        "obstacles": 4,
        "spawn_interval": 2.0,
    },
]


class GameScene(AbstractScene):
    def __init__(
        self,
        manager: SceneManager,
        config: Config,
        player_image: pygame.Surface,
        memory_image: pygame.Surface,
        enemy_image: pygame.Surface,
        obstacle_image: pygame.Surface,
        font: pygame.Font,
        collect_sound: pygame.Sound,
        eat_sound: pygame.Sound,
    ):
        self.config = config

        self.manager = manager

        self.player = None
        self.player_image = player_image
        self.memory_image = memory_image
        self.enemy_image = enemy_image
        self.obstacle_image = obstacle_image

        self.enemies = pygame.sprite.Group()
        self.memories = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.font = font
        self.collect_sound = collect_sound
        self.eat_sound = eat_sound

        self.score = 0
        self.level_index = 0
        self.spawn_timer = 0
        self.level_flash = 0  # Level change timer

    @property
    def level_config(self):
        return LEVELS[self.level_index]

    @property
    def level_number(self):
        return self.level_index + 1

    def on_enter(self, *args, do_reset: bool = True, **kwargs):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sounds/game_theme.wav")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        if do_reset:
            self.score = 0
            self.level_index = 0
            self.spawn_timer = 0
            self.level_flash = 1.5

            self._setup_level()

    def _setup_level(self):
        self.enemies.empty()
        self.memories.empty()
        self.obstacles.empty()
        self.all_sprites.empty()

        for _ in range(self.level_config["obstacles"]):
            obs = Obstacle(
                self.config.window_width,
                self.config.window_height,
                self.obstacle_image,
                self.player,
            )
            self.obstacles.add(obs)
            self.all_sprites.add(obs)

        player_pos = pygame.Vector2(
            self.config.window_width // 2, self.config.window_height // 2
        )
        self.player = Player(
            player_pos,
            self.player_image,
            self.config.speed,
        )
        self.all_sprites.add(self.player, layer=3)

        for _ in range(self.level_config["enemies"]):
            enemy = Enemy(
                self.enemy_image,
                self.player,
                self.config.window_width,
                self.config.window_height,
                self.level_config["enemy_speed"],
            )
            self.enemies.add(enemy)
            self.all_sprites.add(enemy, layer=2)

        for _ in range(self.level_config["memories"]):
            memory = Memory(
                self.memory_image,
                self.config.window_width,
                self.config.window_height,
            )
            self.memories.add(memory)
            self.all_sprites.add(memory, level=1)

    def _advance_level(self) -> None:
        self.level_index += 1
        self.level_flash = 1.5
        self.spawn_timer = 0
        if self.level_index == len(LEVELS):
            self.manager.switch("victory")
            return
        self._setup_level()

    def handle_event(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.switch("menu", game_in_progress=True)

    def update(self, dt: float, *args, **kwargs):
        self.all_sprites.update(dt, *args, **kwargs)

        collected = pygame.sprite.spritecollide(
            self.player, self.memories, True, pygame.sprite.collide_mask
        )

        stolen = pygame.sprite.groupcollide(
            self.enemies, self.memories, False, True
        )

        for _ in collected:
            self.score += 10
            self.collect_sound.play()

        for _ in stolen:
            self.eat_sound.play()

        for _ in range(len(collected) + len(stolen)):
            new_mem = Memory(
                self.memory_image,
                self.config.window_width,
                self.config.window_height,
            )
            self.memories.add(new_mem)
            self.all_sprites.add(new_mem)

        if (
            pygame.sprite.spritecollideany(
                self.player, self.enemies, pygame.sprite.collide_mask
            )
            and not self.player.is_invulnarable
        ):
            self._game_over()
            return

        if (
            pygame.sprite.spritecollideany(
                self.player, self.obstacles, pygame.sprite.collide_mask
            )
            and not self.player.is_invulnarable
        ):
            self._game_over()
            return

        self.spawn_timer += dt
        if self.spawn_timer > self.level_config["spawn_interval"]:
            self.spawn_timer = 0

            enemy = Enemy(
                self.enemy_image,
                self.player,
                self.config.window_width,
                self.config.window_height,
                self.level_config["enemy_speed"],
            )

            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        threshold = self.level_config["threshold"]

        if self.score >= threshold:
            self._advance_level()

        if self.level_flash > 0:
            self.level_flash -= dt

    def _game_over(self):
        self.manager.switch(
            "gameover",
            final_score=self.score,
            reached_level=self.level_number,
        )

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill(self.level_config["bg_color"])
        self.all_sprites.draw(surf)

        score_text = self.font.render(f"Score: {self.score}", True, "white")
        surf.blit(score_text, (10, 10))

        level_text = self.font.render(
            f"Level {self.level_number}", True, "white"
        )
        surf.blit(level_text, (self.config.window_width - 110, 10))

        esc_text = self.font.render("ESC — Menu", True, "#aaaaaa")
        surf.blit(
            esc_text,
            (
                self.config.window_width - esc_text.get_rect().width - 10,
                self.config.window_height - 30,
            ),
        )

        if self.level_flash > 0:
            flash_text = self.font.render(
                f"LEVEL {self.level_number}", True, "white"
            )

            alpha = min(255, int(self.level_flash * 200))
            flash_text.set_alpha(alpha)
            surf.blit(
                flash_text,
                flash_text.get_rect(
                    center=(
                        self.config.window_width // 2,
                        self.config.window_height // 2,
                    )
                ),
            )
