# -*- coding: UTF-8 -*-
import re

from game_lib.basic_operator import *
from game_lib import cheat_lib
from game_lib import sence_lib
from game_lib import ui_lib
import time


def cheat_mail(num=1):
    assert 0 < num <= 100
    cheat_lib.cheat_cmd("mail {}".format(num))


def cheat_template_mail(template_id):
    assert template_id > 100
    cheat_lib.cheat_cmd("mail {}".format(template_id))


def record_mail_info():
    sence_lib.enter_mail()


def scroll_mail_up():
    ui_lib.scroll_down("##scorll_mail")
    time.sleep(2)
    return 3


def get_mails_count():
    txt = engine_find_element("##textNum")
    m = re.match(r"(\d+)/(\d+)", engine_get_element_text(txt))
    if m:
        return int(m.group(1)), int(m.group(2))


def clickable(mail):
    if ui_lib.in_scroll("##scorll_mail", mail):
        return True
    return False


def read_all_mail():
    sence_lib.enter_mail()
    cur_num = 0
    mail_count, _ = get_mails_count()
    # @todo 识别邮件是否已读，用文字切换语言会出问题
    while cur_num < mail_count:
        mails = engine_find_elements_path("/UI Root/window_mail/##obj_mail/##scorll_mail/content/*")
        mail = mails[0]
        engine_click(mail)
        if ui_lib.find_then_click("##btnDraw"):
            engine_click_position(5, 5)
        else:
            ui_lib.find_then_click("##btnKnow")
        cur_num = cur_num + 1


def main():
    cheat_lib.cheat_mail(5)
    read_all_mail()


if __name__ == '__main__':
    main()
