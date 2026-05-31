from menu.main_menu import MainMenu
from menu.shape_selection_menu import ShapeSelectionMenu
from shape_manager import ShapeManager
from utils.utils import get_positive_int, get_params_list
from utils.app_states import AppStates
from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager
from app_logger import get_logger


class App:
    """
    The main app manager.
    """
    def __init__(self):
        """
        Initialize the app.

        Sets up app states, menus and shape manager.
        """
        self.state = AppStates.starting
        self.logger = get_logger("app")
        self.logger.info("booting up...")
        self.logger.debug("setting up shape manager.")
        self.shape_manager = ShapeManager()
        self.logger.debug("setting up main menu.")
        self.main_menu = MainMenu()
        self.logger.debug("setting up shape selection menu.")
        self.shape_selection_menu = ShapeSelectionMenu()
        self.state = AppStates.ready
        self.logger.info("system ready.")

    def run(self):
        """
        main app loop (event loop).

        runs the actual app.
        """
        self.state = AppStates.running
        while self.state == AppStates.running:
            action = self.main_menu.execute_menu()
            self.logger.debug(f"running selected action. action: {action.action_name}")
            action.action(self)

        self.state = AppStates.exiting
        self.logger.info("shutting down.")
