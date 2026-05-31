from app import App
from utils.app_states import AppStates
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("exit", "exit")
def handle_exit(app: App):
    """
    exit - action

    Args:
        app (App): 
    """
    app.state = AppStates.set_to_exit