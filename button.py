from pygame import sprite, Surface, draw, Rect, font
from constants import COLOURS

class Button(sprite.Sprite):
    def __init__(self, vars, pos) -> None:
        super().__init__()
        txt, val = vars
        self.image = self.make_button_image(txt)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.my_value = val

    def make_button_image(self, msg):
        button = Surface((120, 55))
        draw.rect(button, COLOURS['BLACK'],
                        Rect(0, 5, 115, 50),
                        0)
        draw.rect(button, COLOURS['GREY'],
                        Rect(5, 0, 120, 50),
                        0)
        button_font = font.SysFont('arial' , 30)
        option_text = button_font.render(
            str(msg), 
            True, 
            (COLOURS['BKGD'])
        )
        button_center = button.get_rect().center
        button.blit(option_text, option_text.get_rect(center = button_center))
        return button

    def on_click(self):
        return self.my_value