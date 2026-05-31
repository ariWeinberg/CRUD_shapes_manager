from shape_manager_errors import *


MAX_INPUT_ITERATIONS = 20


def get_positive_int(prompt: str, zero_is_valid: bool=False):
    """
    Get a positive int as input from the user.

    Repeatedly get input from the user until a valid input is enterd.

    Args:
        prompt (str): The prompt to dispay to the user.
        zero_is_valid (bool): Decides whether zero is a valid input.

    Returns:
        int: The first valid input as an int.

    Raises:
        ShapeManagerArgumentTypeError: Raised if either `prompt` is not a string or `is_zero_valid` is not a boolean.
        ShapeManagerInputIterrationsError: Raised if MAX_INPUT_ITERATIONS was exceeded (too many invalid inputs.).
    """
    user_input = ""
    for attempt in range(MAX_INPUT_ITERATIONS):
        user_input = input(
            prompt if attempt == 0
            else "Please only type positive whole numbers (or 0): ")
        if not user_input.isdecimal():
            continue

        try:
            value = int(user_input)
        except ValueError:
            continue

        if value > 0 or ((value == 0) and zero_is_valid):
            return value
    
    raise ShapeManagerInputIterationsError("too many invalid inputs.")


def get_params_list(shape_params: tuple[str]) -> dict[str, int]:
    """
    Get user input for each needed parameter in the list.

    For now only supports int type, may be extended to other types as needed.
    
    Args:
        shape_params (tuple[str]): The list of needed parameters.

    Returns:
        dict[str, int]: The resulting Parameters as a dictionary wehere the parameter anme is the key.

    Raises:
        ShapeManagerArgumentTypeError: Raised if shape_params is not a list or any of its values are not strings.
        ShapeManagerInputIterationsError: Re-raised from get_positive_int if the number of maximum input iterations was exceeded
    """
    if not isinstance(shape_params, tuple):
        raise ShapeManagerArgumentTypeError("Argument shape_params must be a tuple.")
    result_params = {}
    for param in shape_params:
        if not isinstance(param, str):
            raise ShapeManagerArgumentTypeError("All values in shape_params must be str's.")
        try:
            value = get_positive_int(f"please enter a value for {param}: ")
        except ShapeManagerInputIterationsError:
            raise
        result_params[param] = value
    return result_params
