import math
HEX_RADIUS = 40
SQRT3 = math.sqrt(3)
from settings import WIDTH, HEIGHT
class Hexagon:
    """Represents a hexagonal tile on the board."""
    def __init__(self, q, r, s, radius=HEX_RADIUS):
        self.q = q
        self.r = r
        self.s = s
        self.radius = radius
        self.x, self.y = self.calculate_position()
        self.corners = self.get_corners()
        self.vertices = self.get_vertices()
        self.internal_lines = self.get_internal_lines()

    
    def calculate_position(self):
        """Converts hexagonal coordinates to pixel coordinates."""
        center_x, center_y = WIDTH // 2, HEIGHT // 5
        x = center_x + self.radius * 1.5 * self.q
        y = center_y + self.radius * SQRT3 * (self.r + self.q / 2)
        return x, y
    
    def get_corners(self):
        """Returns the six corner points of the hexagon."""
        angles = [math.radians(60 * i) for i in range(6)]
        return [(self.x + self.radius * math.cos(a), self.y + self.radius * math.sin(a)) for a in angles]
    
    def get_vertices(self):
        """Returns the center and edges where rings can be placed."""
        return [(self.x, self.y)] + self.get_corners()

    def get_internal_lines(self):
        """Returns the internal lines of the hexagon to divide it into six triangular segments."""
        return [(self.x, self.y, corner[0], corner[1]) for corner in self.corners]


def generate_hex_grid():
    """Generates the hexagonal ring structure for the YINSH board."""
    hexagons = []
    directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]
    
    for radius in range(0, 5):  
        q, r, s = -radius, radius, 0  
        for i in range(6):  
            for _ in range(radius):
                hexagons.append(Hexagon(q, r, s))
                q, r, s = q + directions[i][0], r + directions[i][1], s + directions[i][2]
    return hexagons