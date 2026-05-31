from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("filter_by_shape_type", "filter by shape type")
def handle_filter_by_shape_type(app: App):
    shape_descriptor = app.shape_selection_menu.execute_menu()
    for shape in app.shape_manager.get_all_shapes(type_filter=shape_descriptor.shape_name):
        print(shape)