from utils.utils import get_positive_int
from app import App
from dynamic_actions_managment.dynamic_action_decorator import dynamic_action


@dynamic_action("compare_two_shapes", "compare two shapes")
def handle_compare_two_shapes(app: App):
    shape1_id = get_positive_int("please enter the id of the first shape: ", zero_is_valid=True)
    shape2_id = get_positive_int("please enter the id of the second shape: ", zero_is_valid=True)

    shape1 = app.shape_manager.get_shape_by_id(shape1_id)
    shape2 = app.shape_manager.get_shape_by_id(shape2_id)

    id1, id2 = shape1.shape_id, shape2.shape_id
    type1, type2 = shape1.shape_type, shape2.shape_type
    area1, area2 = shape1.get_area(), shape2.get_area()
    perimeter1, perimeter2 = shape1.get_perimeter(), shape2.get_perimeter()

    id1_str, id2_str = f"ID:{id1}", f"ID:{id2}"
    str_type1, str_type2 = f"Shape Type: {type1}", f"Shape Type: {type2}"
    str_area1, str_area2 = f"Area: {area1:.2f}", f"Area: {area2:.2f}"
    str_perimeter1, str_perimeter2 = f"Perimeter: {perimeter1:.2f}", f"Perimeter: {perimeter2:.2f}"

    area_comperasion_result = '=' if area1 == area2 else '>' if area1 > area2 else '<'
    perimeter_comperasion_result = '=' if perimeter1 == perimeter2 else '>' if perimeter1 > perimeter2 else '<'

    # column_widths
    w1, w2 = 25, 3

    print(f"""
┌{'':─^{w1}}┬{'':─^{w2}}┬{'':─^{w1}}┐
│{id1_str:<{w1}}│{'•':^{w2}}│{id2_str:<{w1}}│
├{'':─^{w1}}┼{'':─^{w2}}┼{'':─^{w1}}┤
│{str_type1:<{w1}}│{'•':^{w2}}│{str_type2:<{w1}}│
├{'':─^{w1}}┼{'':─^{w2}}┼{'':─^{w1}}┤
│{str_area1:<{w1}}│{area_comperasion_result:^{w2}}│{str_area2:<{w1}}│
├{'':─^{w1}}┼{'':─^{w2}}┼{'':─^{w1}}┤
│{str_perimeter1:<{w1}}│{perimeter_comperasion_result:^{w2}}│{str_perimeter2:<{w1}}│
└{'':─^{w1}}┴{'':─^{w2}}┴{'':─^{w1}}┘""")
