from .shape_manager_base_error import ShapeManagerBaseError


class ShapeManagerDuplicateShapeIdError(ShapeManagerBaseError):
    """
    Raised when trying to create a shape with an id that already exists.
    """
    pass
