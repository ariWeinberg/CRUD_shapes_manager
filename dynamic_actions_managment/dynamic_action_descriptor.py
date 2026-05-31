from collections.abc import Callable


class DynamicActionDescriptor:
    """
    A class representing a dynamic action including its name, its display name, and the function itself.
    """
    def __init__(self, action_name: str, action_menu_name: str, action: Callable):
        """
        Initialize a action descriptor.

        Args:
            action_name (str): The name of the shape, also known as shape_type.
            action_menu_name (str): The display name for this shape.
        """
        self.action_name: str = action_name
        self.action_menu_name: str = action_menu_name
        self.action: type = action