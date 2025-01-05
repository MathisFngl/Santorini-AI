import pygame


def render_grid(array, circle_params):
    """
    Render a 5x5 grid in PyGame with colors transitioning from white to red.
    Parameters:
        array (2D list): A 5x5 list with values ranging from 0 to 5.
    """
    # Initialize PyGame
    pygame.init()
    # Constants
    GRID_SIZE = 100  # Size of each cell
    MARGIN = 5  # Space between cells
    OFFSET = 20 #Margin for axes
    WIDTH, HEIGHT = (GRID_SIZE + MARGIN) * 5 + OFFSET , (GRID_SIZE + MARGIN) * 5 + OFFSET
    SCREEN_COLOR = (0, 0, 0)  # Background color
    AXIS_TEXT_COLOR = (255, 255, 255)  # White for axes and text
    # Create PyGame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    screen.fill(SCREEN_COLOR)
    # Font for text
    font = pygame.font.Font(None, 36)
    # Validate input array
    if len(array) != 5 or not all(len(row) == 5 for row in array):
        raise ValueError("Input array must be a 5x5 grid.")
    def value_to_color(value):
        if value == 0:
            return (124, 252, 0)  # Grass Green
        elif value == 1:
            return (245, 245, 220)  # Beige
        elif value == 2:
            return (210, 180, 140)  # Darker Beige
        elif value == 3:
            return (139, 69, 19)  # Brown
        elif value == 4:
            return (0, 0, 255)  # Blue
    def draw_circle(x, z, color):
        # Convert grid coordinates (0 to 4) to pixel positions
        pixel_x = x * (GRID_SIZE + MARGIN) + GRID_SIZE // 2
        pixel_y = z * (GRID_SIZE + MARGIN) + GRID_SIZE // 2
        pygame.draw.circle(screen, color, (pixel_x + OFFSET, pixel_y + OFFSET), 30)

    def draw_axes():
        # Draw horizontal axis (x)
        pygame.draw.line(screen, AXIS_TEXT_COLOR, (OFFSET, OFFSET), (WIDTH - OFFSET, OFFSET), 2)
        pygame.draw.polygon(screen, AXIS_TEXT_COLOR, [(WIDTH - OFFSET, OFFSET), (WIDTH - OFFSET - 10, OFFSET - 5),
                                                      (WIDTH - OFFSET - 10, OFFSET + 5)])
        # Draw vertical axis (y)
        pygame.draw.line(screen, AXIS_TEXT_COLOR, (OFFSET, OFFSET), (OFFSET, HEIGHT - OFFSET), 2)
        pygame.draw.polygon(screen, AXIS_TEXT_COLOR, [(OFFSET, HEIGHT - OFFSET), (OFFSET - 5, HEIGHT - OFFSET - 10),
                                                      (OFFSET + 5, HEIGHT - OFFSET - 10)])
        # Label axes
        x_label = font.render("x", True, AXIS_TEXT_COLOR)
        y_label = font.render("y", True, AXIS_TEXT_COLOR)
        screen.blit(x_label, (WIDTH - OFFSET + 5, OFFSET - 20))
        screen.blit(y_label, (OFFSET - 20, HEIGHT - OFFSET - 15))

    def draw_labels():
        # Draw numbers for x-axis
        for i in range(5):
            label = font.render(str(i), True, AXIS_TEXT_COLOR)
            x = OFFSET + i * (GRID_SIZE + MARGIN) + GRID_SIZE // 2 - label.get_width() // 2
            y = OFFSET - 25
            screen.blit(label, (x, y))

    # Main render loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Draw the grid
        for row in range(5):
            for col in range(5):
                value = array[row][col]
                color = value_to_color(value)
                x = col * (GRID_SIZE + MARGIN) + OFFSET
                y = row * (GRID_SIZE + MARGIN)  + OFFSET
                pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))
        for params in circle_params:
            x, z, color = params
            draw_circle(x, z, color)
            draw_axes()
            draw_labels()
        pygame.display.flip()
    pygame.quit()