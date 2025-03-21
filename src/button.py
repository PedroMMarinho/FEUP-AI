import pygame
from ui import draw_text

class ClickButton:

    button_groups = {}

    def __init__(self,text, x, y, height, width, font, 
                 button_color, text_color, hover_color, hover_text_color, border_color=None, shadow_color=None, action=None,
                 alt_text=None, alt_button_color=None, alt_text_color=None, alt_hover_color=None, alt_hover_text_color=None, alt_border_color=None, alt_shadow_color=None, selected=False, group=None):
        
        self.text = text
        self.alt_text = alt_text
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.font = font
        self.action = action
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Select and group logic
        self.selected = selected
        self.group = group    
        if self.group is not None and self.group not in ClickButton.button_groups:
            ClickButton.button_groups[self.group] = self
        if self.selected:
            ClickButton.button_groups[self.group] = self
        # Colors
        self.color = button_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.hover_text_color = hover_text_color
        self.border_color = border_color
        self.shadow_color = shadow_color
        # Alternative Colors
        self.alt_color = alt_button_color
        self.alt_text_color = alt_text_color
        self.alt_hover_color = alt_hover_color
        self.alt_hover_text_color = alt_hover_text_color
        self.alt_border_color = alt_border_color
        self.alt_shadow_color = alt_shadow_color

    def draw(self, screen):
        pos = pygame.mouse.get_pos()

        is_hovered = self.rect.collidepoint(pos)

        if self.selected:
            button_color = self.color
        elif is_hovered:
            button_color = self.hover_color
        else:
            button_color = self.color

        if self.selected:
            text_color = self.text_color
        elif is_hovered:
            text_color = self.hover_text_color
        else:
            text_color = self.text_color


        # Shadow
        if self.shadow_color is not None:
            shadow_offset = 4
            pygame.draw.rect(screen, self.shadow_color, (self.x + shadow_offset, self.y + shadow_offset, self.width, self.height), border_radius=10)

        # Border
        if self.border_color is not None:
            pygame.draw.rect(screen, self.border_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), border_radius=12)

        # Button
        pygame.draw.rect(screen, button_color, self.rect, border_radius=10)

        # Text
        text_x = self.x + (self.width - self.font.size(self.text)[0]) // 2
        text_y = self.y + (self.height - self.font.get_height()) // 2

        draw_text(screen, self.text, self.font, text_color, text_x, text_y)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos) and self.action:
            if not (self.group is not None and self.selected):
                self.action()
                self.change_to_alt()

            if self.group is not None and not self.selected:
                previous_button = ClickButton.button_groups[self.group]
                previous_button.change_to_alt()
                previous_button.selected = False  
                ClickButton.button_groups[self.group] = self
                self.selected = True

    def change_to_alt(self):

        if self.alt_text is not None:
            self.text, self.alt_text = self.alt_text, self.text
        if self.alt_color is not None:
            self.color, self.alt_color = self.alt_color, self.color
        if self.alt_text_color is not None:
            self.text_color, self.alt_text_color = self.alt_text_color, self.text_color
        if self.alt_hover_color is not None:
            self.hover_color, self.alt_hover_color = self.alt_hover_color, self.hover_color
        if self.alt_hover_text_color is not None:
            self.hover_text_color, self.alt_hover_text_color = self.alt_hover_text_color, self.hover_text_color
        if self.alt_border_color is not None:
            self.border_color, self.alt_border_color = self.alt_border_color, self.border_color
        if self.alt_shadow_color is not None:
            self.shadow_color, self.alt_shadow_color = self.alt_shadow_color, self.shadow_color
        
