import pygame
import machine

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 70)
font_color = (150, 130, 60)   #150 130 60
bg = (55, 55, 55)   #80, 40, 110
height = 700  # высота = y
weight = 700  # ширина = x
sc = pygame.display.set_mode((weight, height))
clock = pygame.time.Clock()
run = True
control = machine.Control()
cell = height // machine.height
while run:
    sc.fill(bg)
    for plant in control.plants:
        if plant.name == 'grass':
            pygame.draw.rect(sc, (0, 100, 0), (plant.x * cell, plant.y * cell, cell, cell))
        elif plant.name == 'berry':
            pygame.draw.rect(sc, (100, 0, 0), (plant.x * cell, plant.y * cell, cell, cell))
    for animal in control.animals:
        pygame.draw.rect(sc, (0, 0, 40 * (animal.age // 100)), (animal.x * cell, animal.y * cell, cell, cell))
    pygame.display.flip()
    clock.tick(10)
    control.turn()

pygame.quit()
