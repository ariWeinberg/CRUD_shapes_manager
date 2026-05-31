from collections.abc import Callable
from shape_manager_errors import ShapeManagerArgumentTypeError
from .dynamic_action_manager import DynamicActionTypeManager


def dynamic_action(
        action_name: str,
        action_menu_name: str,
        ) -> Callable[[type], type]:
    """
    A decorator to register a DynamicAction function into the system.

    Registers the decorated function into DynamicActionManager.

    Args:
        action_name (str): The name of the action.
        action_menu_name (str): The display name for this action.

    Returns:
        Callable[[type], type]: The actual wrapper.

    Raises:
        ShapeManagerArgumentTypeError: Raised if any of the Arguments is of incorrect type.
    """
    if not isinstance(action_name, str):
        raise ShapeManagerArgumentTypeError('`action_name` must be a string.')
    if not isinstance(action_menu_name, str):
        raise ShapeManagerArgumentTypeError('`action_menu_name` must be a string.')
    
    def wrapper(action) -> Callable:
        """
        The actual wrapper for a DynamicAction action.

        Basically it just registers the shape and returns the original function.

        Returns:
            Callable: The original function.
        """        
        DynamicActionTypeManager.register_action(
            action_name=action_name,
            action_menu_name=action_menu_name,
            action=action
        )
        return action
    return wrapper
    