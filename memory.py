import random

import pygame


class Memory(pygame.sprite.Sprite):
    def __init__(
        self, image: pygame.Surface, window_width: int, window_height: int
    ):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect(
            center=(
                random.randint(30, window_width - 30),
                random.randint(30, window_height - 30),
            )
        )

        self.mask = pygame.mask.from_surface(self.image)
