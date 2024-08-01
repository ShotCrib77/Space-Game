import pygame as pg

pg.init()

# Define some colors
GREY = (169, 169, 169)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Button class
class Button:
    def __init__(self, rect, text, font, color, text_color, action=None):
        self.rect = pg.Rect(rect)  # rect should be a tuple (x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        # Draw the button
        pg.draw.rect(surface, self.color, self.rect)
        
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Check if the button was clicked
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

# Example actions for buttons
def action_button_1():
    print("Button 1 action!")

def action_button_2():
    print("Button 2 action!")

# Initialize screen and fonts
screen = pg.display.set_mode((600, 400))
font = pg.font.SysFont('Arial', 24)

# Create buttons using rectangles for positioning and size
button_1 = Button((50, 25, 128, 75), 'Dmg', font, BLACK, WHITE, action_button_1)
button_2 = Button((236, 25, 128, 75), 'Speed', font, BLACK, WHITE, action_button_2)
button_3 = Button((422, 25, 128, 75), 'Health', font, BLACK, WHITE)

# Main loop
running = True
while running:
    screen.fill(GREY)
    
    # Draw buttons
    button_1.draw(screen)
    button_2.draw(screen)
    button_3.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Check for button clicks
        button_1.is_clicked(event)
        button_2.is_clicked(event)
        button_3.is_clicked(event)

    pg.display.update()

pg.quit() 