import socket
import json
from threading import Thread

from .base_networking import BaseNetworking
from .protocol import GameObjectsManager, Action, SET_CLIENT_ID


class BaseClient(BaseNetworking):
    def __init__(self, address: tuple[str, int] = ("localhost", 8000)):
        self._client_id: int | None = None
        self._address = address
        self._game_objects_manager = GameObjectsManager
        self._actions = {
            SET_CLIENT_ID: self.set_client_id
        }
        self._socket: socket.socket | None = None

    def add_action(self, action: str, function):
        self._actions[action] = function

    def call_action(self, action: Action):
        function = self._actions.get(action.action)
        if function:
            function(**action.args)

    def send_action_to_server(self, action: Action):
        self.send_data(self._socket, action.action_info)

    def start_client(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(self._address)
            self._handle_actions()
            Thread(target=self._listen_server).start()
        except Exception as e:
            print(e)

    def _handle_actions(self):
        data = self.recv_data(self._socket)
        if data:
            data = json.loads(data)
            action = Action.from_dict(data)
            self.call_action(action)

    def _listen_server(self):
        while True:
            self._handle_actions()

    # actions

    def set_client_id(self, client_id: int):
        self._client_id = client_id
