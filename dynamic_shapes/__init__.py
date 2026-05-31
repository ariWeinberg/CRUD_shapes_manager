import os
import importlib
from app_logger import get_logger


def load_all_shapes():
    """
    load all dynamic shapes
    """
    logger = get_logger("dynamic_shapes")

    for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__))):

        if file_name.endswith(".py") and file_name != os.path.basename(__file__):
            module_name = file_name[:-3]
            try:
                # Use relative import notation (note the leading dot) and pass the package name
                importlib.import_module(f".{module_name}", package="dynamic_shapes")
                logger.info(f"Successfully imported: {module_name}")
            except Exception as e:
                logger.warning(f"Failed to import {module_name}: {e}")

load_all_shapes()
