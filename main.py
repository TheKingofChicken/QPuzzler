import pygame
from pygame.constants import FULLSCREEN

#Initialise pygame
pygame.init()

#setting up display
display = pygame.display.set_mode((800,600))
pygame.display.set_caption('QPuzzler')

#Game loop:
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == '__main__':
    main()
