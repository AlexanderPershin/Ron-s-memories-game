import pygame


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        image: pygame.Surface,
        speed: int,
    ):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect(center=pos)

        self.speed = speed

        self.max_hp = 100
        self.hp = 100

    def _stay_in_world(self, screen_rect: pygame.Rect) -> None:
        self.rect.centerx = max(
            screen_rect.left, min(self.rect.centerx, screen_rect.right)
        )
        self.rect.centery = max(
            screen_rect.top, min(self.rect.centery, screen_rect.bottom)
        )

    def update(self, dt: float, *args, screen_rect: pygame.Rect, **kwargs):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

        self._stay_in_world(screen_rect)
