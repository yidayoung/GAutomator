# -*- coding: UTF-8 -*-
import wpyscripts.manager as manager
from wpyscripts.tools import basic_operator as wpy_operator

logger = manager.get_logger()
engine = manager.get_engine()
device = manager.get_device()
report = manager.get_reporter()


def screen_shot_click(element, sleeptime=2, exception=False):
    return wpy_operator.screen_shot_click(element, sleeptime, exception)


def screen_shot_click_pos(pos_x, pos_y, sleeptime=2, exception=True):
    return wpy_operator.screen_shot_click_pos(pos_x, pos_y, sleeptime, exception)


def find_element_wait(name, max_count=10, sleeptime=3):
    return wpy_operator.find_element_wait(name, max_count, sleeptime)


def screenshot():
    return report.screenshot()


def engine_click(src):
    return engine.click(src)


def engine_input(name, string):
    return engine.input(name, string)


def engine_find_element(src):
    return engine.find_element(src)


def engine_find_elements_path(src):
    return engine.find_elements_path(src)


def engine_click_position(x, y):
    return engine.click_position(x, y)


def engine_get_element_text(src):
    return engine.get_element_text(src)


def engine_get_element_image(src):
    return engine.get_element_image(src)


def engine_get_element_bound(src):
    return engine.get_element_bound(src)
