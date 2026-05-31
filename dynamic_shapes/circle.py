# from shapes.shape_types import ShapeTypes
from dynamic_shape_managment.shape import Shape
from math import pi
from dynamic_shape_managment.dynamic_shape_decorator import dynamic_shape
import math
from numbers import Real

@dynamic_shape(shape_name="circle", shape_menu_name="Circle", shape_params=("radius",))
class Circle(Shape):
    """a class representing a circle shape."""
    def __init__(self, radius: int, shape_id: int | None = None):
        """
        initialize the circle by using the base initializer and setting `radius`

        Args:
            radius (int): The radius for this circle.
            shape_id (int | None): The shape id, leave None for auto-generation.

        Raises:
            ValueError: Raised if one of its argument values is invalid.
            TypeError: Raised if one of its arguments has an invalid type.
        """
        self.validate_params(radius=radius)
        
        super().__init__("circle", shape_id)

        self.radius = radius
    
    def validate_params(self, radius):
        if not isinstance(radius, Real):
            raise TypeError("Rectangle sides must be Real numbers.")
        if not math.isfinite(radius):
            raise ValueError("Rectangle sides must be Finite numbers.")
        if not radius > 0:
            raise ValueError("Rectangle sides must be positive.")
        
    def get_area(self):
        """calculate the area of the circle. formula: `radius` to the power of 2 times `pi`"""
        self.validate_params(radius=self.radius)
        return round(number=((self.radius ** 2) * pi), ndigits=2)

    def get_perimeter(self):
        """calculate the perimeter of the circle. formula: `radius` times 2 times `pi`"""
        self.validate_params(radius=self.radius)
        return round(number=((self.radius * 2) * pi), ndigits=2)


if __name__ == "__main__":
    valid_test_values = [
        ("Unit circle", 1, 3.14, 6.28),
        ("non-Unit circle", 5, 78.54, 31.42),
        ("float", 2.5, 19.63, 15.71),
        ("large number", 1e6, 3141592653589.79, 6283185.31),
        ("tiny number", 1e-5, 0.0, 0.0),
    ]
    invalid_test_values = [
        ("Zero param", 0, ValueError),
        ("Negative dimension", -5, ValueError),
        ("Type Mismatch", "5", TypeError),
        ("Missing data", None, TypeError),
        ("Infinite bounds", float('inf'), ValueError),
        ("Not a number", float('nan'), ValueError),
    ]

    for test_name, radius, expected_area, expected_perimeter in valid_test_values:
        print(f"testing valid case: {test_name}.")
        test_circle = Circle(radius=radius)
        assert test_circle.get_area() == expected_area
        assert test_circle.get_perimeter() == expected_perimeter
        print(f"test case: {test_name}. passed successfuly")


    for test_name, radius, expected_exception in invalid_test_values:
        print(f"testing invalid case: {test_name}.")
        exc = None
        try:
            test_circle = Circle(radius=radius)
        except Exception as e:
            exc = e
        assert isinstance(exc, expected_exception)
        print(f"test case: {test_name}. passed successfuly")

    print("all tests passed successfully.")
