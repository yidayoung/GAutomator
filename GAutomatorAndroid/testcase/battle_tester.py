# -*- coding: UTF-8 -*-

from testcase.tools import *


def main(battle_count=10):
    clear_main()
    enter_battle()
    for i in range(battle_count):
        handle_do_one_fight()


def start_game():
    start_button = engine.find_element("##btn_login")
    engine.click(start_button)


def need_pass():
    start_button = find_element_wait("##btnSkip", 3, 1)
    if start_button is not None:
        engine.click(start_button)
        return True
    return False


def clear_main():
    find_element_wait("##node_ui", 10, 1)
    close_button = engine.find_element("##btnClose")
    while close_button is not None:
        close_button = engine.find_element("##btnClose")
        engine.click(close_button)


def enter_battle():
    battle = engine.find_element("##btn_battle")
    engine.click(battle)


def hang_on_battle():
    battle1 = engine.find_element("/UI Root/window_fight_main/GameObject ("
                                  "1)/##node_dungeonlist/obj_dungeon_list1/##viewport/##content/##dungeon1")
    engine.click(battle1)
    find_element_wait("#g#node_drop_fixed")
    forward_btn = engine.find_element("##btn_forward")
    if forward_btn is not None:
        engine.click(forward_btn)
    else:
        close_button = engine.find_element("##btnClose")
        engine.click(close_button)


def clear_story():
    story_layer = engine.find_element("##btn_next")
    if story_layer is None:
        return False
    else:
        while story_layer is not None:
            story_layer = engine.find_element("##btn_next")
            engine.click(story_layer)
            time.sleep(1)


def clear_finger():
    finger = engine.find_element("finger")
    engine.click(finger)
    close = engine.find_element("##btnBlankClose")
    engine.click(close)


def clear_tutorial():
    tutorial = engine.find_element("left")
    engine.click(tutorial)


def close_battle(close):
    logger.debug("close_battle")
    engine.click(close)
    close = find_element_wait("##btnBlankClose", 5, 1)
    while close is not None:
        engine.click(close)
        logger.debug("close_battle click one try one more")
        close = find_element_wait("##btnBlankClose", 3, 1)


def loop_fight():
    logger.debug("loop fight")
    clear_story()
    clear_finger()
    clear_tutorial()
    time.sleep(1)


def fight():
    """
    在战斗界面，且战斗节点亮的情况下，进行一场战斗，函数执行完毕后，界面恢复到选择关卡界面
    """
    logger.debug("begin fight")
    fight_btn = find_element_wait("##btn_fight")
    engine.click(fight_btn)
    find_element_wait("window_battlemap_ui")
    # 进入战斗后已找到关闭按钮为目的进行loop，loop过程中关闭引导
    close = engine.find_element("##btnBlankClose")
    while close is None:
        close = engine.find_element("##btnBlankClose")
        loop_fight()
    close_battle(close)
    # 这里到战斗界面完全退出才算终止，也就是要等到返回挂机界面
    find_element_wait("window_fight_main")


def do_hang_on():
    """
    执行挂机操作，会把当前next节点作为挂机点，如果没挂机就挂上，如果挂了就点开看下退出
    """
    logger.debug("do_hang_on")
    enter_btn = engine.find_element("##next")
    engine.click(enter_btn)
    find_element_wait("#g#node_drop_fixed")
    forward_btn = engine.find_element("##btn_forward")
    if forward_btn is not None:
        engine.click(forward_btn)
    else:
        close_button = engine.find_element("##btnClose")
        engine.click(close_button)


def handle_do_one_fight():
    """
    进行一次推图操作，入口是主界面，进入后无论是什么结果都会尝试推进下一关卡

    """
    fight_btn = engine.find_element("##btn_fight")
    if fight_btn is None:
        do_hang_on()
    fight()


if __name__ == "__main__":
    main()
