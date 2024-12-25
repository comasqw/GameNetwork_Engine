from engine.client import BaseClient
from drawing_game_objects import Dot, ActionGetAllDots, SET_ALL_DOTS, ActionAddDot, SET_DOT
import pygame
pygame.init()


class Client(BaseClient):
    def __init__(self):
        super().__init__()
        self.start_client()
        self.dots: list[Dot] = []
        self.add_action(SET_ALL_DOTS, self.set_all_dots)
        self.add_action(SET_DOT, self.set_dot)
        self.get_all_dots()

    def get_all_dots(self):
        self.send_action_to_server(ActionGetAllDots(self._client_id))

    def set_all_dots(self, dots: list[dict]):
        for dot in dots:
            self.dots.append(Dot.from_dict(dot))

    def add_dot(self, x: int, y: int, color=(0, 0, 0)):
        self.send_action_to_server(ActionAddDot(self._client_id, x=x, y=y, color=color))

    def set_dot(self, dot: dict):
        self.dots.append(Dot.from_dict(dot))


def main():
    client = Client()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    colors = {1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255), 4: (0, 0, 0)}
    color = colors[4]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    color = colors[1]
                elif event.key == pygame.K_2:
                    color = colors[2]
                elif event.key == pygame.K_3:
                    color = colors[3]
                elif event.key == pygame.K_4:
                    color = colors[4]

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            x, y = pygame.mouse.get_pos()
            client.add_dot(x, y, color)

        screen.fill((255, 255, 255))

        for dot in client.dots:
            pygame.draw.circle(screen, tuple(dot.color), (dot.x, dot.y), 5, 0)

        pygame.display.update()
        # clock.tick(60)


if __name__ == '__main__':
    main()
