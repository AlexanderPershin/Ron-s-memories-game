import pygame


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        image: pygame.Surface,
        speed: int,
    ):
        super().__init__()

        self.original_image = image.copy()
        self.image = image

        self.pos = pos

        self.rect = self.image.get_rect(center=pos)

        self.invulnarable_image = pygame.Surface(
            (120, 120), flags=pygame.SRCALPHA
        )
        shield_surface = pygame.Surface((120, 120), flags=pygame.SRCALPHA)
        pygame.draw.circle(
            shield_surface,
            "#00669955",
            (60, 60),
            50,
        )

        self.invulnarable_image.blit(shield_surface, (0, 0))
        self.invulnarable_image.blit(
            self.original_image,
            self.original_image.get_rect(
                center=self.invulnarable_image.get_rect().center
            ),
        )

        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed

        self.invulnarability_timer = 2  # 2 seconds can't be damaged

    @property
    def is_invulnarable(self) -> bool:
        return self.invulnarability_timer > 0

    def _stay_in_world(self, screen_rect: pygame.Rect) -> None:
        self.pos.x = max(screen_rect.left, min(self.pos.x, screen_rect.right))
        self.pos.y = max(screen_rect.top, min(self.pos.y, screen_rect.bottom))

    def update(self, dt: float, *args, screen_rect: pygame.Rect, **kwargs):
        self.invulnarability_timer -= dt

        keys = pygame.key.get_pressed()

        move = pygame.Vector2()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1

        if move.length_squared() > 0:
            move.normalize_ip()

        self.pos += move * self.speed * dt

        self._stay_in_world(screen_rect)

        if self.is_invulnarable:
            self.image = self.invulnarable_image
        else:
            self.image = self.original_image

        self.rect.center = self.pos
