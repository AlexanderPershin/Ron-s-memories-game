import pygame

from config import Config
from scenes.scene import AbstractScene
from scenes.scene_manager import SceneManager


class VictoryScene(AbstractScene):
    def __init__(
        self,
        manager: SceneManager,
        config: Config,
        font: pygame.Font,
    ):
        self.manager = manager
        self.config = config
        self.font = font

        self.final_score = 0
        self.reached_level = 1

    def handle_event(self, event: pygame.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.manager.switch("game")
                elif event.key == pygame.K_ESCAPE:
                    self.manager.switch("menu")

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill("lightblue")
        title = self.font.render(
            "You have won! Congratulations!", True, "#006699"
        )
        hint = self.font.render(
            "ENTER — New run    ESC — Menu", True, "#aaaaaa"
        )

        surf.blit(
            title,
            title.get_rect(
                center=(
                    self.config.window_width // 2,
                    self.config.window_height // 2 - 80,
                )
            ),
        )
        surf.blit(
            hint,
            hint.get_rect(
                center=(
                    self.config.window_width // 2,
                    self.config.window_height // 2,
                )
            ),
        )
