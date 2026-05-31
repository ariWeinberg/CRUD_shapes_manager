class ShapeManagerBaseError(Exception):
    """
    Base class for all app-specific errors.
    """
    def __init__(self, *args):
        super().__init__(*args)
