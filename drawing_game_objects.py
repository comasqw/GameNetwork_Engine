from engine.protocol import GameObject, Action


class Dot(GameObject):
    def __init__(self, object_id: int, *, object_type: str = "Dot", x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.color = color
        super().__init__(object_id, object_type, x=x, y=y, color=color)

# actions


GET_ALL_DOTS = "GetAllDots"
SET_ALL_DOTS = "SetAllDots"
ADD_DOT = "AddDot"
SET_DOT = "SetDot"


class ActionGetAllDots(Action):
    def __init__(self, client_id: int):
        super().__init__(GET_ALL_DOTS, client_id=client_id)


class ActionSetAllDots(Action):
    def __init__(self, dots: list[Dot]):
        dots = [dot.object_info for dot in dots]
        super().__init__(SET_ALL_DOTS, dots=dots)


class ActionAddDot(Action):
    def __init__(self, client_id: int, x: int, y: int, color: tuple):
        super().__init__(ADD_DOT, client_id=client_id, x=x, y=y, color=color)


class ActionSetDot(Action):
    def __init__(self, dot: Dot):
        super().__init__(SET_DOT, dot=dot.object_info)
