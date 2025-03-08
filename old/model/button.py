import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color

        # Draw shadow
        shadow_offset = 5
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=10)

        # Draw button
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Draw text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)



    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)



class ToggleButton:
    def __init__(self, text, x, y, width, height, color, hover_color, active_color, group):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.group = group  # List of all buttons in the same group
        self.active = False  # Is this button selected?
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.active:
            current_color = self.active_color  # Use active color if selected
        elif self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color  # Use hover color if hovered
        else:
            current_color = self.color  # Default color

        # Draw shadow
        shadow_offset = 5
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=10)

        # Draw button
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Draw border if selected
        if self.active:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, width=4, border_radius=10)  # White border when active

        # Draw text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            # Deselect all buttons in the group
            for button in self.group:
                button.active = False
            self.active = True
            return True
        return False




class SwitchButton:
    def __init__(self, text_black, text_white, x, y, width, height):
        self.text_black = text_black  
        self.text_white = text_white  
        self.text = text_black        
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 50)
        self.selected_piece = "black"  

        self.black_background = (0, 0, 0)  
        self.white_background = (255, 255, 255)  
        self.black_text = (255, 255, 255)  
        self.white_text = (0, 0, 0)  

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Set the current button colors based on the state
        if self.selected_piece == "black":
            current_background = self.black_background
            current_text = self.black_text
        else:
            current_background = self.white_background
            current_text = self.white_text

        # Change color on hover
        if is_hovered:
            current_background = (30, 30, 30) if self.selected_piece == "black" else (230, 230, 230)
            current_text = (255, 255, 255) if self.selected_piece == "black" else (0, 0, 0)

        # Draw shadow for a cleaner look
        shadow_offset = 5
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=10)

        # Draw the button itself
        pygame.draw.rect(screen, current_background, self.rect, border_radius=10)

        # Draw the text on the button
        text_surf = self.font.render(self.text, True, current_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            # Toggle the state on click
            if self.selected_piece == "black":
                self.selected_piece = "white"
                self.text = self.text_white
            else:
                self.selected_piece = "black"
                self.text = self.text_black

            self.selected_piece = self.selected_piece


class GameButton:
    def __init__(self, type, x, y, color, hover_color, action):
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.pos = (x,y)
        self.radius = 10 if type == "marker" else 12 
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color
        if self.type == 'marker':
            pygame.draw.circle(screen,current_color,self.pos,self.radius)
        elif self.type == 'ring':
            pygame.draw.circle(screen,current_color,self.pos,self.radius,4)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


