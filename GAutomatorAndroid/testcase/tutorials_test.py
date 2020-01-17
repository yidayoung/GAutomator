# -*- coding: UTF-8 -*-
from testcase.tools import *

engine = manager.get_engine()
logger = manager.get_logger()

TIMEOUT = 60 * 8


def main():
    start_time = time.time()
    scene = engine.get_scene()
    logger.debug("Scene :   {0}".format(scene))
    while True:
        if time.time() - start_time > TIMEOUT:
            logger.error("call tutorials test time out!")
            return False
        loop()
        if is_done():
            logger.debug("call tutorials test success done!")
            return True


def click_finger():
    engine.click(engine.find_element("##finger"))


def click_next():
    engine.click(engine.find_element("##btn_next"))


def clear_close():
    close = engine.find_element("##btnBlankClose")
    engine.click(close)


def clear_tutorial():
    tutorial = engine.find_element("left")
    engine.click(tutorial)


def clear_finger2():
    finger = engine.find_element("finger")
    engine.click(finger)


def click_button(clicked, name, is_force=False):
    if not clicked or is_force:
        btn = engine.find_element(name)
        if btn is not None:
            if name == "##btnBlankClose":
                """后台关闭按钮特殊处理下，有些地方要点击其他部分，
                但是控件点击点刚好在中间, 所以先固定的点击左上角10,10"""
                close_btn = engine.find_element("##btnClose")
                if close_btn is not None:
                    engine.click(close_btn)
                else:
                    engine.click_position(10, 10)
            logger.debug("find button {} and click".format(name))
            engine.click(btn)
            return True
    return False


def loop():
    buttonList = ["##finger", "##btn_next", "##btnSure", "##btnBlankClose", ("finger", True), "left"]
    clicked = False
    for btn in buttonList:
        if isinstance(btn, tuple):
            r = click_button(clicked, btn[0], btn[1])
        else:
            r = clicked or click_button(clicked, btn)
        clicked = clicked or r


def is_done():
    """
    现在判断的方法是看右边活动收缩的按钮是展开的不，也就是按钮名字变成了close
    然后点一下，变成了open， 这个方法也不是太准确，最好是客户端提供一个获得当前进度的回调，然后用回调获得新手引导值
    :return:
    """
    activity_close = engine.find_element("/UI Root/window_major_haven/##node_ui/activity_area/GameObject/Button_close")
    if activity_close is not None:
        engine.click(activity_close)
        open_btn = find_element_wait("/UI Root/window_major_haven/##node_ui/activity_area/GameObject/button_open", 3, 1)
        return open_btn is not None

    return activity_close is not None


if __name__ == '__main__':
    main()
