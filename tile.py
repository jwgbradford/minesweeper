from pygame import sprite, Surface, draw, font
from constants import COLOURS

class Tile(sprite.Sprite):
    def __init__(self, pos, size, colour) -> None:
        super().__init__()
        self.pos = pos
        self.size = size
        self.image = self.make_tile_image(size, colour)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.is_mine = False
        self.is_clicked = False
        self.surrounding = 0

    def make_tile_image(self, size, colour):
        tile = Surface((size, size))
        tile.fill(colour)
        return tile
    
    def on_click(self, mouse_presses, score):
        if self.is_mine:
            score = self.found_mine(mouse_presses, score)
        elif not self.is_mine:
            score = self.not_a_mine(mouse_presses, score)
        return score

    def found_mine(self, mouse_presses, score):
        if mouse_presses[0]:
            self.image.fill(COLOURS['RED'])
            score = -1
        elif mouse_presses[2]:
            self.draw_flag()
            score += 1
            self.is_clicked = True
        return score

    def not_a_mine(self, mouse_presses, score):
        if mouse_presses[0]:
            self.image.fill(COLOURS['BROWN'])
            my_font = font.SysFont('arial' , self.size)
            option_text = my_font.render(
                str(self.surrounding), 
                True, 
                (COLOURS['BKGD'])
            )
            self.image.blit(
                option_text, 
                option_text.get_rect(
                    center = self.image.get_rect().center
                )
            )
            if self.is_clicked:
                score -= 1
                self.is_clicked = False
        elif mouse_presses[2]:
            self.draw_flag()
            self.is_clicked = True
            score += 1
        return score

    def draw_flag(self):
        draw.polygon(
            self.image, 
            COLOURS['RED'],
            [
                [self.size * 0.1, self.size * 0.1], 
                [self.size * 0.8, self.size * 0.35], 
                [self.size * 0.1, self.size * 0.5]
            ],
            0
        )
        draw.line(
            self.image, 
            COLOURS['RED'],
            (self.size * 0.1, self.size * 0.5),
            (self.size * 0.1, self.size * 0.9),
            2
        )


