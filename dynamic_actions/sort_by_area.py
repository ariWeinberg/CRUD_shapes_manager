from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("sort_by_area", "sort by area")
def handle_sort_by_area(app: App):
    """
    sort by area - action

    Args:
        app (App): 
    """
    for shape in app.shape_manager.get_all_shapes(sort_direction=True):
        print(shape)