# -*- coding: UTF-8 -*-
"""
负责场景切换
"""
from ui_lib import find_then_click, find_btn_in_list
from basic_operator import engine
from basic_operator import logger
import time


def enter_main():
    """
    以找到##text_time，也就是时间那个label为重点,不断的点击退出按钮
    """
    time_lable = engine.find_element("##text_time")
    exit_btns = ["##btnBlankClose", "##btnClose"]
    while not time_lable:
        finded = False
        for btn in exit_btns:
            if btn is "##btnBlankClose":
                engine.click_position(5, 5)
                finded = True
            else:
                finded = find_then_click(btn) or finded
        if not finded:
            time.sleep(3)
        time_lable = engine.find_element("##text_time")
    # 退出到主界面后可能会出现一些弹窗啥的，保险起见再做一次清理

    exit_btn = find_btn_in_list(exit_btns)
    while exit_btn:
        engine.click(exit_btn)
        exit_btn = find_btn_in_list(exit_btns)
    logger.debug("切到主界面完成")


def enter_shop():
    enter_main()
    ship_btn = engine.find_elements_path("##btn_func{img=major_btn_market_n}")
    assert len(ship_btn) == 1, '找不到舰队按钮'
    engine.click(ship_btn[0])


def enter_ship_main():
    enter_main()
    ship_btn = engine.find_elements_path("##btn_func{img=major_btn_ship_n}")
    assert len(ship_btn) == 1, '找不到舰队按钮'
    engine.click(ship_btn[0])


def clear_blank_close():
    while True:
        if find_btn_in_list(["##btnBlankClose"]):
            engine.click_position(5, 5)
        else:
            return


def clear_ads():
    while True:
        if not find_then_click("##btnClose"):
            return


def enter_mail():
    enter_main()
    mail_btn = engine.find_element(
        "/UI Root/window_major_haven/##node_ui/GameObject_flexible/##flex_btn_obj/##func_obj_mail/obj_main_btn/Image"
        "/##btn_func")
    if not mail_btn:
        find_then_click("##btn_show")
        mail_btn = engine.find_element(
            "/UI Root/window_major_haven/##node_ui/GameObject_flexible/##flex_btn_obj/##func_obj_mail/obj_main_btn"
            "/Image/##btn_func")
    engine.click(mail_btn)


if __name__ == '__main__':
    enter_ship_main()
