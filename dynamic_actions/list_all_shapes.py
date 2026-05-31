from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("list_all_shapes", "list all shapes")
def handle_list_all_shapes(app: App):
    for shape in app.shape_manager.get_all_shapes():
        print(shape)