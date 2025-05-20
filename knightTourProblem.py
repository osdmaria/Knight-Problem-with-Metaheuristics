import random
import pygame
import sys

class Chromosome:
    def __init__(self, genes):
        if genes == None:
            self.genes = random.choices(range(1,8), k=64)
        else:
            self.genes = genes
        

    def crossover(self, partner):
        point = random.randint(1,62)
        s1_g = self.genes[:point]
        s2_g = self.genes[point:]

        s1_p= partner[:point]
        s2_p = partner[point:]
        genes1 = s1_g + s2_p
        genes2 = s1_p + s2_g
        offspring1 = Chromosome(genes1)
        offspring2 = Chromosome(genes2)

        return offspring1, offspring2


    def mutation(self):
        mutation_prob = 0.01
        for i in range(0,63):
            will_mutate = random.random()
            if will_mutate <= mutation_prob:
                self.genes[i] = random.randint(1,8)

    



class Knight:
    def __init__(self,chromosome):
        self.position = (0,0)
        if chromosome == None:
            self.chromosome = Chromosome(genes=None)
        else: 
            self.chromosome = chromosome
        self.path = [(0,0)]
        self.fitness = 0
    def move_forward(self,direction):
        move_dict = {1: (1, 2), 2: (2, 1), 3: (2, -1), 4: (1, -2), 5: (-1, -2), 6: (-2, -1), 7: (-2, 1), 8: (-1, 2)}

        if direction in move_dict:
            move = move_dict[direction]
            self.position = (self.position[0] + move[0], self.position[1] + move[1])
            self.path.append(self.position)
            # print("appended", self.position)
            return self.position
        else:
            # print("Invalid direction")
            return self.position
        
    def move_backward(self):
        self.path.pop() 
        self.position = self.path[-1]
        # print("removed")

    def check_moves(self):
        for direction in range(0,64):
            valid = False
            current = self.chromosome.genes[direction]
            initial = self.chromosome.genes[direction]
            # print(self.chromosome.genes)
            while valid == False:
                new_position = self.move_forward(self.chromosome.genes[direction])
                if self.valid_move(new_position):
                    valid = True
                else:
                    # print(self.path)
                    self.move_backward()
                    current = (current % 8) + 1
                    if current == initial:
                        break
                    else:
                        self.chromosome.genes[direction] = current

            
       
    def eval_fitness(self):
        eval = 0
        for position in self.path:
            eval += 1
        self.fitness = eval
        return eval

    def valid_move(self,position):
        x , y = position
        if x >= 0 and x<=7 and y >= 0 and y <= 7 and (position not in self.path[:-1]):
            # print("valid!")
            return True
        else: 
            # print("invalid!")
            return False      




class Population:
    def __init__(self, population_size):
        self.generations = 1
        self.population = population_size
        self.knights = [Knight(chromosome=None) for i in range(1, self.population)]

    
    def check_population(self):
        for knight in self.knights:
            knight.check_moves()


    def evaluate(self):
        max = self.knights[0].eval_fitness()
        best_knight = self.knights[0]
        for knight in self.knights:
            temp = knight.eval_fitness()
            if temp > max:
                max = temp
                best_knight = knight
        print(max)
        return max, best_knight
    
    def tournament_selection(self):
        selected_knights = random.sample(self.knights,3)
        selected_sorted = sorted(selected_knights, key=lambda obj: obj.eval_fitness(), reverse=True)
        final_knights = selected_sorted[:2]
        return final_knights
    
    def create_new_generation(self):
        knights = []
        while len(knights) <=48:
            parents = self.tournament_selection()
            parentA = parents[0]
            parentB = parents[1]
            child1, child2 = parentA.chromosome.crossover(parentB.chromosome.genes)
            child1.mutation()
            child2.mutation()
            k1 = Knight(child1)
            k2 = Knight(child2)
            knights.append(k1)
            knights.append(k2)
        
        self.knights = knights
        self.generations = self.generations + 1
        print("number of generations is:", self.generations)



def main():
    population_size = 50
    # Create the initial population
    population = Population(population_size)
    while True:
    # Check the validity of the current population
        population.check_population()
        # Evaluate the current generation and get the best knight with its fitness value
        maxFit, bestSolution = population.evaluate()
        if maxFit == 64:
            print("Found solution!")
            print(bestSolution.path)
            break
        # Generate the new population
        population.create_new_generation()
    
    


    # Create the user interface to display the solution

    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 800
    CELL_SIZE = WIDTH // 8
    FPS = 60
    CIRCLE_RADIUS = CELL_SIZE // 12

    # Colors
    WHITE = (250, 245, 226)
    BLACK = (125, 215, 132)
    RED = (255, 0, 0)
    LINE_COLOR = (56, 166, 0)

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour Problem")

    # Knight image
    knight_img = pygame.image.load("knight.png")  # Replace "knight.png" with your image file
    knight_img = pygame.transform.scale(knight_img, (CELL_SIZE, CELL_SIZE))

    # Font
    font = pygame.font.Font(None, 30)
    FONT_COLOR = (0, 0, 0)

    # Function to draw the chessboard
    def draw_board(visited_cells, lines):
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                if (col, row) in visited_cells:
                    draw_visited_cell((col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                    visited_cells.index((col, row)) + 1)

        for line in lines:
            pygame.draw.line(screen, LINE_COLOR, line[0], line[1], 2)

    def draw_visited_cell(center, move_number):
        pygame.draw.circle(screen, (56, 166, 0)
, center, CIRCLE_RADIUS)

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
    lines = []

    # List of knight's moves
    positions = bestSolution.path

    for i in range(len(positions) - 1):
        current_position = positions[i]
        next_position = positions[i + 1]

        visited_cells.append(current_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_board(visited_cells, lines)
        draw_knight(current_position)

        lines.append(((current_position[0] * CELL_SIZE + CELL_SIZE // 2, current_position[1] * CELL_SIZE + CELL_SIZE // 2),
                    (next_position[0] * CELL_SIZE + CELL_SIZE // 2, next_position[1] * CELL_SIZE + CELL_SIZE // 2)))

        pygame.display.flip()
        clock.tick(FPS)
        pygame.time.wait(500)  # Pause for 500 milliseconds after each move

    # Draw the knight at the last position
    screen.fill(WHITE)
    draw_board(visited_cells, lines)
    draw_knight(positions[-1])  # Draw at the last position
    pygame.display.flip()

    # Wait for the user to press Enter to exit
    waiting_for_enter = True
    while waiting_for_enter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_enter = False
                    pygame.quit()
                    sys.exit()




if __name__ == "__main__":
    main()
             

