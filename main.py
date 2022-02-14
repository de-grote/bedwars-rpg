import pygame
import os.path as path
from functools import cache
from math import floor
from stages import Stages


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
        self.occupied: set[tuple[int, int]] = set()
        self.platforms: set[Platform] = set()
        self.load_scene(0)
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
        # TEMP
        if self.keys[pygame.K_q]:
            self.load_scene(0)
        return

    def render(self) -> None:
        self.screen.fill((0, 200, 255))
        self.screen.blit(*self.player.render())
        for p in self.platforms:
            self.screen.blit(*p.render(self.scale, (self.cam.x, self.cam.y)))
        pygame.display.update()
        return

    def place_block(self, pos: tuple[int, int]) -> None:
        x = floor(pos[0] / (self.scale * 16) - self.cam.x / 16)
        y = floor(pos[1] / (self.scale * 16) - self.cam.y / 16)
        if (x, y) in self.occupied:
            return
        if (x + 1, y) in self.occupied or (x - 1, y) in self.occupied \
                or (x, y + 1) in self.occupied or (x, y - 1) in self.occupied:
            if self.player.x + self.player.width <= x * 16 or x * 16 + 16 <= self.player.x or \
                    self.player.y + self.player.height <= y * 16 or y * 16 + 16 <= self.player.y:
                self.occupied.add((x, y))
                self.platforms.add(Platform("bedrock.png", (x * 16, y * 16), (16, 16)))

    def load_scene(self, scene_number: int):
        self.occupied.clear()
        self.platforms.clear()
        scene: dict = Stages.stages[scene_number]
        self.platforms.update(Platform(*s) for s in scene["platforms"])
        self.occupied.update(scene["occupied"])
        self.player.pos = scene["player"]
        self.cam.all = scene["cam"]


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
        if self.x + self.game.cam.x < 0 or self.y + self.game.cam.y < 0 or \
                self.x + self.width + self.game.cam.x > self.game.screen_x or \
                self.y + self.height + self.game.cam.y > self.game.screen_y:
            return True
        for p in self.game.platforms:
            if self.y + self.height > p.top and self.y < p.bottom and self.x + self.width > p.left and self.x < p.right:
                return True
        return False

    def render(self) -> tuple[pygame.Surface, tuple[int, int]]:
        return self.sprite, ((self.x + self.game.cam.x) * self.game.scale, (self.y + self.game.cam.y) * self.game.scale)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos: dict[str: int]):
        self.x = pos["x"]
        self.y = pos["y"]


class Cam:
    def __init__(self, game):
        self.game: Game = game
        self._x: int = 0
        self._y: int = 0
        self.max_x: int | None = None
        self.min_x: int | None = None
        self.max_y: int | None = None
        self.min_y: int | None = None

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

    @property
    def all(self) -> tuple[int, int, int | None, int | None, int | None, int | None]:
        return self._x, self._y, self.max_x, self.min_x, self.max_y, self.min_y

    @all.setter
    def all(self, info) -> None:
        self._x = info["x"]
        self._y = info["y"]
        self.max_x = info["max_x"]
        self.min_x = info["min_x"]
        self.max_y = info["max_y"]
        self.min_y = info["min_y"]


class Platform:
    scale: int = 1

    def __init__(self, sprite, pos: tuple[int, int], size: tuple[int, int]):
        self.sprite = load_image(sprite, (size[0] * self.scale, size[1] * self.scale))
        self.x, self.y = pos
        self.width, self.height = size

    def render(self, scale: int, offset: tuple[int, int]) -> tuple[pygame.Surface, tuple[int, int]]:
        return self.sprite, ((self.x + offset[0]) * scale, (self.y + offset[1]) * scale)

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
