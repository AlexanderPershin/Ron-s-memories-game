import pygame


class ScoreText(pygame.sprite.Sprite):
    def __init__(
        self,
        font: pygame.Font,
        color: str,
        topleft: tuple = (10, 10),
    ):
        super().__init__()

        self.font = font
        self.color = color
        self.topleft = topleft
        self.score = 0

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.topleft)

    def _render(self) -> None:
        self.image = self.font.render(
            f"Score: {self.score}",
            antialias=False,
            color=self.color,
        )
        self.rect = self.image.get_rect(topleft=self.topleft)

    def update(self, dt: float, *args, score=0, **kwargs):
        self.score = score
        self._render()


class Ui(pygame.sprite.Sprite):
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        font: pygame.font.Font,
        color: str,
    ):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.Surface(
            (screen_width, screen_height), pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.sprites = pygame.sprite.Group(
            ScoreText(font, color, topleft=(10, 10)),
        )

    def update(
        self,
        dt: float,
        *args,
        score: int = 0,
        **kwargs,
    ) -> None:
        self.sprites.update(
            dt,
            score=score,
        )

        self.image.fill("#00000000")

        self.sprites.draw(self.image)
