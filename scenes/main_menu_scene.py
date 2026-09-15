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
        image: pygame.Surface,
    ):
        self.manager = manager
        self.config = config
        self.font = font
        self.image = image

        self.title = self.font.render("Ron's Memories", True, "#009900")
        self.title_rect = self.title.get_rect(
            center=(
                self.config.window_width // 2,
                self.config.window_height // 2 - 40,
            )
        )

        self.enter = self.font.render(
            "ENTER / SPACE — Start", True, "#ffffff", "#006699"
        )
        self.enter_rect = self.enter.get_rect(
            center=(
                self.config.window_width // 2,
                self.config.window_height // 2 + 40,
            )
        )

        self.quit = self.font.render("ESC — Quit", True, "#ffffff", "#fa5252")
        self.quit_rect = self.quit.get_rect(
            center=(
                self.config.window_width // 2,
                self.config.window_height // 2 + 80,
            )
        )

    def handle_event(self, event: pygame.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.manager.switch("game")
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.enter_rect.collidepoint(
                    event.pos
                ):
                    self.manager.switch("game")
                elif event.button == 1 and self.quit_rect.collidepoint(
                    event.pos
                ):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill("lightskyblue")

        surf.blit(
            self.image, self.image.get_rect(center=surf.get_rect().center)
        )

        surf.blit(self.title, self.title_rect)

        surf.blit(self.enter, self.enter_rect)

        surf.blit(self.quit, self.quit_rect)
