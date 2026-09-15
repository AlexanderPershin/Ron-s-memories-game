import random

import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(
        self,
        window_width: int,
        window_height: int,
        image: pygame.Surface,
        player: pygame.sprite.Sprite,
        existing_rects: pygame.sprite.Group = None,
    ):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        existing_rects = existing_rects or pygame.sprite.Group()
        for _ in range(50):
            self.rect.topleft = (
                random.randint(20, window_width - self.rect.width - 20),
                random.randint(20, window_height - self.rect.height - 20),
            )
            if not pygame.sprite.spritecollide(
                self, existing_rects, False
            ) and not player.rect.colliderect(self.rect):
                break
        else:
            self.kill()
