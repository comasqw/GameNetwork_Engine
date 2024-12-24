from engine.client import BaseClient
from grid_drawing_game_objects import Grid, ActionGetGrid, ActionChangeGridCellStatus, SET_GRID, UPDATE_GRID_CELL_STATUS
import pygame
pygame.init()


class Client(BaseClient):
    def __init__(self):
        super().__init__()
        self.start_client()
        self.grid: Grid | None = None
        self.get_grid()

        self.add_action(SET_GRID, self.set_grid)
        self.add_action(UPDATE_GRID_CELL_STATUS, self.update_grid)

    def get_grid(self):
        self.send_action_to_server(ActionGetGrid(self._client_id))

    def set_grid(self, grid_info: dict):
        self.grid = Grid.from_dict(grid_info)

    def update_grid(self, x: int, y: int):
        self.grid.change_cell_status(x, y)

    def change_grid_cell_status(self, x: int, y: int):
        self.send_action_to_server(ActionChangeGridCellStatus(self._client_id, x, y))


def main():
    client = Client()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("grid drawing")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                client.change_grid_cell_status(x, y)

        screen.fill((255, 255, 255))
        for coordinate, status in client.grid.grid.items():
            if status:
                x, y = map(int, coordinate.split(","))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, client.grid.cell_x, client.grid.cell_y))

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
