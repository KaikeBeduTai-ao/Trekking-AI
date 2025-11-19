import pygame
from ui import GameWindow

from vision.cone_detector import ConeDetector
import cv2


def main():
    pygame.init()
    vision = ConeDetector()

    window = GameWindow()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame = vision.get_frame()
        if frame is not None:
            cv2.imshow("Camera", frame)
            cv2.waitKey(1)

        window.update()
        clock.tick(60)  # 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
