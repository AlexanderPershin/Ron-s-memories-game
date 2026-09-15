import pygame

from config import Config
from scenes.scene import AbstractScene
from scenes.scene_manager import SceneManager


class MainMenuScene(AbstractScene):
    def __init__(
        self,
        manager: SceneManager,
        config: Config,
        font: pygame.Font,
    ):
        self.manager = manager
        self.config = config
        self.font = font

    def handle_event(self, event: pygame.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.manager.switch("game")
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill("#aaaaaa")

        title = self.font.render("MAIN MENU", True, "#ffffff")

        hint = self.font.render(
            "ENTER / SPACE — Start    ESC — Quit", True, (200, 200, 200)
        )

        surf.blit(
            title,
            title.get_rect(
                center=(
                    self.config.window_width // 2,
                    self.config.window_height // 2 - 40,
                )
            ),
        )
        surf.blit(
            hint,
            hint.get_rect(
                center=(
                    self.config.window_width // 2,
                    self.config.window_height // 2 + 40,
                )
            ),
        )
