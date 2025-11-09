import pygame
from worm import worm_class

main_width = 1920
main_height = 1080
apps_width = 960
apps_height = 540

worms = []

apps_size = [(960, 540, (0,0)), (1920, 540, (960,0)),
             (960, 1080, (0,540)), (1920, 1080, (960,540))]

pygame.init()
screen = pygame.display.set_mode((main_width, main_height))
clock = pygame.time.Clock()
run = 1

for size in apps_size:
    worms.append(worm_class(200, size[0], size[1], size[2]))

font = pygame.font.Font('freesansbold.ttf', 32)

#worm = worm_class(200, apps_size, apps_size, (0,0))
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
    screen.fill((0,0,0))
    for worm in worms:
        stamina, width, height, null_point = worm.neuro_update(screen)
        if stamina == 0:
            worms.remove(worm)
            worms.append(worm_class(200, width, height, null_point))
        

    
    pygame.draw.line(screen, (0,0,255), (960, 0), (960, 1080), 5)
    pygame.draw.line(screen, (0,0,255), (0, 540), (1920, 540), 5)


    fps = clock.get_fps()
    text = font.render(str(int(fps)), True, (0,255,0), (0,0,255))
    textRect = text.get_rect()
    textRect.center = (960,16)
    screen.blit(text,textRect)
    pygame.display.update()
    clock.tick(60)