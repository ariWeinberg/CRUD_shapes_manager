import os
import importlib
from app_logger import get_logger

from . import create_shape
from . import list_all_shapes
from . import update_shape
from . import delete_shape


__all__ = [
    "create_shape",
    "list_all_shapes",
    "update_shape",
    "delete_shape",
]
# uncomment to enforce order.

# from . import search_shape_by_id
# from . import filter_by_shape_type
# from . import sort_by_area
# from . import compare_two_shapes
# from . import delete_all_shapes


def load_all_actions():
    """
    load all dynamic actions
    """
    logger = get_logger("dynamic_actions_init")

    for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__))):

        if file_name.endswith(".py") and file_name != os.path.basename(__file__) and file_name != "exit_.py":
            module_name = file_name[:-3]
            try:
                # Use relative import notation (note the leading dot) and pass the package name
                importlib.import_module(f".{module_name}", package="dynamic_actions")
                __all__.append(module_name)
                logger.info(f"Successfully imported: {module_name}")
            except Exception as e:
                logger.warning(f"Failed to import {module_name}: {e}")


load_all_actions()
from . import exit_
__all__.append("exit_")
