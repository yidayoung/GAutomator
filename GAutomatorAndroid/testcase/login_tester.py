# -*- coding: UTF-8 -*-

from game_lib.basic_operator import *
from game_lib import sence_lib
import time


def no_sdk_reg(account, password):
    account_btn = find_element_wait("##btn_account")
    if account_btn is None:
        logger.error("没有在登陆界面")
        return False
    engine_click(account_btn)

    reg_panel = find_element_wait("#b#btn_panel_regster", 3, 1)
    if reg_panel is None:
        logger.error("没有登录界面弹出!")
        return False
    engine_click(reg_panel)

    reg_btn = find_element_wait("#b#btn_regster", 3, 1)
    if reg_btn is None:
        logger.error("没有注册界面弹出!")
        return False
    account_input = engine_find_element("/UI Root/window_login_account/adapter/#o#obj_rester/#k#input_n_account")
    password_input = engine_find_element("/UI Root/window_login_account/adapter/#o#obj_rester/#k#input_n_password")
    password_input2 = engine_find_element("/UI Root/window_login_account/adapter/#o#obj_rester/#k#input_n_password2")

    engine_input(account_input, account)
    engine_input(password_input, password)
    engine_input(password_input2, password)
    engine_click(reg_btn)

    if not check_login_success(account):
        logger.error("账号注册失败")
        return False
    return True


def check_login_success(accountName):
    # 如果成功了，那么会返回主界面，且账号的地方是账号名
    acc_name_panel = find_element_wait("##account_name", 5, 1)
    if acc_name_panel is None:
        return False
    new_acc_name = engine_get_element_text(acc_name_panel)
    if new_acc_name != accountName:
        return False
    return True


def no_sdk_login(account, password, need_reg=False):
    if need_reg:
        return no_sdk_reg(account, password)
    else:
        account_btn = engine_find_element("##btn_account")
        engine_click(account_btn)
        login_btn = find_element_wait("#b#btn_login", 3, 1)
        if login_btn is None:
            logger.error("点击账号按钮后，没有弹出注册界面")
            return False
        account_input = engine_find_element("#k#input_o_account")
        password_input = engine_find_element("#k#input_o_password")

        engine_input(account_input, account)
        engine_input(password_input, password)

        engine_click(engine_find_element("#b#btn_login"))
        return check_login_success(account)


def chose_server(sid, partion_name="第1分区"):
    """
    选择服务器，入口必须是在刚进入游戏的主界面
    :param sid: 服务器ID，数字
    :param partion_name: 可以参数，如果选了必须是分区名字的字符串，而不能是ID，字符串必须完整
    """
    reg_btn = find_element_wait("##btn_serverList", 3, 1)
    if reg_btn is None:
        logger.error("没有在登陆界面")
        return False
    engine_click(reg_btn)
    time.sleep(1)
    partition_btn = engine_find_elements_path("obj_partion_item{{txt={}}}".format(partion_name))
    if len(partition_btn) <= 0:
        logger.error("没有找到分区{}".format(partion_name))
        return False
    engine_click(partition_btn[0])
    time.sleep(2)
    sidStr = "{}服 ".format(sid)
    server_btn = engine_find_elements_path("obj_server_item{{txt={}}}".format(sidStr))
    if len(server_btn) <= 0:
        logger.error("没有找到服务器{}".format(sidStr))
        return False
    engine_click(server_btn[0])

    # 判断选区是否成功通过看执行完成后，区服处的字符串是否包括sidStr判断
    server_name = find_element_wait("##server_name")
    serverNameStr = engine_get_element_text(server_name)
    if sidStr not in serverNameStr:
        logger.error("选区失败，目标区为{}:{}, 当前区为{}", partion_name, sid, serverNameStr)
        return False
    return True


def click_login():
    login_btn = find_element_wait("##btn_login")
    engine_click(login_btn)
    skip_btn = find_element_wait("##btnSkip", 5, 3)
    if skip_btn is not None:
        engine_click(skip_btn)
        return True
    return False


def main(acc_name=str(int(time.time())), sid=1):
    # 有时候会弹出公告，清理下主界面
    sence_lib.clear_blank_close()
    no_sdk_reg("1030", "1")
    assert (no_sdk_reg(acc_name, "1"))
    assert (chose_server(sid))
    assert (no_sdk_login(acc_name, "1"))
    assert (chose_server(sid))
    assert (click_login())


if __name__ == '__main__':
    main()
