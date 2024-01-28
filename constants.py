COLOURS = {
    "WHITE" : (255, 255, 255),
    "BLACK" : (0, 0, 0),
    "GREY" : (100, 100, 100),
    "LGREEN" : (154, 230, 127),
    "DGREEN" : (116, 212, 81),
    "BKGD" : (45, 154, 6),
    "BROWN" : (229, 194, 159),
    "RED" : (200, 40, 5)
}

BUTTON_DATA = {
    'easy' : {
        'vars' : ('Easy', 'e'),
        'pos' : (30, 300)
    },
    'medium' : {
        'vars' : ('Medium', 'm'),
        'pos' : (180, 300)
    },
    'hard' : {
        'vars': ('Hard', 'h'),
        'pos' : (330, 300)
    }
}

GAME_DATA = {
    'e' : {
        'rows' : 8,
        'columns' : 10,
        'mines' : 10,
        'scale' : 50
    },
    'm' : {
        'rows' : 14,
        'columns' : 18,
        'mines' : 40,
        'scale' : 40
    },
    'h' : {
        'rows' : 20,
        'columns' : 24,
        'mines' : 99,
        'scale' : 30
    },
}