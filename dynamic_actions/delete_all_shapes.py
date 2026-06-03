from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("delete_all_shapes", "delete all shapes")
def handle_delete_all_shapes(app: App):
    """
    delete all shapes - action

    Args:
        app (App):
    """
    app.shape_manager.delete_all()