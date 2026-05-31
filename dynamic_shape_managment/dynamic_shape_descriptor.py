class DynamicShapeDescriptor:
    """
    A class representing a dynamic shape including its name, its display name,  the list of its required aruments, and the type itself.
    """
    def __init__(self, shape_name: str, shape_menu_name: str, shape_params: tuple[str], cls):
        """
        Initialize a shape descriptor.

        Args:
            shape_name (str): The name of the shape, also known as shape_type.
            shape_menu_name (str): The display name for this shape.
            shape_params (tuple[str]): A tuple listing the names of arguments required to instanciate this class.
        """
        self.shape_name: str = shape_name
        self.shape_menu_name: str = shape_menu_name
        self.shape_params: tuple[str] = shape_params
        self.cls: type = cls