import csv
import random

from atom import Atom
from atomrect import AtomRect
import pygame

BACKGROUND = (0, 0, 0)
SQUARE_WIDTH = 64
FONT = 'Comic Sans'

screen = pygame.display.set_mode((1152, 800))
pygame.display.set_caption("Periodic Table Quiz")
screen.fill(BACKGROUND)
pygame.display.flip()


def create_atoms():
    atoms = []
    with open('periodictable.csv', 'r') as csvfile:
        atomic_data = csv.DictReader(csvfile)
        for atom in atomic_data:
            atoms.append(Atom(int(atom["AtomicNumber"]), float(atom["AtomicMass"]), atom["Symbol"]))
    return atoms


def create_layout():
    p_table = [[1] + [0] * 16 + [1], [1] * 2 + [0] * 10 + [1] * 6, [1] * 2 + [0] * 10 + [1] * 6, [1] * 18, [1] * 18,
               [1] * 18, [1] * 18, [0] * 2 + [1] * 14 + [0] * 2, [0] * 2 + [1] * 14 + [0] * 2]
    return p_table


def create_atomrects(atoms):
    atomrecs = []
    w = SQUARE_WIDTH
    p_table = create_layout()
    atom_num = 0
    for i in range(len(p_table)):
        for j in range(len(p_table[i])):
            if p_table[i][j] == 1:
                if atom_num == 57:
                    atom_num = 71

                elif atom_num == 89:
                    atom_num = 103

                elif atom_num == 118:
                    atom_num = 57

                elif atom_num == 71:
                    atom_num = 89

                atomrecs.append(AtomRect(pygame.Rect((j * w, i * w), (w, w)), atoms[atom_num]))
                atom_num += 1
    return atomrecs


def start_game():
    pygame.init()
    atoms = create_atoms()
    unfound_atoms = atoms.copy()
    rects = create_atomrects(atoms)
    num_font = pygame.font.SysFont(FONT, 18)
    sym_font = pygame.font.SysFont(FONT, 28)
    big_num_font = pygame.font.SysFont(FONT, 28)
    big_sym_font = pygame.font.SysFont(FONT, 40)
    question_font = pygame.font.SysFont(FONT, 30)
    question_square = pygame.Rect(((screen.get_width()/2)-50, 650), (100, 100))

    current_atom = random.choice(unfound_atoms)
    click = False
    wrong_atom_clicked = False
    wrong_attempts = 0

    running = True

    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        render_question_square(big_num_font, big_sym_font, question_square, current_atom, wrong_attempts)
        render_question(question_font, question_square)

        mx, my = pygame.mouse.get_pos()

        for r in rects:
            if r.rect.collidepoint((mx, my)) and not r.found:
                pygame.draw.rect(screen, (40, 40, 40), r.rect)
                if click:
                    if r.atom == current_atom:
                        wrong_attempts = 0
                        current_atom = correct_atom_clicked(current_atom, r, unfound_atoms)
                    else:
                        wrong_atom_clicked = True
                        wrong_attempts += 1
                        pygame.draw.rect(screen, (255, 0, 0), r.rect)
            else:
                render_atoms(r)

            render_atom_text(num_font, r, sym_font)

        click = False
        pygame.display.flip()
        if wrong_atom_clicked:
            pygame.time.delay(100)
            wrong_atom_clicked = False


def render_atom_text(num_font, r, sym_font):
    num = num_font.render(str(r.get_atomic_number()), True, (255, 255, 255))
    screen.blit(num, (r.rect.x + 2, r.rect.y))
    if r.found:
        sym = sym_font.render(str(r.get_symbol()), True, (255, 255, 255))
        screen.blit(sym, (r.rect.x + 18, r.rect.y + 30))


def render_atoms(r):
    if r.found:
        pygame.draw.rect(screen, r.bg, r.rect)
    else:
        pygame.draw.rect(screen, r.bg, r.rect, width=1)


def correct_atom_clicked(current_atom, r, unfound_atoms):
    r.set_found()
    r.change_bg()
    unfound_atoms.remove(current_atom)
    try:
        current_atom = random.choice(unfound_atoms)
    except IndexError:
        print("All elements found, now exiting")
        exit(0)
    return current_atom


def render_question_square(big_num_font, big_sym_font, question_square, atom, wrong_attempts):
    pygame.draw.rect(screen, (255, 255, 0), question_square)
    bsym = big_sym_font.render(str(atom.symbol), True, (0, 0, 0))
    screen.blit(bsym, (question_square.x + 30, question_square.y + 40))
    if wrong_attempts >= 3:
        bnum = big_num_font.render(str(atom.atomic_number), True, (0, 0, 0))
        screen.blit(bnum, (question_square.x + 2, question_square.y))


def render_question(question_font, question_square):
    question = question_font.render("Click where the element belongs", True, (255, 255, 0))
    screen.blit(question, (question_square.x - question.get_width() - 10, question_square.y + 25))


if __name__ == "__main__":
    start_game()
