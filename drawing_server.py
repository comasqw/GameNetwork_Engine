from engine.server import BaseServer
from drawing_game_objects import Dot, GET_ALL_DOTS, ActionSetAllDots, ADD_DOT, ActionSetDot


class Server(BaseServer):
    def __init__(self):
        super().__init__()
        self.dots: list[Dot] = []

        self.add_action(GET_ALL_DOTS, self.get_all_dots)
        self.add_action(ADD_DOT, self.add_dot)

    def get_all_dots(self, client_id: int):
        client = self.clients_manager.get_client(client_id)
        if client:
            self.send_action_to_client(client, ActionSetAllDots(self.dots))

    def add_dot(self, client_id: int, x: int, y: int, color: tuple):
        client = self.clients_manager.get_client(client_id)
        if client:
            dot = Dot(self.game_objects_manager.generate_object_id(), x=x, y=y, color=color)
            self.dots.append(dot)
            self.send_action_to_all_clients(ActionSetDot(dot))


if __name__ == '__main__':
    server = Server()
    server.start_server()