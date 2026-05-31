# CRUD Shapes Project

A command-line Python application for creating, reading, updating, deleting, searching, filtering, sorting, and comparing geometric shapes.

The project stores shapes in a local JSON file and uses decorators to register shape types and menu actions dynamically.

## Features

- Create shapes through an interactive CLI menu.
- List all saved shapes.
- Update or delete shapes by ID.
- Search for a shape by ID.
- Filter shapes by type.
- Sort shapes by area.
- Compare two shapes by area and perimeter.
- Persist shape data in `shapes.json`.
- Add new shape types or actions without changing the menu code.

## Requirements

- Python 3.10 or newer.
- No third-party Python packages are required.

## Project Structure

```text
.
├── main.py                         # Program entry point
├── app.py                          # Main application loop
├── shape_manager.py                # Shape persistence and CRUD logic
├── shapes.json                     # JSON datastore
├── app_logger.py                   # Logging setup
├── dynamic_shapes/                 # Built-in shape implementations
├── dynamic_shape_managment/        # Shape base class, descriptors, registry, decorator
├── dynamic_actions/                # CLI action handlers
├── dynamic_actions_managment/      # Action descriptors, registry, decorator
├── menu/                           # Main menu and shape selection menu
├── shape_manager_errors/           # Custom exception classes
└── utils/                          # Input helpers and app state enum
```

## Running the App

From the project root:

```bash
python3 main.py
```

The app opens an interactive menu. Type the number of the action you want to run and follow the prompts.

## Data Storage

Shapes are stored in `shapes.json`.

Each saved shape has this structure:

```json
{
  "shape_id": 1,
  "shape_type": "circle",
  "shape_params": {
    "radius": 5
  }
}
```

When the app starts, `ShapeManager` loads the file and rebuilds shape objects using the registered dynamic shape types.

## Built-In Shapes

The application currently includes:

| Shape | Parameters | Area | Perimeter |
| --- | --- | --- | --- |
| Circle | `radius` | `pi * radius^2` | `2 * pi * radius` |
| Square | `side` | `side^2` | `4 * side` |
| Rectangle | `width`, `height` | `width * height` | `2 * (width + height)` |
| Triangle | `side_a`, `side_b`, `side_c` | Heron's formula | `side_a + side_b + side_c` |

All dimensions must be positive finite real numbers. Triangle dimensions must also satisfy the triangle inequality.

## Built-In Actions

The menu actions are registered dynamically from files in `dynamic_actions/`.

Available actions include:

- Create shape
- List all shapes
- Update shape
- Delete shape
- Search shape by ID
- Filter by shape type
- Sort by area
- Compare two shapes
- Delete all shapes
- Exit

## How Dynamic Registration Works

Shape modules are imported from `dynamic_shapes/__init__.py`. Each shape class uses the `@dynamic_shape` decorator, which registers it with `DynamicShapeTypeManager`.

Action modules are imported from `dynamic_actions/__init__.py`. Each action function uses the `@dynamic_action` decorator, which registers it with `DynamicActionTypeManager`.

The menus read from those registries, so newly registered shapes and actions automatically become available.

## Adding a New Shape

Create a new file in `dynamic_shapes/`, for example `dynamic_shapes/pentagon.py`:

```python
from dynamic_shape_managment.dynamic_shape_decorator import dynamic_shape
from dynamic_shape_managment.shape import Shape


@dynamic_shape(
    shape_name="pentagon",
    shape_menu_name="Pentagon",
    shape_params=("side",),
)
class Pentagon(Shape):
    def __init__(self, side: int, shape_id: int | None = None):
        if side <= 0:
            raise ValueError("Pentagon side must be positive.")

        super().__init__("pentagon", shape_id)
        self.side = side

    def get_area(self):
        return 1.72048 * self.side ** 2

    def get_perimeter(self):
        return self.side * 5
```

Restart the app. The new shape should appear in the shape selection menu.

## Adding a New Action

Create a new file in `dynamic_actions/`, for example `dynamic_actions/count_shapes.py`:

```python
from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("count_shapes", "count shapes")
def handle_count_shapes(app: App):
    print(len(list(app.shape_manager.get_all_shapes())))
```

Restart the app. The new action should appear in the main menu.

## Logs

The logger writes rotating log files in the project root:

- `debug.log`
- `info.log`
- `warning.log`

These files are useful for debugging registration, menu flow, and persistence issues.

## Running Shape Self-Tests

Some shape modules include simple self-tests under `if __name__ == "__main__"`.

Examples:

```bash
python3 dynamic_shapes/circle.py
python3 dynamic_shapes/square.py
python3 dynamic_shapes/rectangle.py
python3 dynamic_shapes/triangle.py
```

## Notes

- `shapes.json` must exist and contain either valid JSON or an empty JSON-compatible value before the app loads it.
- Input helpers currently collect positive whole numbers from the CLI, even though shape constructors can accept real numbers.
- Shape and action menu order depends on dynamic import order from the filesystem, except for the explicitly imported default action modules.
