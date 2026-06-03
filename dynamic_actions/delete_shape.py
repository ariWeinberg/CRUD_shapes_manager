from app import App
from utils.utils import get_positive_int
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("delete_shape", "delete shape")
def handle_delete_shape(app: App):
    """
    delete shape - action

    Args:
        app (App):
    """
    shape_id = get_positive_int("please select a shape to update (by id): ", zero_is_valid=True)
    app.shape_manager.delete_shape(shape_id)