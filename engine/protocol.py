import uuid


class GameObject:
    def __init__(self, object_id: int, object_type: str, **kwargs):
        self._object_id = object_id
        self._object_type = object_type
        self._object_info = {
            "object_id": object_id,
            "object_type": object_type,
            **kwargs
        }

    @classmethod
    def from_dict(cls, object_info: dict):
        return cls(**object_info)

    @property
    def object_id(self):
        return self._object_id

    @property
    def object_type(self):
        return self._object_type

    @property
    def object_info(self):
        return self._object_info

    def update_object_attr(self, key, value):
        if key in ("id", "type"):
            return
        self._object_info[key] = value

    def __repr__(self):
        return str(self._object_info)


class GameObjectsManager:
    def __init__(self):
        self._game_objects: dict[int, GameObject] = {}

    @property
    def game_objects(self):
        return self._game_objects

    def generate_object_id(self):
        object_id = uuid.uuid4().int

        while object_id in self._game_objects:
            object_id = uuid.uuid4().int

        return object_id

    def add_game_object(self, game_object: GameObject):
        if game_object.object_id in self._game_objects:
            return

        self._game_objects[game_object.object_id] = game_object

    def add_game_object_from_dict(self, object_info: dict):
        game_object = GameObject.from_dict(object_info)
        self.add_game_object(game_object)

    def create_game_object(self, object_type: str, **kwargs):
        game_object = GameObject(self.generate_object_id(), object_type, **kwargs)
        self.add_game_object(game_object)

    def remove_game_object(self, object_id: int):
        if object_id in self._game_objects:
            del self._game_objects[object_id]

    def get_object(self, object_id: int):
        if object_id in self._game_objects:
            return self._game_objects[object_id]

    def get_objects_with_attr(self, key, value) -> list[int]:
        game_objects = []
        for game_object in self._game_objects.values():
            attr = game_object.object_info.get(key)
            if attr == value:
                game_objects.append(game_object.object_id)

        return game_objects


class Action:
    def __init__(self, action: str, **kwargs):
        self._action = action
        self._args = kwargs
        self._action_info = {
            "action": action,
            **kwargs
        }

    @classmethod
    def from_dict(cls, action_info: dict):
        return Action(**action_info)

    def __repr__(self):
        return str(self._action_info)

    @property
    def action(self):
        return self._action

    @property
    def args(self):
        return self._args

    @property
    def action_info(self):
        return self._action_info

# base actions


SET_CLIENT_ID = "SetClientId"


class ActionSetClientId(Action):
    def __init__(self, client_id: int):
        super().__init__(SET_CLIENT_ID, client_id=client_id)
