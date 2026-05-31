from .dynamic_action_descriptor import DynamicActionDescriptor
from collections.abc import Callable

class DynamicActionTypeManager:
    """
    A simple class managing the dynamic actions, allowing for registration of new actions and fetching of existing ones.
    """
    action_descriptors: list[DynamicActionDescriptor] = []
    action_name_to_descriptor_map: dict[str, DynamicActionDescriptor] = {}

    @classmethod
    def register_action(cls, action_name: str, action_menu_name: str, action: Callable):
        """
        Register a new action type into the system.

        Args:
            action_name (str): The name of the action.
            action_menu_name (str): The display name for the action.
            action (type): The action function itself.
        """
        # missing validation for: valid action, not duplicate.
        descriptor = DynamicActionDescriptor(
            action_name=action_name,
            action_menu_name=action_menu_name,
            action=action
            )
        cls.action_descriptors.append(descriptor)
        cls.action_name_to_descriptor_map[action_name] = descriptor

    @classmethod
    def get_action_descriptor(cls, action_name: str) -> DynamicActionDescriptor:
        """
        Fetch a action descriptor by its name.

        Args:
            action_name (str): The name of the action to look for its descriptor.

        Returns:
            DynamicActionDescriptor: The found action descriptor.
        """
        return cls.action_name_to_descriptor_map[action_name]
