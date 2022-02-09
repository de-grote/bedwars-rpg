import pygame
import os.path as path
from functools import cache


class Game:
    def __init__(self):
        pygame.display.set_caption("Bedwars RPG")
        pygame.display.set_icon(load_image("player.png", (32, 32)))
        self.scale = 6
        Platform.scale = self.scale
        self.screen_x = 256
        self.screen_y = 144
        self.screen = pygame.display.set_mode((self.screen_x * self.scale, self.screen_y * self.scale))
        self.clock = pygame.time.Clock()
        self.player: Player = Player(self)
        self.cam: Cam = Cam(self)
        self.keys: list[bool] = []
        self.platforms: list[Platform] = [
            Platform("bedrock.png", (144, 128), (16, 16)),
            Platform("bedrock.png", (128, 112), (16, 16)),
            Platform("bedrock.png", (96, 128), (16, 16)),
            Platform("bedrock.png", (112, 112), (16, 16)),
            Platform("bed.png", (112, 135), (32, 9)),
        ]
        self.loop()

    def loop(self):
        while True:
            self.input()
            self.player.update(self.keys)
            self.render()
            self.clock.tick(30)

    def input(self) -> None:
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit("Thanks for playing!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.place_block(event.pos)
        return

    def render(self) -> None:
        self.screen.fill((0, 200, 255))
        self.player.render()
        for p in self.platforms:
            p.render(self.screen, self.scale, (self.cam.x, self.cam.y))
        pygame.display.update()
        return

    def place_block(self, pos: tuple[int, int]) -> None:
        self.platforms.append(Platform("bedrock.png", (
            (pos[0] / (self.scale * 16) - self.cam.x / 16).__floor__() * 16,
            (pos[1] / (self.scale * 16) - self.cam.y / 16).__floor__() * 16
            ), (16, 16)))


class Player:
    def __init__(self, game):
        self.game: Game = game
        self.width: int = 16
        self.height: int = 32
        self.sprite = load_image("player.png", (self.width * self.game.scale, self.height * self.game.scale))
        self.x: int = 0
        self.y: int = 0
        self.vx: int = 0
        self.vy: int = 0
        self.speed: int = 4
        self.jump_height: int = 7
        self.gravity: int = 1
        self.grounded: bool = False
        self.sneaking: bool = False

    def update(self, keys):
        self.walk(keys)

    def walk(self, keys) -> None:
        self.vx = 0
        if keys[pygame.K_LSHIFT]:
            self.speed = 1
            self.sneaking = True
        elif keys[pygame.K_LCTRL]:
            self.speed = 4
            self.sneaking = False
        else:
            self.speed = 2
            self.sneaking = False
        if keys[pygame.K_a]:
            self.vx -= self.speed
        elif keys[pygame.K_d]:
            self.vx += self.speed
        if self.grounded and keys[pygame.K_SPACE]:
            self.vy -= self.jump_height
        self.vy += self.gravity
        self.move()

    def move(self) -> None:
        if self.x + self.game.cam.x <= 32:
            self.game.cam.x += self.speed
        elif self.x + self.game.cam.x >= 208:
            self.game.cam.x -= self.speed
        if self.y + self.game.cam.y <= 32:
            self.game.cam.y += abs(self.vy)
        elif self.y + self.game.cam.y >= 96:
            self.game.cam.y -= abs(self.vy)
        if self.grounded and self.sneaking:
            self.y += 1
            if self.vx > 0:
                self.x += 1
                if not self.collision():
                    self.x -= 1
                self.x -= 1
            elif self.vx < 0:
                self.x -= 1
                if not self.collision():
                    self.x += 1
                self.x += 1
            self.y -= 1
        self.y += self.vy
        if self.collision():
            if self.vy > 0:
                self.grounded = True
                while self.collision():
                    self.y -= 1
            else:
                while self.collision():
                    self.y += 1
            self.vy = 0
        else:
            self.grounded = False
        self.x += self.vx
        if self.collision():
            if self.vx > 0:
                while self.collision():
                    self.x -= 1
            else:
                while self.collision():
                    self.x += 1

    def collision(self) -> bool:
        if self.x + self.game.cam.x < 0 or self.y + self.game.cam.y < 0 or self.x + self.width + self.game.cam.x > self.game.screen_x or self.y + self.height + self.game.cam.y > self.game.screen_y:
            return True
        for p in self.game.platforms:
            if self.y + self.height > p.top and self.y < p.bottom and self.x + self.width > p.left and self.x < p.right:
                return True
        return False

    def render(self):
        self.game.screen.blit(self.sprite, ((self.x + self.game.cam.x) * self.game.scale, (self.y + self.game.cam.y) * self.game.scale))


class Cam:
    def __init__(self, game):
        self.game: Game = game
        self._x: int = 0
        self._y: int = 0
        self.max_x: int | None = None
        self.min_x: int | None = None
        self.max_y: int | None = None
        self.min_y: int | None = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x
        if self.max_x is not None and self._x > self.max_x:
            self._x = self.max_x
        if self.min_x is not None and self._x < self.min_x:
            self._x = self.min_x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        self._y = y
        if self.max_y is not None and self._y > self.max_y:
            self._y = self.max_y
        if self.min_y is not None and self._y < self.min_y:
            self._y = self.min_y


class Platform:
    scale: int = 1

    def __init__(self, sprite, pos: tuple[int, int], size: tuple[int, int]):
        self.sprite = load_image(sprite, (size[0] * self.scale, size[1] * self.scale))
        self.x, self.y = pos
        self.width, self.height = size

    def render(self, screen, scale: int, offset: tuple[int, int]):
        screen.blit(self.sprite, ((self.x + offset[0]) * scale, (self.y + offset[1]) * scale))

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width


@cache
def load_image(name: str, *args) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path.join("assets", name)), *args)


if __name__ == "__main__":
    pygame.init()
    Game()
