import numpy as np
import random
import time
import pygame
import sys
pygame.init()

# Constants
WIDTH = 450
HEIGHT = 450
CELL_SIZE = WIDTH // 9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

def board_print(board):
    """
    Prints 9x9 numpy array input board in an easier to read format.
    """

    # Some basic checks
    assert board.shape == (9, 9)
    assert type(board) == np.ndarray

    # Convert array elements to strings
    board_str = board.astype(str)

    # Our row separator
    row_sep = '-' * 25

    # Loop through 9 rows
    for i in range(9):

        # At each multiple of 3, print row separator
        if i % 3 == 0:
            print(row_sep)

        # Get row data
        row = board_str[i]

        # Format row of data with pipe separators at each end, and between each sub grid
        print('| ' + ' '.join(row[0:3]) + ' | ' + ' '.join(row[3:6]) + ' | ' + ' '.join(row[6:]) + ' |')

    # Print final row separator at bottom after loops finish
    print(row_sep)

def is_valid(sudoku, row, col, num):
    if num in list(sudoku[row]):
        return False
    if num in list(sudoku[:, col]):
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if sudoku[i][j] == num:
                return False
    return True

def find_empty(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                return (row, col)
    return None

def solve_sudoku(sudoku):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    empty_cell = find_empty(sudoku)
    if not empty_cell:
        return True

    row, col = empty_cell
    for num in range(1, 10):
        sudoku[row][col] = num
        # draw_board()
        # pygame.display.flip()
        # time.sleep(0.001)
        sudoku[row][col] = 0
        if is_valid(sudoku, row, col, num):
            sudoku[row][col] = num
            # draw_board()
            # pygame.display.flip()
            if solve_sudoku(sudoku):
                return True
            sudoku[row][col] = 0
            # draw_board()
            # pygame.display.flip()
        draw_board()
        pygame.display.flip()
    return False

def find_empty_cell_constrained(board):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells

def solve_sudoku_constrained(sudoku):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    empty_cells = find_empty_cell_constrained(sudoku)
    if not empty_cells:
        return True
    empty_cells.sort(key=lambda cell: len(find_possible_options(sudoku, cell[0], cell[1])))

    for row, col in empty_cells:
        for num in find_possible_options(sudoku, row, col):
            sudoku[row][col] = num

            draw_board()
            pygame.display.flip()

            if solve_sudoku_constrained(sudoku):
                draw_board()
                pygame.display.flip()
                return True
            sudoku[row][col] = 0  # Backtrack
            draw_board()
            pygame.display.flip()

    return False


def find_possible_options(board, row, col):
    options = set(range(1, 10))
    for i in range(9):
        options.discard(board[row][i])
        options.discard(board[i][col])
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            options.discard(board[i][j])
    return options

def draw_board():
    screen.fill(WHITE)
    for i in range(9):
        for j in range(9):
            if problem[i][j] != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(problem[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw grid lines
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        else:
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
def show_popup():
    font = pygame.font.Font(None, 32)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_text("SOLVED", font, BLACK, WIDTH // 2, 50)


        pygame.display.flip()


problem = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

# Main game loop
solved = False
running = True
constrained = True
while running:
    time.sleep(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not solved:
        if constrained:
            solved = solve_sudoku_constrained(problem)
        else:
            solved = solve_sudoku(problem)
        if solved:
            show_popup()

    draw_board()  # Draw the Sudoku board
    pygame.display.flip()  # Update the display

# Quit Pygame
pygame.quit()
sys.exit()