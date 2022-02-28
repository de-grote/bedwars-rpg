import pygame
import os.path as path
import json
from functools import cache
from math import floor
from itertools import combinations


class Game:
    def __init__(self):
        pygame.display.set_caption("Bedwars RPG")
        pygame.display.set_icon(load_image("logo.png", (32, 32)))
        self.scale = 6
        Platform.scale = self.scale
        self.screen_x = 256
        self.screen_y = 144
        self.screen = pygame.display.set_mode((self.screen_x * self.scale, self.screen_y * self.scale))
        self.clock = pygame.time.Clock()
        self.player: Player = Player(self)
        self.cam: Cam = Cam(self)
        self.keys: list[bool] = []
        self.keys_down: set[int] = set()
        self.occupied: set[tuple[int, int]] = set()
        self.platforms: set[Platform] = set()
        self.creative = False
        with open("stages.json", "r") as f:
            self.stages = json.load(f)
        with open("controls.json", "r") as f:
            self.controls = json.load(f)
        self.load_scene("test_stage")
        self.loop()

    def loop(self):
        while True:
            self.input()
            self.player.update()
            self.render()
            self.clock.tick(30)

    def input(self) -> None:
        self.keys = pygame.key.get_pressed()
        self.keys_down.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit("Thanks for playing!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.place_block(event.pos)
                elif event.button == 1:
                    self.break_block(event.pos)
            # TEMP
            if event.type == pygame.KEYDOWN:
                self.keys_down.add(event.key)
        if pygame.K_q in self.keys_down:
            self.load_scene("test_stage")
        elif pygame.K_e in self.keys_down:
            self.switch_mode()
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
        if ((x + 1, y) in self.occupied or (x - 1, y) in self.occupied or
            (x, y + 1) in self.occupied or (x, y - 1) in self.occupied or self.creative) and \
            (self.player.x + self.player.width <= x * 16 or x * 16 + 16 <= self.player.x or
             self.player.y + self.player.height <= y * 16 or y * 16 + 16 <= self.player.y):
            self.occupied.add((x, y))
            self.platforms.add(Platform("bedrock.png", (x * 16, y * 16), (16, 16)))

    def load_scene(self, scene_number: str) -> None:
        self.occupied.clear()
        self.platforms.clear()
        scene: dict = self.stages[scene_number]
        self.platforms.update(Platform(*s) for s in scene["platforms"])
        self.occupied.update(tuple(o) for o in scene["occupied"])
        self.player.set(scene["player"])
        self.cam.set(scene["cam"])

    def break_block(self, pos: tuple[int, int]) -> None:
        x = pos[0] / self.scale - self.cam.x
        y = pos[1] / self.scale - self.cam.y
        for platform in self.platforms:
            if platform.x <= x <= platform.x + platform.width and platform.y <= y <= platform.y + platform.height:
                self.platforms.remove(platform)
                for i in combinations((*range(platform.x // 16, (platform.x + platform.width) // 16),
                                       *range(platform.y // 16, (platform.y + platform.height) // 16)), 2):
                    self.occupied.discard(i)
                return

    def switch_mode(self) -> None:
        self.creative = not self.creative
        self.player.switch_mode()


class Player:
    def __init__(self, game):
        self.game: Game = game
        self.width: int = 16
        self.height: int = 32
        self.sprite: dict[str: pygame.Surface] = {
            "idle": load_image("player.png", (self.width * self.game.scale, self.height * self.game.scale)),
            "idle_c": load_image("creative.png", (self.width * self.game.scale, self.height * self.game.scale))
        }
        self.status: str = "idle"
        self.x: int = 0
        self.y: int = 0
        self.vx: int = 0
        self.vy: int = 0
        self.speed: int = 4
        self.jump_height: int = 7
        self.gravity: int = 1
        self.grounded: bool = False
        self.sneaking: bool = False
        self.flying: bool = False
        self.creative: bool = False

    def update(self):
        self.walk()

    def walk(self) -> None:
        self.vx = 0
        if self.game.keys[pygame.__getattribute__("K_" + self.game.controls["up"])]:
            if self.flying:
                self.vy = -self.speed
        elif self.game.keys[pygame.__getattribute__("K_" + self.game.controls["down"])]:
            if self.flying:
                self.vy = self.speed
        else:
            if self.flying:
                self.vy = 0
        if self.game.keys[pygame.__getattribute__("K_" + self.game.controls["sneak"])]:
            self.speed = 1
            self.sneaking = True
        elif self.game.keys[pygame.__getattribute__("K_" + self.game.controls["sprint"])]:
            self.speed = 4
            self.sneaking = False
        else:
            self.speed = 2
            self.sneaking = False
        if self.game.keys[pygame.__getattribute__("K_" + self.game.controls["left"])]:
            self.vx -= self.speed
        elif self.game.keys[pygame.__getattribute__("K_" + self.game.controls["right"])]:
            self.vx += self.speed
        if self.grounded and self.game.keys[pygame.__getattribute__("K_" + self.game.controls["jump"])]:
            self.vy -= self.jump_height
        elif self.creative and not self.grounded and\
                pygame.__getattribute__("K_" + self.game.controls["jump"]) in self.game.keys_down:
            self.flying = not self.flying
            self.vy = 0
        if not self.flying:
            self.vy += self.gravity
        self.move()

    def move(self) -> None:
        if self.x + self.game.cam.x <= 32:
            self.game.cam.x += self.speed
        elif self.x + self.game.cam.x >= 208:
            self.game.cam.x -= self.speed
        if self.y + self.game.cam.y <= 48:
            self.game.cam.y += abs(self.vy)
        elif self.y + self.game.cam.y >= 80:
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
        return self.sprite[self.status + ("_c" if self.game.creative else "")], \
               ((self.x + self.game.cam.x) * self.game.scale, (self.y + self.game.cam.y) * self.game.scale)

    def set(self, pos: dict[str: int]) -> None:
        self.x = pos["x"]
        self.y = pos["y"]

    def switch_mode(self) -> None:
        self.creative = not self.creative
        if not self.creative:
            self.flying = False


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

    def set(self, info: dict) -> None:
        self._x = info["x"]
        self._y = info["y"]
        self.max_x = info["max_x"]
        self.min_x = info["min_x"]
        self.max_y = info["max_y"]
        self.min_y = info["min_y"]


class Platform:
    scale: int = 1

    def __init__(self, sprite, pos: tuple[int, int], size: tuple[int, int], break_time: int | None = None):
        self.sprite = load_image(sprite, (size[0] * self.scale, size[1] * self.scale))
        self.x, self.y = pos
        self.width, self.height = size
        self.break_time: int = break_time

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
