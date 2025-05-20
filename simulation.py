import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 8
FPS = 60
CIRCLE_RADIUS = CELL_SIZE // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 150, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Tour")

# Knight image
knight_img = pygame.image.load("knight.png")  # Replace "knight.png" with your image file
knight_img = pygame.transform.scale(knight_img, (CELL_SIZE, CELL_SIZE))
# Font
font = pygame.font.Font(None, 30)
FONT_COLOR = (0,0,0)
# Function to draw the chessboard
def draw_board(visited_cells):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            if (col, row) in visited_cells:
                draw_visited_cell((col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),visited_cells.index((col, row)) + 1)

def draw_visited_cell(center , move_number):
    pygame.draw.circle(screen, RED, center, CIRCLE_RADIUS)
    # Display move number above the cell
    text = font.render(str(move_number), True, FONT_COLOR)
    text_rect = text.get_rect(center=(center[0], center[1] - CELL_SIZE // 4))
    screen.blit(text, text_rect)

# Function to draw the knight at a specific position
def draw_knight(position):
    screen.blit(knight_img, (position[0] * CELL_SIZE, position[1] * CELL_SIZE))

# Main loop
clock = pygame.time.Clock()
visited_cells = []  # Starting position is not visited

# List of knight's moves
positions = [(0, 0), (1, 2), (0, 4), (1, 6), (3, 7), (5, 6), (7, 7), (6, 5), (7, 3), (6, 1), (4, 2), (3, 4), (5, 3), (7, 4), (6, 6), (5, 4), (4, 6), (6, 7), (7, 5), (6, 3), (7, 1), (5, 0), (3, 1), (1, 0), (0, 2), (1, 4), (2, 2), (4, 3), (6, 4), (7, 2), (6, 0), (4, 1), (6, 2), (7, 0), (5, 1), (3, 0), (1, 1), (0, 3), (2, 4), (0, 5), (1, 7), (3, 6), (1, 5), (0, 7), (2, 6), (4, 7), (5, 5), (7, 6), (5, 7), (4, 5), (3, 3), (2, 1), (1, 3), (2, 5), (0, 6), (2, 7), (3, 5), (2, 3), (4, 4), (5, 2), (4, 0), (3, 2), (2, 0), (0, 1)]

for position in positions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    visited_cells.append(position)

    screen.fill(WHITE)
    draw_board(visited_cells)
    draw_knight(position)

    pygame.display.flip()
    clock.tick(FPS)
    pygame.time.wait(500)  # Pause for 500 milliseconds after each move