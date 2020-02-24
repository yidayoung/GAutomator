# coding=utf-8

from basic_operator import engine


def find_then_click(btn):
    """
    查找按钮，如果找到了就点击，返回True，没找到就直接发挥False
    :param btn: 要查找的按钮
    :return: 是否找到了按钮
    """
    btn = engine.find_element(btn)
    if btn:
        engine.click(btn)
        return True
    return False


def find_btn_in_list(btn_list):
    """
    在给定的按钮名字中调用find_element来查找，找到任意按钮就立刻返回，根据列表顺序
    :param btn_list: 要查找的按钮列表
    :return: 查找到的按钮|None
    """
    for btn_name in btn_list:
        btn = engine.find_element(btn_name)
        if btn:
            return btn
    return None


def calc_scroll_layer(item):
    """
    计算滑动控件的范围
    :param item: 滑动控件的名字
    :return:
    """
    scroll_layer = engine.get_element_bound(engine.find_element(item))
    y_min = scroll_layer.y
    y_max = scroll_layer.y + scroll_layer.height
    y_center = (y_min + y_max) / 2
    x_min = scroll_layer.x
    x_max = scroll_layer.x + scroll_layer.width
    x_center = (x_min + x_max) / 2
    return x_center, y_center, x_max, x_min, y_max, y_min


def scroll_down(item, steps=10, duration=10, step_sleep=5):
    """
    将item向下滑动，起始点为y轴底端，目标点为y轴的顶端
    :param item: 滑动框bound
    :param steps: 滑动中间的步骤数，每一步的间隔为5ms，可以用于控制滑动速度和平滑度
    :param duration: 结束位置按压时间，单位是毫秒ms
    :param step_sleep:每个步骤的间隔时长，单位毫秒
    """
    x_center, y_center, x_max, x_min, y_max, y_min = calc_scroll_layer(item)
    engine.swipe_and_press(x_center, y_max, x_center, y_min, steps, duration, step_sleep)


def scroll_up(item, steps=10, duration=10, step_sleep=5):
    """
    将item向上滑动，起始点为y轴低端，目标点为y轴顶端
    :param item:
    :param steps:
    :param duration:
    :param step_sleep:
    """
    x_center, y_center, x_max, x_min, y_max, y_min = calc_scroll_layer(item)
    engine.swipe_and_press(x_center, y_min, x_center, y_max, steps, duration, step_sleep)


def in_scroll(scroll_name, obj):
    """
    判断obj的点击位置，也就是click最终点击的位置是不会是在scroll里，可以确保目标控件可以被点击
    :param scroll_name: 滑动框
    :param obj: 要判断的空间
    :return: 是否在滑动框的可视范围内
    """
    scroll_layer = engine.get_element_bound(engine.find_element(scroll_name))
    o = engine.get_element_bound(obj)
    ship_center_x = o.x + o.width / 2
    ship_center_y = o.y + o.height / 2
    scroll_layer_max_x = scroll_layer.x + scroll_layer.width
    scroll_layer_max_y = scroll_layer.y + scroll_layer.height
    if scroll_layer.x < ship_center_x < scroll_layer_max_x and scroll_layer.y < ship_center_y < scroll_layer_max_y:
        return True
    else:
        return False
