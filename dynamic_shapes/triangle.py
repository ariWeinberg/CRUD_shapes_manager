from __future__ import annotations
import math
from numbers import Real
from typing import Literal
from dynamic_shape_managment.shape import Shape
from dynamic_shape_managment.dynamic_shape_decorator import dynamic_shape
from pydantic import BaseModel, Field, computed_field
import shape_manager_errors

class TriangleCreate(BaseModel):
    shape_type: Literal["triangle"] = "triangle"
    side_a: float = Field(gt=0)
    side_b: float = Field(gt=0)
    side_c: float = Field(gt=0)

    def to_domain(self) -> Triangle:
        return Triangle(side_a=self.side_a, side_b=self.side_b, side_c=self.side_c)
    

class TriangleUpdate(BaseModel):
    shape_type: Literal["triangle"] = "triangle"
    side_a: float | None = Field(default=None, gt=0)
    side_b: float | None = Field(default=None, gt=0)
    side_c: float | None = Field(default=None, gt=0)

    def apply_to_domain(self, triangle: Triangle) -> Triangle:
        update_data = self.model_dump(exclude_unset=True)
        if not isinstance(triangle, Triangle):
            message = f"update to shape Triangle cannot be applied to object of type {type(triangle)}"
            raise shape_manager_errors.ShapeManagerNonMatchingShapeTypesError(message)

        for field_name, value in update_data.items():
            setattr(triangle, field_name, value)

        return

class TriangleResponse(BaseModel):
    shape_type: Literal["triangle"] = "triangle"
    shape_id: int = Field(gt=0)
    side_a: float = Field(gt=0)
    side_b: float = Field(gt=0)
    side_c: float = Field(gt=0)

    @classmethod
    def from_domain(cls, triangle: Triangle) -> TriangleResponse:
        return cls(shape_id=triangle.shape_id, side_a=triangle.side_a, side_b=triangle.side_b, side_c=triangle.side_c)
    
    @computed_field
    @property
    def area(self) -> float:
        semi_perimeter = self.perimeter * 0.5

        diff_a = (semi_perimeter - self.side_a)
        diff_b = (semi_perimeter - self.side_b)
        diff_c = (semi_perimeter - self.side_c)

        squared_area = semi_perimeter * diff_a * diff_b * diff_c

        return round(number=(squared_area ** 0.5), ndigits=2)

    @computed_field
    @property
    def perimeter(self) -> float:
        return (self.side_a + self.side_b + self.side_c)
    
@dynamic_shape(
    shape_name="triangle",
    shape_menu_name="Triangle",
    shape_params=("side_a", "side_b", "side_c",),
    shape_creation_model=TriangleCreate,
    shape_update_model=TriangleUpdate,
    shape_response_model=TriangleResponse,
    )
class Triangle(Shape):
    """a class representing a triangle shape."""

    def __init__(self, side_a: int, side_b: int, side_c: int, shape_id: int | None = None):
        """
        initialize the triangle by using the base initializer and setting `side_a`, `side_b`, and `side_c`

        Validates argument types and values.

        Args:
            side_a (int): First side of the triangle.
            side_b (int): Second side of the triangle.
            side_c (int): Third side of the triangle.
            shape_id (int | None): The shape id, leave None for auto-generation.

        Raises:
            ValueError: Raised if one of its argument values is invalid.
            TypeError: Raised if one of its arguments has an invalid type.
        """
        # validate sides
        self.validate_params(side_a=side_a, side_b=side_b, side_c=side_c)

        super().__init__(shape_type="triangle", shape_id=shape_id)

        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def validate_params(self, side_a, side_b, side_c):
        sides = (side_a, side_b, side_c)
        if not all(isinstance(side, Real) for side in sides):
            raise TypeError("Triangle sides must be Real numbers.")
        if not all(math.isfinite(side) for side in sides):
            raise ValueError("Triangle sides must be Finite numbers.")
        if not all(side > 0 for side in sides):
            raise ValueError("Triangle sides must be positive.")
        if (side_a + side_b <= side_c) or (side_a + side_c <= side_b) or (side_b + side_c <= side_a):
            message = f"Invalid dimensions ({side_a}, {side_b}, {side_c}).\n" + \
                "the sum of any two sides must be greater than the third side."
            raise ValueError(message)
        
    def get_area(self):
        """calculate the area of the triangle. formula: Heron's formula."""
        self.validate_params(side_a=self.side_a, side_b=self.side_b, side_c=self.side_c)
        # to understand the formula refer to Herons formula on wikipedia
        # https://en.wikipedia.org/wiki/Heron%27s_formula
        semi_perimeter = self.get_perimeter() * 0.5

        diff_a = (semi_perimeter - self.side_a)
        diff_b = (semi_perimeter - self.side_b)
        diff_c = (semi_perimeter - self.side_c)

        squared_area = semi_perimeter * diff_a * diff_b * diff_c

        return round(number=(squared_area ** 0.5), ndigits=2)

    def get_perimeter(self):
        """calculate the perimeter of the triangle. formula: sum of `side_a`, `side_b`, `side_c` """
        self.validate_params(side_a=self.side_a, side_b=self.side_b, side_c=self.side_c)
        # simply return the sum of all sides...
        return (self.side_a + self.side_b + self.side_c)


if __name__ == "__main__":
    valid_test_values = [
        ("Equilateral", 5, 5, 5, 10.83, 15),
        ("Isosceles", 5, 5, 8, 12, 18),
        ("Scalene", 4, 5, 6, 9.92, 15),
        ("Extreme aspect ratio", 100, 100, 1, 50, 201),
        ("Floats", 2.5, 3.5, 4.5, 4.35, 10.5),
        ("Large Numbers", 1e6, 1e6, 1e6, 433012701892.22, 3000000.0),
        ("Tiny floats", 1e-5, 1e-5, 1e-5, 0.00, 3.0000000000000004e-05),
    ]
    invalid_test_values = [
        ("Flat line", 2, 3, 5, ValueError),
        ("Disconnected", 2, 3, 10, ValueError),
        ("Infinty", float('inf'), 5, 5, ValueError),
        ("Nan", float('nan'), 5, 5, ValueError),
        ("Data type mismatch", "5", 5, 5, TypeError),
        ("Missing data", None, 5, 5, TypeError),
        ("Complex numbers", 3+4j, 5, 5, TypeError),
    ]

    for test_name, side_a, side_b, side_c, expected_area, expected_perimeter in valid_test_values:
        print(f"testing valid case: {test_name}.")
        test_triangle = Triangle(side_a=side_a, side_b=side_b, side_c=side_c)
        assert test_triangle.get_area() == expected_area
        assert test_triangle.get_perimeter() == expected_perimeter
        print(f"test case: {test_name}. passed successfuly")


    for test_name, side_a, side_b, side_c , expected_exception in invalid_test_values:
        print(f"testing invalid case: {test_name}.")
        exc = None
        try:
            test_triangle = Triangle(side_a=side_a, side_b=side_b, side_c=side_c)
        except Exception as e:
            exc = e
        assert isinstance(exc, expected_exception)
        print(f"test case: {test_name}. passed successfuly")

    print("all tests passed successfully.")

    # Complex numbers
    exc = None
    try:
        test_triangle = Triangle(side_a=3+4j, side_b=5, side_c=5)
    except Exception as e:
        exc = e
    assert isinstance(exc, TypeError)
