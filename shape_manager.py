import json
from dynamic_shape_managment.shape import Shape
from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager, DynamicShapeDescriptor
from app_logger import get_logger


class ShapeManager:
    """
    a simple manager for the list of shapes.
    its responsibilities are:
        CRUD operations over the list.
        persistancy over a JSON file as a datastore.
    """
    def __init__(self, filename: str | None = None):
        """
        Initialize the shape manager.

        Args:
            filename (str | None): the filepath to use as the data store.
        """
        self.logger = get_logger("shape_manager")
        self.filename = filename or "shapes.json"

        self.shapes: list[Shape] = []
        self.load_from_json()

    def load_from_json(self):
        """
        lLoad all shapes from json datastore
        """
        self.logger.info("loading all shapes from datastore.")
        shape_ids: set[int] = set()
        with open(self.filename, 'r', encoding='utf-8') as f:
            try:
                shapes_json = json.load(f)
            except json.JSONDecodeError:
                shapes_json = {}

            for shape_item in shapes_json:
                shape_id = shape_item.get("shape_id")
                shape_type = shape_item.get("shape_type")
                shape_params = shape_item.get("shape_params")

                shape = DynamicShapeTypeManager.get_shape_descriptor(
                    shape_name=shape_type
                    ).cls(
                        **shape_params,
                        shape_id=shape_id)

                self.shapes.append(shape)
                shape_ids.add(shape.shape_id)
        Shape.next_shape_id = max((shape_ids or [0])) + 1

    def create_shape(self, shape: Shape):
        """
        Add a new shape to the datastore.

        Adds the shape to the list of shapes and saves to the datastore.
        """
        self.logger.info(f"adding new shape: {shape.shape_id}")
        self.shapes.append(shape)
        self.save_to_json()

    def get_all_shapes(self, type_filter: str | None=None, sort_direction: bool | None=None):
        """
        Get the list of shapes from the datastore.

        get an iterator over all the shapes in the datastore.
        Or alternatively get the sorted version of it or a filterd version based on a supplied shape_type (also known as shape_name.).

        Args:
            type_filter (str | None): the shape_type to filter for.
            sort_direction (bool | None): whether to sort or not and in what direction.
        """
        if type_filter:
            return filter(lambda s: s.shape_type == type_filter, self.shapes)
        if sort_direction:
            return iter(sorted(self.shapes, key=lambda shape: shape.get_area(), reverse=sort_direction))
        return iter(self.shapes)

    def update_shape(self, shape_id: int, new_data: Shape):
        """
        Update a specific shape in the datastore.

        Args:
            shape_id (int): The id of the shape to update.
            new_data (Shape): The updated version of the shape.
        """
        self.logger.info(f"updating shape: {shape_id}")
        self.delete_shape(shape_id)
        new_data.shape_id = shape_id
        Shape.shape_ids.add(shape_id)
        self.create_shape(new_data)

    def delete_shape(self, shape_id: int):
        """
        Delete a shape from the datastore.

        Args:
            shape_id (int): The id of the shape to delete.
        """
        self.logger.info(f"deleting shape: {shape_id}")
        self.shapes[:] = [shape for shape in self.shapes if shape.shape_id != shape_id]
        self.save_to_json()

    def delete_all(self):
        """
        Delete all shapes from the datastore.
        """
        self.logger.info(f"updating all shpaes.")
        self.shapes = []
        self.save_to_json()

    def get_shape_by_id(self, shape_id: int) -> Shape:
        """
        Get a specific shape from the datastore by its id.

        Args:
            shape_id (int): The id of the shape to get.

        Returns:
            Shape: The found shape.

        Raises:
            ValueError: Raised if no shape is found with a matching shape_id.
        """
        self.logger.info(f"fetching shape: {shape_id}")
        for shape in self.shapes:
            if shape.shape_id == shape_id:
                return shape
        message = f"no shape with id: {shape_id} was found"
        raise ValueError(message)

    def save_to_json(self):
        """
        save all shapes to the datastore.
        """
        self.logger.info("saving changes to datastore.")
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([shape.to_dict() for shape in self.shapes], f, indent=4)
