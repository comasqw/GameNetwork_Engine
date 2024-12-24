from engine.server import BaseServer
from grid_drawing_game_objects import Grid, ActionSetGrid, ActionUpdateGridCellStatus, GET_GRID, CHANGE_GRID_CELL_STATUS


class Server(BaseServer):
    def __init__(self):
        super().__init__()
        self.grid = Grid(self.game_objects_manager.generate_object_id(),
                         size_x=600, size_y=600,
                         cell_x=30, cell_y=30)
        self.game_objects_manager.add_game_object(self.grid)
        self.add_action(GET_GRID, self.get_grid)
        self.add_action(CHANGE_GRID_CELL_STATUS, self.change_grid_cell_status)

    def get_grid(self, client_id: int):
        client = self.clients_manager.get_client(client_id)
        if client:
            self.send_action_to_client(client, ActionSetGrid(self.grid.object_info))

    def change_grid_cell_status(self, client_id: int, x: int, y: int):
        client = self.clients_manager.get_client(client_id)
        if client:
            self.grid.change_cell_status(x, y)
            self.send_action_to_all_clients(ActionUpdateGridCellStatus(x, y))


if __name__ == '__main__':
    server = Server()
    server.start_server()
