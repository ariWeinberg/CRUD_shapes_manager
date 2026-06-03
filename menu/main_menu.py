from dynamic_actions_managment.dynamic_action_manager import DynamicActionTypeManager
from dynamic_actions_managment.dynamic_action_descriptor import DynamicActionDescriptor
from app_logger import get_logger


class MainMenu:
    """
    Manages and displays the main menue for the app
    """
    def __init__(
            self,
            prompt_template: str = "\n_________________________________\nWelcome to CRUD shape manager.\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\nwhat would you like to do today?\n{menu_lines}\n\nplease type the number of the option you want: ",
            invalid_input_retry_prompt: str = "please enter a valid option: ",
            max_input_iterations: int = 20,
            ):
        """
        Initialize the main menu.

        Setup the list of options and other setting of the menu.

        Args:
            menu_options (dict | None):
            prompt_template (str | None):
            invalid_input_retry_prompt (str | None):
            max_input_iterations (int | None):
        """
        self.logger = get_logger("main_menu")
        self.logger.debug("setting up main menu.")

        self.menu_options: dict = {str(k): (v.action_menu_name, v) for k, v in enumerate(DynamicActionTypeManager.action_descriptors, 1)}

        self.prompt_template: str = prompt_template
        self.invalid_input_retry_prompt = invalid_input_retry_prompt
        self.max_input_iterations: int = max_input_iterations

        self.logger.debug("main menu is ready.")

    def display_menu(self):
        """
        Display the shape selection menu.
        """
        self.logger.debug("displaying main menu.")
        menu_lines = "\n".join([f'{op}. {op_value[0]}.' for op, op_value in self.menu_options.items()])

        print(self.prompt_template.format(menu_lines=menu_lines), end="")

    def is_valid_input(self, choice: str) -> bool:
        """
        Display the shape selection menu.

        Args:
            choice (str): Test if the input is a valid choice out of the menu options.

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
            raise RuntimeError("too many invalid inputs.")

        self.logger.debug(f"got user input. input: {choice}")
        return choice

    def execute_menu(self) -> DynamicActionDescriptor:
        """
        Execute the main menu.

        Display the menu,
        get input selection,
        validate the input,
        and return the corresponding action descriptor.

        Returns:
            DynamicActionDescriptor: the selected action's descriptor object.
        """
        self.display_menu()
        return self.menu_options[self.get_input()][1]
