from .shape_manager_base_error import ShapeManagerBaseError


class ShapeManagerShapeTypeNotFoundError(ShapeManagerBaseError):
    """
    Raised when an shape is not found when looked for.
    """
    pass
