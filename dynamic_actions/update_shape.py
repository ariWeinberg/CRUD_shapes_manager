from utils.utils import get_positive_int, get_params_list
from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager
from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("update_shape", "update shape")
def handle_update_shape(app: App):
    shape_id = get_positive_int("please select a shape to update (by id): ", zero_is_valid=True)
    old_shape = app.shape_manager.get_shape_by_id(shape_id)

    print(f"editing shape:\n{old_shape}\n")

    shape_descriptor = DynamicShapeTypeManager.get_shape_descriptor(old_shape.shape_type)
    shape_attributes = get_params_list(shape_descriptor.shape_params)

    shape = shape_descriptor.cls(**shape_attributes)
    app.shape_manager.update_shape(shape_id, shape)