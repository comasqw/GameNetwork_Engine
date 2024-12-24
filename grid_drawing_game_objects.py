from engine.protocol import GameObject, Action


class Grid(GameObject):
    def __init__(self, object_id: int, *, object_type: str = "Grid",
                 size_x: int, size_y: int, cell_x: int, cell_y: int, grid: dict | None = None):
        self.size_x = size_x
        self.size_y = size_y
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.grid = grid if grid else self._init_grid()
        super().__init__(object_id, object_type, size_x=size_x, size_y=size_y, cell_x=cell_x, cell_y=cell_y,
                         grid=self.grid)

    def _init_grid(self):
        grid = {}
        for x in range(self.size_x // self.cell_x):
            for y in range(self.size_y // self.cell_y):
                grid[f"{x * self.cell_x},{y * self.cell_y}"] = False
        return grid

    def change_cell_status(self, x: int, y: int):
        x = (x // self.cell_x) * self.cell_x
        y = (y // self.cell_y) * self.cell_y

        key_str = f"{x},{y}"
        if key_str in self.grid:
            self.grid[key_str] = not self.grid[key_str]

# actions


SET_GRID = "SetGrid"
GET_GRID = "GetGrid"
CHANGE_GRID_CELL_STATUS = "ChangeGridCellStatus"
UPDATE_GRID_CELL_STATUS = "UpdateGridCellStatus"


class ActionSetGrid(Action):
    def __init__(self, grid_info):
        super().__init__(SET_GRID, grid_info=grid_info)


class ActionGetGrid(Action):
    def __init__(self, client_id: int):
        super().__init__(GET_GRID, client_id=client_id)


class ActionChangeGridCellStatus(Action):
    def __init__(self, client_id: int, x: int, y: int):
        super().__init__(CHANGE_GRID_CELL_STATUS, client_id=client_id, x=x, y=y)


class ActionUpdateGridCellStatus(Action):
    def __init__(self, x: int, y: int):
        super().__init__(UPDATE_GRID_CELL_STATUS, x=x, y=y)
