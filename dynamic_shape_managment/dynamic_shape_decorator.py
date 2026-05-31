from collections.abc import Callable
from shape_manager_errors import ShapeManagerArgumentTypeError
from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager
from app_logger import get_logger

def dynamic_shape(
        shape_name: str,
        shape_menu_name: str,
        shape_params: tuple[str, ...]
        ) -> Callable[[type], type]:
    """
    A decorator to register a DynamicShape class into the system.

    Registers the decorated class into DynamicShapeTypeManager.

    Args:
        shape_name (str): The name of the shape, also known as shape_type.
        shape_menu_name (str): The display name for this shape.
        shape_params (tuple[str, ...]): A tuple of the parameter names required to create an instance of this shape. (for now all are assumed to be integers.).

    Returns:
        Callable[[type], type]: The actual wrapper.

    Raises:
        ShapeManagerArgumentTypeError: Raised if any of the Arguments is of incorrect type.
    """
    logger = get_logger("dynamic_shape_managment")
    if not isinstance(shape_name, str):
        logger.warning('`shape_name` must be a string.')
        raise ShapeManagerArgumentTypeError('`shape_name` must be a string.')
    if not isinstance(shape_menu_name, str):
        logger.warning('`shape_menu_name` must be a string.')
        raise ShapeManagerArgumentTypeError('`shape_menu_name` must be a string.')
    if not isinstance(shape_params, tuple):
        logger.warning('`shape_params` must be a tuple.')
        raise ShapeManagerArgumentTypeError('`shape_params` must be a tuple.')
    
    for param in shape_params:
        if not isinstance(param, str):
            logger.warning('All values in `shape_params` must be strings.')
            raise ShapeManagerArgumentTypeError('All values in `shape_params` must be strings.')
    
    def wrapper(cls: type) -> type:
        """
        The actual wrapper for a DynamicShape class.

        Basically it just registers the shape and returns the original class.

        Returns:
            type: The original class.
        """
        logger.info(f"registering shape: {shape_name}")
        logger.debug(f"registering shape: {shape_name}, {shape_menu_name}, {shape_params}")
        
        DynamicShapeTypeManager.register_shape(
            shape_name=shape_name,
            shape_menu_name=shape_menu_name,
            shape_params=shape_params,
            shape_cls=cls
        )
        return cls
    return wrapper
    