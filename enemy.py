import random

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        player: pygame.sprite.Sprite,
        window_width: int,
        window_height: int,
        speed_range: tuple[int, int],
    ):
        super().__init__()

        self.window_width = window_width
        self.window_height = window_height
        self.image = image

        for _ in range(50):
            self.rect = self.image.get_rect(
                center=(
                    random.randint(50, self.window_width - 50),
                    random.randint(50, self.window_height - 50),
                )
            )
            if not player.rect.colliderect(self.rect):
                break
        else:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.Vector2(self.rect.center)

        direction = pygame.Vector2(
            random.choice([-1, 1]),
            random.choice([-1, 1]),
        ).normalize()

        speed = random.uniform(*speed_range)

        self.velocity = direction * speed

    def update(self, dt: float, *args, **kwargs) -> None:
        self.pos += self.velocity * dt
        self.rect.center = self.pos

        if self.rect.left < 0 or self.rect.right > self.window_width:
            self.velocity.x *= -1

        if self.rect.top < 0 or self.rect.bottom > self.window_height:
            self.velocity.y *= -1
