from pygame import display, event, font, sprite, mouse, time, quit, init, QUIT, MOUSEBUTTONDOWN
from constants import COLOURS, BUTTON_DATA, GAME_DATA
from button import Button
from tile import Tile
from itertools import cycle
from random import randint

class Minesweeper:
    def __init__(self) -> None:
        init()
        self.my_clock = time.Clock()

    def check_button_click(self, buttons, pos):
        for button in buttons:
            if button.rect.collidepoint(pos):
                return button.my_value
        return "set mode"
    
    def make_buttons(self):
        button_group = sprite.Group()
        for data in BUTTON_DATA:
            vars = BUTTON_DATA[data]['vars']
            pos = BUTTON_DATA[data]['pos']
            button_group.add(Button(vars, pos))
        return button_group

    def open_screen(self, window):
        window.fill(COLOURS['LGREEN'])
        txt_font = font.SysFont('arial' , 80)
        option_text = txt_font.render(str("PICK  A"), True, (COLOURS['BLACK']))
        window.blit(option_text, (110, 10))
        option_text = txt_font.render(str("PICK  A"), True, (COLOURS['GREY']))
        window.blit(option_text, (115, 5))
        option_text = txt_font.render(str("GAMEMODE"), True, (COLOURS['BLACK']))
        window.blit(option_text, (5, 100))
        option_text = txt_font.render(str("GAMEMODE"), True, (COLOURS['GREY']))
        window.blit(option_text, (10, 95))

    def set_up(self):
        self.score = 0
        self.timer = 0
        window = display.set_mode((500, 400))
        self.open_screen(window)
        buttons = self.make_buttons()
        buttons.draw(window)
        display.update()
        game_mode = 'set mode'
        while game_mode == 'set mode':
            for my_event in event.get():
                if my_event.type == QUIT:
                    quit()
                    raise SystemExit
                elif my_event.type == MOUSEBUTTONDOWN:
                    game_mode = self.check_button_click(
                        buttons, 
                        mouse.get_pos()
                    )
        return GAME_DATA[game_mode]

    def game_window(self, vars):
        Width = int(vars['columns'] * vars['scale'])
        height = int(vars['rows'] * vars['scale'] 
                     + vars['scale'] * 1.5)
        screen = display.set_mode((Width, height))
        screen.fill(COLOURS['BKGD'])
        return screen

    def make_tiles(self, vars):
        tile_grid = []
        tile_colour = (COLOURS['LGREEN'], COLOURS['DGREEN'])
        tile_colours = cycle(tile_colour)
        for i in range (0, vars['rows']):
            cols = []
            for j in range (0, vars['columns']):
                tile_x = j * vars['scale']
                tile_y = i * vars['scale'] + vars['scale'] * 1.5
                colour = next(tile_colours)
                cols.append(Tile(
                    (tile_x, tile_y), 
                    vars['scale'], 
                    colour)
                )
            next(tile_colours)
            tile_grid.append(cols)
        return tile_grid

    def update_screen(self, screen, tiles, scale):
        screen.fill(COLOURS['BKGD'])
        txt_font = font.SysFont('arial' , scale)
        option_text = txt_font.render(
            str(self.score), 
            True, 
            (COLOURS['BLACK'])
        )
        screen.blit(
            option_text, 
            (scale * 1.2, scale * 0.45)
        )
        timer_txt = round(self.timer, 1)
        option_text = txt_font.render(
            str(timer_txt), 
            True, 
            (COLOURS['BLACK'])
        )
        screen.blit(
            option_text, 
            (scale * 5.2, scale * 0.45)
        )
        for row in tiles:
            for tile in row:
                screen.blit(tile.image, tile.pos)
        display.update()

    def add_mines(self, tiles, vars):
        mines = vars['mines']
        rows = vars['rows']
        cols = vars['columns']
        for _ in range (mines):
            x = randint(0, cols - 1)
            y = randint(0, rows - 1)
            while tiles[y][x].is_mine:
                x = randint(0, cols - 1)
                y = randint(0, rows - 1)
            tiles[y][x].is_mine = True
        return tiles

    def check_tile_click(self, tiles, pos, mouse_presses):
        self.is_checked = []
        for i, row in enumerate(tiles):
            for j in range(len(row)):
                if tiles[i][j].rect.collidepoint(pos):
                    self.score = tiles[i][j].on_click(mouse_presses, self.score)
                    if not tiles[i][j].is_mine and tiles[i][j].surrounding == 0:
                        tiles = self.clear_empty(tiles, i, j, mouse_presses)
        return tiles

    def clear_empty(self, tiles, i, j, mouse_presses):
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0:
                    pass
                else:
                    try:
                        if (tiles[i + y][j + x].surrounding == 0 and 
                            not tiles[i + y][j + x] in self.is_checked
                            ):
                            tiles[i + y][j + x].on_click(mouse_presses, self.score)
                            self.is_checked.append(tiles[i + y][j + x])
                            tiles = self.clear_empty(tiles, i + y, j + x, mouse_presses)
                    except:
                        pass
        return tiles

    def game_over(self, bkgd, txt):
        width = 500
        height = 400
        window = display.set_mode((width, height))
        window.fill(bkgd)
        txt_font = font.SysFont('arial' , int(width // 3.5))
        option_text = txt_font.render(
            str("YOU"), 
            True, 
            (COLOURS['BLACK'])
        )
        window.blit(option_text, (width // 6, height // 12))
        option_text = txt_font.render(
            str(txt), 
            True, 
            (COLOURS['BLACK'])
        )
        window.blit(option_text, (width // 8, height // 2))
        option_text = txt_font.render(
            str("YOU"), 
            True, 
            (COLOURS['GREY'])
        )
        window.blit(option_text, (width // 5.5, height // 12))
        option_text = txt_font.render(
            str(txt), 
            True, 
            (COLOURS['GREY'])
        )
        window.blit(option_text, (width // 7.2, height // 2))
        display.update()
        while True:
            for my_event in event.get():
                if my_event.type == QUIT:
                    quit()
                    raise SystemExit
                elif my_event.type == MOUSEBUTTONDOWN:
                    self.run()

    def check_win(self, tiles):
        checked = True
        for row in tiles:
            for tile in row:
                if tile.is_mine and not tile.is_clicked:
                    checked = False
        return checked
    
    def check_touching_mines(self, tiles):
        for i, row in enumerate(tiles):
            for j in range(len(row)):
                if not tiles[i][j].is_mine:
                    tiles[i][j].surrounding = self.check_surrounding(i, j, tiles)
        return tiles

    def check_surrounding(self, i, j, tiles):
        surrounding = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0:
                    pass
                else:
                    try:
                        if tiles[i + y][j + x].is_mine:
                            surrounding += 1
                    except:
                        pass
        return surrounding
        self.my_clock = time.Clock()
    
    def run(self):
        game_vars = self.set_up()
        window = self.game_window(game_vars)
        tiles = self.make_tiles(game_vars)
        tiles = self.add_mines(tiles, game_vars)
        tiles = self.check_touching_mines(tiles)
        while True:
            for my_event in event.get():
                if my_event.type == QUIT:
                    quit()
                    raise SystemExit
                elif my_event.type == MOUSEBUTTONDOWN:
                    tiles = self.check_tile_click(
                        tiles, 
                        mouse.get_pos(), 
                        mouse.get_pressed())
                    if self.score == -1:
                        self.game_over(COLOURS['RED'], "LOSE")
                    elif (self.score == game_vars['mines'] 
                        and self.check_win(tiles)
                        ):
                        self.game_over(COLOURS['BKGD'], "WIN")
            self.update_screen(window, tiles, game_vars['scale'])
            self.timer += 0.1
            self.my_clock.tick(10)

if __name__ == '__main__':
    my_game = Minesweeper()
    my_game.run()
