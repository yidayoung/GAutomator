# -*- coding: UTF-8 -*-
"""
作弊必须在主界面进行，作弊截止动作为作弊输入窗口再次点开
"""
from basic_operator import engine
from game_lib import sence_lib
import time


def cheat_cmd(cmd):
    sence_lib.enter_main()
    input_layer = engine.find_element("##inputField")
    cheat_btn = engine.find_element("##btnCheat")
    assert cheat_btn, '找不到作弊按钮'
    while not input_layer:
        engine.click(cheat_btn)
        # 可能突然就弹个广告出来，处理下
        sence_lib.clear_ads()
        input_layer = engine.find_element("##inputField")
    engine.click(input_layer)
    engine.input(input_layer, cmd)
    engine.click(input_layer)
    # 作弊完成后可能界面会发生变化，每次作弊必须确保界面恢复到能找到作弊按钮且点出输入框
    check_count = 0

    input_layer = engine.find_element("##inputField")
    while not input_layer:
        time.sleep(1)
        if check_count > 10:
            print("尝试清除界面找到作弊按钮失败")
        engine.click(engine.find_element("##Button_exit"))
        engine.click(engine.find_element("##btnBlankClose"))
        engine.click(engine.find_element("##btnClose"))
        engine.click(cheat_btn)
        input_layer = engine.find_element("##inputField")


def cheat_money(typeid, num):
    cheat_cmd("add_money {} {}".format(typeid, num))


def cheat_ship(typeid, star=3, num=1):
    assert typeid < 9999
    realTypeID = typeid * 100 + star
    cheat_cmd("add_ship {} {}".format(realTypeID, num))


def cheat_level(level):
    cheat_cmd("set_lvl {}".format(level))


def cheat_vip(level):
    cheat_cmd("set_vip {}".format(level))


def cheat_mail(num=1):
    assert 100 >= num > 0
    cheat_cmd("mail {}".format(num))


if __name__ == '__main__':
    # cheat_money(2, 10)
    for star in range(3, 10):
        cheat_ship(120 + star, star, 1)
    # cheat_level(90)
    # cheat_vip(3)
    # cheat_mail(10)
    # for lv in range(29, 200, 10):
    #     cheat_level(lv)
