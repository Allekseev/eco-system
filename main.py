import pygame
import machine

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 70)
font_color = (150, 130, 60)   #150 130 60
bg = (55, 55, 55)   #80, 40, 110
height = 750  # высота = y
weight = 750  # ширина = x
sc = pygame.display.set_mode((weight, height))
clock = pygame.time.Clock()
run = True
control = machine.Control()
cell = height // machine.height
speed = 1
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for i in range(100):
                    control.turn()
            if event.key == pygame.K_RIGHT:
                speed += 1
                print(speed)
            if event.key == pygame.K_LEFT and speed:
                speed -= 1
                print(speed)
    sc.fill(bg)
    for plant in control.plants:
        if plant.name == 'grass':
            pygame.draw.rect(sc, (0, 100, 0), (plant.x * cell, plant.y * cell, cell, cell))
        elif plant.name == 'berry':
            pygame.draw.rect(sc, (100, 0, 0), (plant.x * cell, plant.y * cell, cell, cell))
    for animal in control.animals:
        pygame.draw.rect(sc, (animal.rgb[0] * (animal.gen >= 0), animal.rgb[1] * (animal.gen >= 0), animal.rgb[2] * (animal.gen >= 0)), (animal.x * cell, animal.y * cell, cell, cell))
    pygame.display.flip()
    clock.tick(10)
    for i in range(speed):
        control.turn()

pygame.quit()
