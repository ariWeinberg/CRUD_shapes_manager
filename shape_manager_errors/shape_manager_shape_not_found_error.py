from .shape_manager_base_error import ShapeManagerBaseError


class ShapeManagerShapeNotFoundError(ShapeManagerBaseError):
    """
    Raised when trying to access a shape with an id that doesnt exist.
    """
    pass
