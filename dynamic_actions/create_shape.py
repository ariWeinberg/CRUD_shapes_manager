from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager
from utils.utils import get_params_list
from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("create_shape", "create shape")
def handle_create_shape(app: App):
    choice = app.shape_selection_menu.execute_menu()

    shape_descriptor = DynamicShapeTypeManager.get_shape_descriptor(choice.shape_name)
    shape_attributes = get_params_list(shape_descriptor.shape_params)

    shape = shape_descriptor.cls(**shape_attributes)
    app.shape_manager.create_shape(shape)
