 
import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
pygame.init()
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("assets/ball.wav")

screen_width = 700
screen_height = 500
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Ballz")

def find_symmetrical_line(p1, p2):
                x1, y1 = p1
                x2, y2 = p2

                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2

                slope = (y2 - y1) / (x2 - x1)
                perpendicular_slope = -1 / slope

                b = mid_y - perpendicular_slope * mid_x

                return perpendicular_slope, b

def find_line(p1, p2):
                    x1, y1 = p1
                    x2, y2 = p2

                    slope = (y2 - y1) / (x2 - x1)
                    intercept = y1 - slope * x1

                    return slope, intercept

def find_intersection_point(line1, line2):
                        slope1, intercept1 = line1
                        slope2, intercept2 = line2

                        if slope1 == slope2:
                            return None  # Lines are parallel, no intersection point

                        x = (intercept2 - intercept1) / (slope1 - slope2)
                        y = slope1 * x + intercept1

                        return x, y        
def calculate_vector(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    vector_x = x2 - x1
    vector_y = y2 - y1

    return [vector_x, vector_y]

def shorten_vector(vector, length):
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
        if magnitude == 0:
            return vector
        normalized_vector = [vector[0] / magnitude, vector[1] / magnitude]
        shortened_vector = [normalized_vector[0] * length, normalized_vector[1] * length]
        # print(shortened_vector)
        return shortened_vector    




class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 350
        self.y = 250
        self.radious = 200
        self.color = BLACK
        self.border = 3

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radious, self.border)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vector=[5, 2], color=RED):
        super().__init__()
        
        self.x = x
        self.y = y
        self.y_prev = self.y
        self.x_prev = self.x

        self.radius = 20
        self.color = color
        self.vy = 0 # velocity in y direction
        # self.ay = 0 # acceleration in y direction
        self.ay = 0.4 # acceleration in y direction
        self.speed = 7


        self.colided = False
        self.vector = vector
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius)
        # print(self.vector)
    
    def stop(self):
        print("STOP")
        # self.vy = 0
        # self.ay = 0

    def check_collision_with_box(self, box):
        distance_from_box_center = ((self.x - box.x)**2 + (self.y - box.y)**2)**0.5
        max_distance = box.radious - box.border - self.radius
        return distance_from_box_center > max_distance

    def update(self, box):
        self.y_prev = self.y
        self.x_prev = self.x
        self.vy += self.ay # Update y velocity with acceleration
        self.y += self.vy # Update y position with velocity

        # speed = 7
        self.vector = shorten_vector(self.vector, self.speed)
        self.x += self.vector[0]
        self.y += self.vector[1]
        # print(self.vector)

        if self.check_collision_with_box(box):
            self.y = self.y_prev
            self.x = self.x_prev
            self.vector[0] = -self.vector[0]
            self.vector[1] = -self.vector[1]
            self.speed -= 0.05
            # print(self.speed)
            self.vy = -self.vy
            # self.ay += 0.03

    def check_collision_with_ball(self, ball):
        distance = ((self.x - ball.x)**2 + (self.y - ball.y)**2)**0.5
        # print(distance)
        return distance < self.radius + ball.radius

    def update_vector_after_collision(self, ball):
        print(self.colided)
        if self.check_collision_with_ball(ball) and not self.check_collision_with_box(box) and self.colided == False:
            self.colided = True
            self.speed -= 0.05
            # print(self.speed)
            collision_sound.play()
            line = find_symmetrical_line((self.x, self.y), (ball.x, ball.y))
            a, b = line
            line2 = find_line((self.x, self.y), (self.x + self.vector[0], ball.y + self.vector[1]))
            a2, b2 = line2

            intersection_point = find_intersection_point(line, line2)
            
            x_vec, y_vec = calculate_vector((self.x, self.y), intersection_point)
            
            self.vector = [y_vec, x_vec]
        else: 
              self.colided = False

done = False
clock = pygame.time.Clock()
ball = Ball(350, 250, [8, 3])
ball2 = Ball(300, 235, [3, 5], "BLUE")
box = Box()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic ---
    ball.update(box)
    ball2.update(box)

    # print(ball.check_collision_with_ball(ball2))
    ball.update_vector_after_collision(ball2)
    ball2.update_vector_after_collision(ball)

    # --- Screen-clearing ---
 
    screen.fill(WHITE)
 
    # --- Drawing code ---
    box.draw(screen)
    ball.draw(screen)
    ball2.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()