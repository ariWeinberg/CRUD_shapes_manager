from app import App
from utils.utils import get_positive_int
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("search_shape_by_id", "search shape by id")
def handle_search_shape_by_id(app: App):
    """
    search by shape id - action

    Args:
        app (App): 
    """
    shape_id = get_positive_int("please enter the id of the wanted shape: ", zero_is_valid=True)
    shape = app.shape_manager.get_shape_by_id(shape_id)

    print(shape)