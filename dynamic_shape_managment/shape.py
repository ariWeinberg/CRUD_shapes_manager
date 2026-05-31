from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager


class Shape:
    """
    The most basic representation of a shape.

    Attributes:
        shape_id (int): An auto-increamented id for each shape.
        shape_type (str): The name of the shape.
    """
    next_shape_id: int = 0  # the next avilable id for a shape
    shape_ids: set[int] = set()  # all the used ids (needed for validation - no duplicate ids.)

    def __init__(self, shape_type: str, shape_id: int | None = None):
        """
        base initialization method for every shape.

        handles shape_id generation and assignment.
        handles shape_type assignment.

        Args:
            shape_type (str): The nme of the shape_type.
            shape_id (int | None): The shape_id for this shape, default to None - generate id.

        Raises:
            ValueError: raised when initializing with a shape id thats already taken.
        """
        if shape_id in Shape.shape_ids:
            raise ValueError(f"a shape with id {shape_id} already exists.")

        if shape_id is None:
            shape_id = Shape.next_shape_id
            Shape.next_shape_id += 1

        Shape.shape_ids.add(shape_id)

        self.shape_id = shape_id
        self.shape_type = shape_type

    def get_area(self):
        """
        MUST be overriden by EVERY inheriting class.

        This is a place holder method for shape methods that calculate the area of the shape.

        Raises:
            NotImplementedError: you must override this function in every inheriting class
        """
        raise NotImplementedError

    def get_perimeter(self):
        """
        MUST be overriden by EVERY inheriting class.

        This is a place holder method for shape methods that calculate the perimeter of the shape.

        Raises:
            NotImplementedError: you must override this function in every inheriting class
        """
        raise NotImplementedError

    def to_dict(self):
        """
        MUST be overriden by EVERY inheriting class.
        return the dict representation of the shape.
        must be sufficient for recreate.
        """
        shape_descriptor = DynamicShapeTypeManager.get_shape_descriptor(shape_name=self.shape_type)
        return {
            'shape_id': self.shape_id,
            'shape_type': self.shape_type,
            'shape_params': {
                k: self.__dict__[k] for k in shape_descriptor.shape_params
            }
        }
    
    def __str__(self):
        """return a human readable representation of the circle."""
        shape_descriptor = DynamicShapeTypeManager.get_shape_descriptor(shape_name=self.shape_type)

        return f"""
-----------------------
ID:{self.shape_id}
Shape Type: {self.shape_type}
{'\n'.join(f"{k.capitalize()}: {self.__dict__[k]}" for k in shape_descriptor.shape_params)}
Area: {self.get_area():.2f}
Perimeter: {self.get_perimeter():.2f}
-----------------------"""

    def __del__(self):
        """
        Remove the id of this shape from the list of ocupied ids when deleted by GC (or manualy).
        """
        shape_id = getattr(self, "shape_id", None)
        if shape_id:
            Shape.shape_ids.remove(shape_id)
