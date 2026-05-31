# from shapes.shape_types import ShapeTypes
from dynamic_shape_managment.shape import Shape
from dynamic_shape_managment.dynamic_shape_decorator import dynamic_shape
from numbers import Real
import math


@dynamic_shape(shape_name='rectangle', shape_menu_name='Rectangle', shape_params=('width', 'height',))
class Rectangle(Shape):
    """a class representing a rectangle shape."""
    def __init__(self, width: int, height: int, shape_id: int | None = None):
        """
        Initialize a rectangle instance.

        includes validation.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            shape_id (int | None): The shape id, leave None for auto-generation.

        Raises:
            ValueError: Raised if one of its argument values is invalid.
            TypeError: Raised if one of its arguments has an invalid type.
        """
        self.validate_params(width, height)
        super().__init__("rectangle", shape_id)
        """initialize the rectangle by using the base initializer and setting `width` and `height`."""        

        self.width = width
        self.height = height

    def validate_params(self, width, height):
        sides = (width, height)
        if not all(isinstance(side, Real) for side in sides):
            raise TypeError("Rectangle sides must be Real numbers.")
        if not all(math.isfinite(side) for side in sides):
            raise ValueError("Rectangle sides must be Finite numbers.")
        if not all(side > 0 for side in sides):
            raise ValueError("Rectangle sides must be positive.")
        
    def get_area(self):
        """calculate the area of the rectangle. formula: `width` times `height`"""
        self.validate_params(width=self.width, height=self.height)
        return self.width * self.height

    def get_perimeter(self):
        """calculate the perimeter of the rectangle. formula: (`width` plus `height`) times 2"""
        self.validate_params(width=self.width, height=self.height)
        return (self.width + self.height) * 2


if __name__ == "__main__":
    valid_test_values = [
        ("Square", 5, 5, 25, 20),
        ("Oblong rectangle", 4, 6, 24, 20),
        ("Oblong rectangle (extream aspect)", 100, 1, 100, 202),
        ("Oblong rectangle (floats)", 2.5, 4.5, 11.25, 14),
        ("Square (large numbers)", 1e6, 1e6, 1000000000000.0, 4000000.0),
        ("Square (tiny numbers)", 1e-5, 1e-5, 1.0000000000000002e-10,4e-05),
    ]
    invalid_test_values = [
        ("Zero param", 0, 5, ValueError),
        ("Negative dimension", -3, 4, ValueError),
        ("Type Mismatch", "5", 5, TypeError),
        ("Missing data", None, 4.5, TypeError),
        ("Infinite bounds", float('inf'), 1e6, ValueError),
        ("Not a number", float('nan'), 1e-5, ValueError),
    ]

    for test_name, width, height, expected_area, expected_perimeter in valid_test_values:
        print(f"testing valid case: {test_name}.")
        test_rectangle = Rectangle(width=width, height=height)
        assert test_rectangle.get_area() == expected_area
        assert test_rectangle.get_perimeter() == expected_perimeter
        print(f"test case: {test_name}. passed successfuly")


    for test_name, width, height, expected_exception in invalid_test_values:
        print(f"testing invalid case: {test_name}.")
        exc = None
        try:
            test_rectangle = Rectangle(width=width, height=height)
        except Exception as e:
            exc = e
        assert isinstance(exc, expected_exception)
        print(f"test case: {test_name}. passed successfuly")

    print("all tests passed successfully.")