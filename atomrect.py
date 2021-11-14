import pygame


class AtomRect:

    def __init__(self, rect: pygame.Rect, atom):
        self.rect = rect
        self.atom = atom
        self.bg = (255, 255, 255)
        self.found = False

    def set_found(self):
        self.found = True

    def change_bg(self):
        self.bg = (0, 255, 0)

    def get_symbol(self):
        return str(self.atom.symbol)

    def get_atomic_number(self):
        return str(self.atom.atomic_number)

