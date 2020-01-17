# -*- coding: UTF-8 -*-

from testcase.tools import *


def create_role(name=str(int(time.time()))):

    name_input = find_element_wait("##name_input")
    if name_input is None:
        logger.error("没有找到角色名输入窗口")
        return False
    engine.input(name_input, name)
    enter = engine.find_element("##btn_confirm")
    engine.click(enter)
    screen_shot_click(enter)
    time.sleep(2)
    return True


def main():
    create_role()


if __name__ == '__main__':
    main()
