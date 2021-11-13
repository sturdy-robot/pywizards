import sys
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class Level:
    def __init__(self, window, level_data):
        self.window = window
        self.tile_size = 64
        self.level_data = level_data
        self.world_shift = 0
        self.world_shift_speed = 0
        self.setup()
        self.player_sprite = None
        self.tiles = None

    def setup(self):
        map_data = self.read_map_data(self.level_data)
        self.tiles = pygame.sprite.Group()

        for i, row in enumerate(map_data):
            for j, cell in enumerate(row):
                x = j * self.tile_size
                y = i * self.tile_size
                if cell == 'X':
                    tile = Tile((x, y), self.tile_size, (0, 204, 102))
                    self.tiles.add(tile)
                elif cell == 'P':
                    player = Player((x, y))
                    self.player_sprite = pygame.sprite.GroupSingle(player)

    @staticmethod
    def read_map_data(level_data):
        with open(level_data, 'r', encoding='utf-8') as fp:
            return fp.read().splitlines()

    def update(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.window)
        self.player_sprite.update()
        self.player_sprite.draw(self.window)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((102, 0, 204))
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = 1
        self.gravity = 1
        self.jump_speed = -1

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.player_speed


def setup_pygame():
    pygame.init()
    window = pygame.display.set_mode((800, 600), pygame.SCALED)
    pygame.display.set_caption("PyWizards")
    return window


def draw(window, level: Level):
    window.fill((255, 255, 255))
    level.update()
    pygame.display.update()


def main():
    window = setup_pygame()
    running = True
    level = Level(window, 'level_data.txt')
    level.setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        draw(window, level)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
