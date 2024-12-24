from abc import ABC
import json
import socket

CONTENT_LENGTH = "Content-Length"


class Data:
    def __init__(self, data: str):
        self._data = f"{CONTENT_LENGTH}{len(data)}\n{data}"

    def __repr__(self):
        return self._data

    @property
    def data(self):
        return self._data

    @classmethod
    def from_dict(cls, data: dict):
        data = json.dumps(data)
        return Data(data)


class BaseNetworking(ABC):
    @staticmethod
    def recv_data(sock: socket.socket):
        check_protocol = sock.recv(len(CONTENT_LENGTH))

        if check_protocol.decode("utf-8") != CONTENT_LENGTH:
            return

        content_length = b""

        while not content_length.endswith(b"\n"):
            content_length += sock.recv(1)

        content_length = int(content_length)

        data = b""

        while len(data) != content_length:
            data += sock.recv(content_length)

        return data.decode("utf-8")

    @staticmethod
    def send_data(sock: socket.socket, data: Data | str | dict):
        if isinstance(data, dict):
            data = Data.from_dict(data)
        elif isinstance(data, str):
            data = Data(data)

        sock.send(data.data.encode("utf-8"))
