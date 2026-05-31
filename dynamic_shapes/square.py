from dynamic_shape_managment.dynamic_shape_decorator import dynamic_shape
from dynamic_shape_managment.shape import Shape
import math
from numbers import Real

@dynamic_shape(shape_name="square", shape_menu_name="Square", shape_params=("side",))
class Square(Shape):
    """a class representing a square shape."""
    def __init__(self, side: int, shape_id: int | None = None):
        """
        initialize the square by using the base initializer and setting `side`

        Args:
            side (int): The size of the square's side.
            shape_id (int | None): The shape id, leave None for auto-generation.

        Raises:
            ValueError: Raised if one of its argument values is invalid.
            TypeError: Raised if one of its arguments has an invalid type.
        """
        self.validate_params(side)
        
        super().__init__("square", shape_id)
        self.side = side

    def validate_params(self, side):
        if not isinstance(side, Real):
            raise TypeError("Rectangle sides must be Real numbers.")
        if not math.isfinite(side):
            raise ValueError("Rectangle sides must be Finite numbers.")
        if not (side > 0):
            raise ValueError("Rectangle sides must be positive.")

    def get_area(self):
        self.validate_params(side=self.side)
        """calculate the area of the square. formula: 'side' to the power of 2"""
        return self.side ** 2

    def get_perimeter(self):
        """calculate the perimeter of the square. formula: 'side' times 4"""
        self.validate_params(side=self.side)
        return self.side * 4

if __name__ == "__main__":
    valid_test_values = [
        ("Unit square", 1, 1, 4),
        ("non-Unit square", 5, 25.0, 20),
        ("float", 2.5, 6.25, 10),
        ("large number", 1e6, 1000000000000.0, 4000000.0),
        ("tiny number", 1e-5, 1.0000000000000002e-10, 4e-05),
    ]
    invalid_test_values = [
        ("Zero param", 0, ValueError),
        ("Negative dimension", -5, ValueError),
        ("Type Mismatch", "5", TypeError),
        ("Missing data", None, TypeError),
        ("Infinite bounds", float('inf'), ValueError),
        ("Not a number", float('nan'), ValueError),
    ]

    for test_name, side, expected_area, expected_perimeter in valid_test_values:
        print(f"testing valid case: {test_name}.")
        test_square = Square(side=side)
        print(test_square.get_area())
        print(test_square.get_perimeter())
        assert test_square.get_area() == expected_area
        assert test_square.get_perimeter() == expected_perimeter
        print(f"test case: {test_name}. passed successfuly")


    for test_name, side, expected_exception in invalid_test_values:
        print(f"testing invalid case: {test_name}.")
        exc = None
        try:
            test_square = Square(side=side)
        except Exception as e:
            exc = e
        assert isinstance(exc, expected_exception)
        print(f"test case: {test_name}. passed successfuly")

    print("all tests passed successfully.")