import pygame


class GameRenderer:
    def __init__(self, width=600, height=600, grid_size=100, margin=5, offset=20):
        pygame.init()
        self.GRID_SIZE = grid_size
        self.MARGIN = margin
        self.OFFSET = offset
        self.WIDTH = width
        self.HEIGHT = height
        self.SCREEN_COLOR = (0, 0, 0)  # Background color
        self.AXIS_TEXT_COLOR = (255, 255, 255)  # White for axes and text

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game")
        self.screen.fill(self.SCREEN_COLOR)
        self.font = pygame.font.Font(None, 36)

    def value_to_color(self, value):
        colors = {
            0: (124, 252, 0),  # Grass Green
            1: (245, 245, 220),  # Beige
            2: (210, 180, 140),  # Darker Beige
            3: (139, 69, 19),  # Brown
            4: (0, 0, 255),  # Blue
        }
        return colors.get(value, (255, 0, 0))  # Default to red if value is invalid

    def draw_circle(self, x, z, color):
        # Convert grid coordinates (0 to 4) to pixel positions
        pixel_x = x * (self.GRID_SIZE + self.MARGIN) + self.GRID_SIZE // 2
        pixel_y = z * (self.GRID_SIZE + self.MARGIN) + self.GRID_SIZE // 2
        pygame.draw.circle(
            self.screen, color, (pixel_x + self.OFFSET, pixel_y + self.OFFSET), 30
        )

    def draw_axes(self):
        pygame.draw.line(
            self.screen, self.AXIS_TEXT_COLOR, (self.OFFSET, self.OFFSET), (self.WIDTH - self.OFFSET, self.OFFSET), 2
        )
        pygame.draw.line(
            self.screen, self.AXIS_TEXT_COLOR, (self.OFFSET, self.OFFSET), (self.OFFSET, self.HEIGHT - self.OFFSET), 2
        )
        x_label = self.font.render("x", True, self.AXIS_TEXT_COLOR)
        y_label = self.font.render("y", True, self.AXIS_TEXT_COLOR)
        self.screen.blit(x_label, (self.WIDTH - self.OFFSET + 5, self.OFFSET - 20))
        self.screen.blit(y_label, (self.OFFSET - 20, self.HEIGHT - self.OFFSET - 15))

    def draw_labels(self):
        for i in range(5):
            label = self.font.render(str(i), True, self.AXIS_TEXT_COLOR)
            x = self.OFFSET + i * (self.GRID_SIZE + self.MARGIN) + self.GRID_SIZE // 2 - label.get_width() // 2
            y = self.OFFSET - 25
            self.screen.blit(label, (x, y))
            label = self.font.render(str(i), True, self.AXIS_TEXT_COLOR)
            x = self.OFFSET - 20
            y = self.OFFSET + i * (self.GRID_SIZE + self.MARGIN) + self.GRID_SIZE // 2 - label.get_height() // 2
            self.screen.blit(label, (x, y))

    def render(self, array, circle_params):
        self.screen.fill(self.SCREEN_COLOR)
        if len(array) != 5 or not all(len(row) == 5 for row in array):
            raise ValueError("Input array must be a 5x5 grid.")
        for row in range(5):
            for col in range(5):
                value = array[row][col]
                color = self.value_to_color(value)
                x = col * (self.GRID_SIZE + self.MARGIN) + self.OFFSET
                y = row * (self.GRID_SIZE + self.MARGIN) + self.OFFSET
                pygame.draw.rect(self.screen, color, (x, y, self.GRID_SIZE, self.GRID_SIZE))
        for params in circle_params:
            x, z, color = params
            self.draw_circle(x, z, color)
        self.draw_axes()
        self.draw_labels()
        pygame.display.flip()


if __name__ == "__main__":
    renderer = GameRenderer()

    grid = [[0, 1, 2, 3, 4] for _ in range(5)]
    circle_params = [(0, 0, (255, 0, 0)), (4, 4, (0, 255, 0))]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update the grid or circle_params as needed
        renderer.render(grid, circle_params)

    pygame.quit()