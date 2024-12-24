import socket
import uuid
import json
from threading import Thread

from .base_networking import BaseNetworking
from .protocol import GameObjectsManager, Action, ActionSetClientId


class Client:
    def __init__(self, client_id: int, client_socket: socket.socket, address: tuple[str, int]):
        self._client_id = client_id
        self._client_socket = client_socket
        self._address = address

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_socket(self):
        return self._client_socket

    @property
    def address(self):
        return self._address

    def close_socket(self):
        self._client_socket.close()


class ClientManager:
    def __init__(self):
        self._clients: dict[int, Client] = {}

    @property
    def clients(self):
        return self._clients

    def generate_client_id(self):
        client_id = uuid.uuid4().int

        while client_id in self._clients:
            client_id = uuid.uuid4().int

        return client_id

    def add_client(self, client: Client):
        if client.client_id in self._clients:
            return

        self._clients[client.client_id] = client

    def create_client(self, client_socket: socket.socket, address: tuple[str, int]) -> Client:
        client_id = self.generate_client_id()
        client = Client(client_id, client_socket, address)
        self.add_client(client)
        return client

    def remove_client(self, client_id: int):
        if client_id in self._clients:
            del self._clients[client_id]

    def get_client(self, client_id: int):
        return self._clients.get(client_id)


class BaseServer(BaseNetworking):
    def __init__(self, address: tuple[str, int] = ("localhost", 8000)):
        self._address = address
        self.clients_manager = ClientManager()
        self.game_objects_manager = GameObjectsManager()
        self._actions: dict = {}
        self._socket: socket.socket | None = None

    def add_action(self, action: str, function):
        self._actions[action] = function

    def call_action(self, action: Action):
        function = self._actions.get(action.action)
        if function:
            function(**action.args)

    def send_action_to_client(self, client: Client, action: Action):
        self.send_data(client.client_socket, action.action_info)

    def send_action_to_all_clients(self, action: Action):
        for client in self.clients_manager.clients.values():
            self.send_action_to_client(client, action)

    def start_server(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self._address)
        self._socket.listen()
        print(f"Server started on {self._address}")
        self._listen_clients()

    def _listen_clients(self):
        while True:
            conn, address = self._socket.accept()
            client = self.clients_manager.create_client(conn, address)
            Thread(target=self._handle_client, args=(client,)).start()

    def _handle_actions(self, client: Client):
        data = self.recv_data(client.client_socket)
        if data:
            data = json.loads(data)
            action = Action.from_dict(data)
            self.call_action(action)

    def _handle_client(self, client: Client):
        self.set_client_id(client)
        while True:
            try:
                self._handle_actions(client)
            except Exception as e:
                print(e)
                client.close_socket()
                self.clients_manager.remove_client(client.client_id)
                break

    # actions

    def set_client_id(self, client: Client):
        self.send_action_to_client(client, ActionSetClientId(client.client_id))
