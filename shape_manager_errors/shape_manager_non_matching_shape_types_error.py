from .shape_manager_base_error import ShapeManagerBaseError


class ShapeManagerNonMatchingShapeTypesError(ShapeManagerBaseError):
    """
    Raised when an update is applied to a shape of another type.
    """
    pass
