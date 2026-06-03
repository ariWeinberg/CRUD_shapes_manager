from .dynamic_shape_descriptor import DynamicShapeDescriptor
from shape_manager_errors import *
from app_logger import get_logger

class DynamicShapeTypeManager:
    """
    A simple class managing the dynamic shapes, allowing for registration of new shapes and fetching of existing ones.
    """
    shape_descriptors: list[DynamicShapeDescriptor] = []
    shape_name_to_descriptor_map: dict[str, DynamicShapeDescriptor] = {}
    logger = get_logger("dynamic_shape_managment")

    @classmethod
    def register_shape(cls, shape_name: str, shape_menu_name: str, shape_params: tuple[str, ...], shape_creation_model, shape_update_model, shape_response_model, shape_cls: type):
        """
        Register a new shape type into the system.

        Args:
            shape_name (str): The name of the shape (also known as shape_type.).
            shape_menu_name (str): The display name for the shape.
            shape_params (tuple[str, ...]): A tuple listing the names of arguments required to instanciate this shape.
            shape_cls (type): The shape class itself.
        """
        # missing validation for: valid shape, not duplicate.
        descriptor = DynamicShapeDescriptor(
            shape_name=shape_name,
            shape_menu_name=shape_menu_name,
            shape_params=shape_params,
            shape_creation_model=shape_creation_model,
            shape_update_model=shape_update_model,
            shape_response_model=shape_response_model,
            cls=shape_cls)
        cls.shape_descriptors.append(descriptor)
        cls.shape_name_to_descriptor_map[shape_name] = descriptor
        cls.logger.info(f"successfully registerd shape: {shape_name}")

    @classmethod
    def get_shape_descriptor(cls, shape_name: str) -> DynamicShapeDescriptor:
        """
        Fetch a shape descriptor by its name.

        Args:
            shape_name (str): The name (type) of the shape to look for itsw descriptor.

        Returns:
            DynamicShapeDescriptor: The found shape descriptor.
        """
        cls.logger.debug(f"Fetching shape: {shape_name}")
        if shape_name in cls.shape_name_to_descriptor_map.keys():
            cls.logger.debug(f"Found shape: {shape_name}")
            return cls.shape_name_to_descriptor_map[shape_name]
        cls.logger.warning(f"shape: {shape_name} was not found.")
        raise ShapeManagerShapeTypeNotFoundError()
