import pygame, math, random
import numpy as np

class worm_class:
    def __init__(self, worm_lenght, display_weight, display_heigh, null_point):
        self.worm = []
        self.display_weight, self.display_heigh = display_weight, display_heigh
        self.null_point = null_point
        self.worm_pos = (random.randint(self.null_point[0], self.display_weight), random.randint(self.null_point[1], self.display_heigh))
        for i in range(worm_lenght):
            self.worm.append(self.worm_pos)

        self.hit_front = False
        self.hit_left = False
        self.hit_right = False

        self.apples = []
        for i in range(20):
            self.apples.append(pygame.Rect(random.randint(self.null_point[0], self.display_weight), random.randint(self.null_point[1], self.display_heigh), 15, 15))


        self.worm_x, self.worm_y = self.worm_pos
        self.stamina = 100
        self.speed = 1
        self.angle = random.randint(0,360)
        ai = {
            "input_size": 4,
            "hidden_size": 10,
            "output_size": 3
        }
        self.W1 = np.random.uniform(0, 1, (ai["hidden_size"], ai["input_size"]))
        self.b1 = np.random.uniform(0, 1, (ai["hidden_size"],))

        self.W2 = np.random.uniform(0, 1, (ai["output_size"], ai["hidden_size"]))
        self.b2 = np.random.uniform(0, 1, (ai["output_size"],))
    def neuro_update(self, screen):
        if self.stamina > 0:
            self.stamina -= 0.1
        else:
            self.stamina = 0
        ray_distance = 175
        for pos in self.worm[::10]:
            pygame.draw.circle(screen, (255,int(self.stamina*2.55),int(self.stamina*2.55)), pos, 10)

        self.angle_rad = math.radians(self.angle)
        self.ray_angle_rad_p = math.radians(self.angle+5)
        self.ray_angle_rad_m = math.radians(self.angle-5)


        for i in range(len(self.worm) - 1, 0, -1):
            self.worm[i] = self.worm[(i-1)]

        self.worm_x += math.cos(self.angle_rad) * self.speed
        self.worm_y += math.sin(self.angle_rad) * self.speed
        self.worm[0] = self.worm_x, self.worm_y

        if self.worm_x <= self.null_point[0]+10 or self.worm_x >= self.display_weight-10:
            self.angle = 180-self.angle
            self.angle_rad = math.radians(self.angle)
        if self.worm_y <= self.null_point[1]+10 or self.worm_y >= self.display_heigh-10:
            self.angle = -self.angle
            self.angle_rad = math.radians(self.angle)

        self.hit_front = False
        self.hit_right = False
        self.hit_left = False

        for apple in self.apples:
            pygame.draw.rect(screen, (100,255,100), apple)
            if apple.clipline(self.worm[0], (self.worm_x + math.cos(self.angle_rad) * ray_distance, self.worm_y + math.sin(self.angle_rad) * ray_distance)):
                self.hit_front = True
            if apple.clipline(self.worm[0], (self.worm_x + math.cos(self.ray_angle_rad_m) * ray_distance, self.worm_y + math.sin(self.ray_angle_rad_m) * ray_distance)):
                self.hit_left = True
            if apple.clipline(self.worm[0], (self.worm_x + math.cos(self.ray_angle_rad_p) * ray_distance, self.worm_y + math.sin(self.ray_angle_rad_p) * ray_distance)):
                self.hit_right = True


            #math shit
            self.nearest_x = max(apple.left, min(self.worm_x, apple.right))
            self.nearest_y = max(apple.top, min(self.worm_y, apple.bottom))
            dx = self.worm_x - self.nearest_x
            dy = self.worm_y - self.nearest_y
            if dx*dx + dy*dy < 15**2:
                self.apples.remove(apple)
                self.stamina += 50
                if self.stamina > 100:
                    self.stamina = 100
                self.apples.append(pygame.Rect(random.randint(self.null_point[0],self.display_weight), random.randint(self.null_point[1],self.display_heigh), 15, 15))


        self.inputs = np.array([self.hit_front, self.hit_left, self.hit_right, self.stamina/100])
        self.hidden = np.tanh(np.dot(self.W1, self.inputs) + self.b1)
        self.output = np.dot(self.W2, self.hidden) + self.b2
        self.best_choise = np.argmax(self.output)

        if self.best_choise == 1:
            self.angle -= 1
        elif self.best_choise == 2:
            self.angle += 1
        else:
            pass

        pygame.draw.line(screen, (0,255,0) if self.hit_front else (255,0,0), (self.worm[0]), (self.worm_x + math.cos(self.angle_rad)*ray_distance, self.worm_y + math.sin(self.angle_rad)*ray_distance))
        pygame.draw.line(screen, (0,255,0) if self.hit_left else (255,0,0), (self.worm[0]), (self.worm_x + math.cos(self.ray_angle_rad_m)*ray_distance, self.worm_y + math.sin(self.ray_angle_rad_m)*ray_distance))
        pygame.draw.line(screen, (0,255,0) if self.hit_right else (255,0,0), (self.worm[0]), (self.worm_x + math.cos(self.ray_angle_rad_p)*ray_distance, self.worm_y + math.sin(self.ray_angle_rad_p)*ray_distance))


        return self.stamina, self.display_weight, self.display_heigh, self.null_point

        #if random.randint(0,100) < 10:
        #    self.angle += random.randint(-15, 15)