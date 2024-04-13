import pygame
import sys
import random
import heapq

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
NUM_NODES_X = (WIDTH - CELL_SIZE) // CELL_SIZE
NUM_NODES_Y = (HEIGHT - CELL_SIZE) // CELL_SIZE
NUM_ROBOTS = 4  # Number of robots

# Define robot class
class Robot:
    def __init__(self, x, y, path_planned=False):
        self.x = x
        self.y = y
        self.target_node = None
        self.path_planned = path_planned
        self.path = []

    def move_to_node(self, node_x, node_y):
        self.target_node = Node(node_x * CELL_SIZE + CELL_SIZE // 2, node_y * CELL_SIZE + CELL_SIZE // 2)
        if self.path_planned:
            self.path = self.find_path()

    # recompute path after n steps 
    def update(self):
        steps = 0
        # n = 10 steps
        while steps < 10:
            if self.path_planned and self.path:
                next_node = self.path[0]
                dx = 1 if next_node.x > self.x else -1 if next_node.x < self.x else 0
                dy = 1 if next_node.y > self.y else -1 if next_node.y < self.y else 0
                self.x += dx
                self.y += dy
                if self.x == next_node.x and self.y == next_node.y:
                    self.path.pop(0)
            elif self.target_node:
                dx = 1 if self.target_node.x > self.x else -1 if self.target_node.x < self.x else 0
                dy = 1 if self.target_node.y > self.y else -1 if self.target_node.y < self.y else 0
                self.x += dx
                self.y += dy
                if self.x == self.target_node.x and self.y == self.target_node.y:
                    self.target_node = None
            steps = steps + 1

    def find_path(self):
        start = (self.x // CELL_SIZE, self.y // CELL_SIZE)
        end = (self.target_node.x // CELL_SIZE, self.target_node.y // CELL_SIZE)
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, (0, start, []))
        while open_list:
            cost, current, path = heapq.heappop(open_list)
            if current == end:
                return [Node((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE) for x, y in path]
            if current in closed_list:
                continue
            closed_list.add(current)
            for neighbor in self.get_neighbors(current):
                new_cost = cost + 1  # Assuming all edges have a cost of 1
                new_path = path + [current]
                heapq.heappush(open_list, (new_cost + self.heuristic(neighbor, end), neighbor, new_path))
        return []

    def heuristic(self, current, end):
        return abs(current[0] - end[0]) + abs(current[1] - end[1])

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < NUM_NODES_X - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < NUM_NODES_Y - 1:
            neighbors.append((x, y + 1))
        return neighbors

# Define node class
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 5)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create robots
robots = [Robot(random.randint(0, NUM_NODES_X - 1) * CELL_SIZE + CELL_SIZE // 2,
                random.randint(0, NUM_NODES_Y - 1) * CELL_SIZE + CELL_SIZE // 2) for _ in range(NUM_ROBOTS - 1)]
robots.append(Robot(random.randint(0, NUM_NODES_X - 1) * CELL_SIZE + CELL_SIZE // 2,
                    random.randint(0, NUM_NODES_Y - 1) * CELL_SIZE + CELL_SIZE // 2, path_planned=True))

# Create nodes
nodes = [[Node((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE) for y in range(NUM_NODES_Y)] for x in range(NUM_NODES_X)]

# Assign random target nodes to robots
for robot in robots:
    target_node = random.choice(random.choice(nodes))
    robot.move_to_node(target_node.x // CELL_SIZE, target_node.y // CELL_SIZE)

# Main loop
while True:
    screen.fill(WHITE)

    # Draw nodes
    for row in nodes:
        for node in row:
            node.draw(screen)

    # Draw robots
    for robot in robots:
        color = BLUE if robot.path_planned else RED
        pygame.draw.rect(screen, color, (robot.x - CELL_SIZE // 2, robot.y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE))

    # Update robots
    for robot in robots:
        #while robot.x != target_node.x and robot.y != target_node.y:
        robot.update()
        if robot.x != target_node.x and robot.y != target_node.y:
            robot.move_to_node(target_node.x // CELL_SIZE, target_node.y // CELL_SIZE)
            robot.update()
        # If the robot reached its target node, assign a new random target node
        if not robot.path_planned and robot.target_node is None:
            target_node = random.choice(random.choice(nodes))
            robot.move_to_node(target_node.x // CELL_SIZE, target_node.y // CELL_SIZE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(30)
