# -*- coding: UTF-8 -*-
from game_lib.basic_operator import *
from game_lib import ui_lib
import time


def create_role(name=str(int(time.time()))):
    ui_lib.find_then_click("##btnSkip")
    name_input = find_element_wait("##name_input")
    if name_input is None:
        logger.error("没有找到角色名输入窗口")
        return False
    engine_input(name_input, name)
    enter = engine_find_element("##btn_confirm")
    engine_click(enter)
    screen_shot_click(enter)
    time.sleep(2)
    return True


def main():
    create_role()


if __name__ == '__main__':
    main()
