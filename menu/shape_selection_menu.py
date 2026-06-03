from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager, DynamicShapeDescriptor
from shape_manager_errors import ShapeManagerInputIterationsError
from app_logger import get_logger


class ShapeSelectionMenu:
    """
    A class for managing and running a menu for the user to select a shape type.
    """
    def __init__(
            self,
            prompt_template: str = "please select an option:\n{menu_lines}\ntype your selection number: ",
            invalid_input_retry_prompt: str = "please enter a valid option: ",
            max_input_iterations: int = 20,
            ):
        """
        Initialize the shape selection menu.

        Setup the list of options and other setting of the menu.

        Args:
            prompt_template (str | None): the prompt to show the user with a placeholder for `menu_lines`.
            invalid_input_retry_prompt (str | None): A retry prompt to display after invalid inputs.
            max_input_iterations (int | None): the maximum number of invalid inputs to tolarate before raising an exception.
        """
        self.logger = get_logger("shape_selection_menu")
        self.logger.debug("setting up shape selection menu.")

        self.menu_options: dict = {str(k): (v.shape_menu_name, v) for k, v in enumerate(DynamicShapeTypeManager.shape_descriptors, 1)}

        self.prompt_template: str = prompt_template
        self.invalid_input_retry_prompt = invalid_input_retry_prompt
        self.max_input_iterations: int = max_input_iterations

        self.logger.debug("shape selection menu is ready.")

    def display_menu(self):
        """
        Display the shape selection menu.
        """
        self.logger.debug("displaying shape selection menu.")
        menu_lines = "\n".join([f'{op}. {op_value[0]}.' for op, op_value in self.menu_options.items()])
        print(self.prompt_template.format(menu_lines=menu_lines), end="")

    def is_valid_input(self, choice: str) -> bool:
        """
        Test if the input is a valid choice out of the menu options.

        Args:
            choice (str): The input to validate.

        Returns:
            bool: Whether the input was valid or not.
        """
        self.logger.debug(f"validating input. input: {choice}")
        if choice in self.menu_options.keys():
            return True
        return False

    def get_input(self) -> str:
        """
        Get a user selection input.

        Repeatedly get input from the user until a valid input is enterd.

        Returns:
            str: The validated input.
        """
        self.logger.debug("getting user input.")
        choice = ""
        iteration_counter = 0
        while iteration_counter < self.max_input_iterations and not self.is_valid_input(choice):
            choice = input(self.invalid_input_retry_prompt if iteration_counter > 0 else "")
            iteration_counter += 1

        if iteration_counter >= self.max_input_iterations:
            self.logger.error("too many invalid inputs.")
            raise ShapeManagerInputIterationsError("too many invalid inputs.")

        self.logger.debug(f"got user input. input: {choice}")
        return choice

    def execute_menu(self) -> DynamicShapeDescriptor:
        """
        Execute the shape selection menu.

        Display the menu,
        get input selection,
        validate the input,
        and return the corresponding shape descriptor.

        Returns:
            DynamicShapeDescriptor: the selected shape's descriptor object.
        """
        self.display_menu()
        return self.menu_options[self.get_input()][1]
