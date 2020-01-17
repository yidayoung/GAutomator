# coding=utf-8
from testcase.tools import *
from testcase.game_lib import cheat_lib, sence_lib
import re


def cheat_ship(shipTypeID, star=3, num=1):
    cheat_lib.cheat_ship(shipTypeID, star, num)


def empty(ship):
    if not engine.find_elements_path(ship.object_name + "/*"):
        return True
    return False


def scroll_down():
    """
    这个和界面强相关，现在实现逻辑是把滑动框从y轴底拉到顶
    """
    scroll_layer = engine.get_element_bound(engine.find_element("##scroll_shipiconlist"))
    y_min = scroll_layer.y
    y_max = scroll_layer.y + scroll_layer.height
    x_center = scroll_layer.x + (scroll_layer.width / 2)
    engine.swipe_and_press(x_center, y_max, x_center, y_min, 10, 10)
    time.sleep(1)
    # 一次拉了3行，每行4个，新增12个单位
    return 3 * 4


def calc_ship_num():
    ship_num_layer = engine.find_element("##ship_bag_limit_text")
    ship_num_str = engine.get_element_text(ship_num_layer)
    ship_num_group = re.match(r"(\d+)/(\d+)", ship_num_str)
    assert ship_num_group, "ship_num_str match failed"
    return int(ship_num_group.group(1)), int(ship_num_group.group(2))


def ensure_clickable(r):
    """
    如果按钮不再滚动窗口里那就点击不了，如果不在就scroll一次，一般就能解决问题
    :param r:
    """
    scroll_layer = engine.get_element_bound(engine.find_element("##scroll_shipiconlist"))
    ship = engine.get_element_bound(r)
    ship_center_x = ship.x + ship.width / 2
    ship_center_y = ship.y + ship.height / 2
    scroll_layer_max_x = scroll_layer.x + scroll_layer.width
    scroll_layer_max_y = scroll_layer.y + scroll_layer.height
    if scroll_layer.x < ship_center_x < scroll_layer_max_x and scroll_layer.y < ship_center_y < scroll_layer_max_y:
        pass
    else:
        scroll_down()
        time.sleep(3)


def find_ship(typeid, star=0, level=0):
    """
    找到指定typeid，星级，品阶的船只
    :param level:
    :param typeid:
    :param star:
    """
    sence_lib.enter_ship_main()
    ship_num, _ = calc_ship_num()
    cur_num = 0
    fist_view = True
    while cur_num < ship_num:
        r = do_one_ship_search(typeid, star, level)
        if r:
            ensure_clickable(r)
            return r
        scroll_num = scroll_down()
        if fist_view:
            cur_num = 16
            fist_view = False
        else:
            cur_num = cur_num + scroll_num
    return None


def calc_ship_star(path_pre):
    """
    通过界面计算船只的星数，pre是Object-golden-stars的上一层路径，必须确保路径拼接后唯一
    :param path_pre:
    :return:
    """
    # 这里是界面就写反了，不是这里代码写错了
    silver_star_lable = engine.find_elements_path(
        path_pre + "/Object-golden-stars/*")
    gold_star_lable = engine.find_elements_path(
        path_pre + "/Object-silver-stars/*")
    if len(silver_star_lable) > 0:
        ship_star = len(silver_star_lable)
    elif len(gold_star_lable) > 0:
        ship_star = 5 + len(gold_star_lable)
    else:
        ship_star = 0
    return ship_star


def do_one_ship_search(typeid, star=0, level=0):
    """
    对当前页面展示的船只进行查找，
    每次只看Y轴中间那行和他上下总共三行，然后返回第三行的Y坐标和
    :param typeid: 
    :param star: 
    :param level: 
    :return: 
    """
    ship_img_str = "card_ship_{}".format(typeid)
    ship_list = engine.find_elements_path("/UI Root/window_ship_content/##scroll_shipiconlist/content/*")
    for ship in ship_list:
        img = engine.find_element(ship.object_name + "/obj_ship_icon(Clone)/##shipNormal/##img_icon")
        if not img:
            continue
        if engine.get_element_image(img) != ship_img_str:
            continue
        if star > 0:
            ship_star = calc_ship_star(ship.object_name + "/obj_ship_icon(Clone)/##shipNormal/##star_node/obj_stars")
            if star != ship_star:
                continue
        if level > 0:
            level_lable = engine.find_element(
                ship.object_name + "/obj_ship_icon(Clone)/##shipNormal/##level")
            ship_level = int(engine.get_element_text(level_lable))
            if level != ship_level:
                continue
        return ship
    return None


def get_cur_level():
    level_lable = engine.find_element(
        "/UI Root/window_neo_shipyard/adapter/FuncNodes/##node_level/obj_ship_uplevel/img_level/##text_level")
    level_str = engine.get_element_text(level_lable)
    m = re.match(r"<.+>(\d+)<.+>/<.+>(\d+)<.+>", level_str)
    assert len(m.groups()) == 2
    return int(m.group(1)), int(m.group(2))


def uplevel_ship(tar_level):
    cur_level, cross_level = get_cur_level()
    if cur_level >= tar_level:
        return

    uplevel_btn = engine.find_element(
        "/UI Root/window_neo_shipyard/adapter/FuncNodes/"
        "##node_level/obj_ship_uplevel/btn_cost/up_btn/##lv_up_upgrade_btn")
    uprank_btn = engine.find_element(
        "/UI Root/window_neo_shipyard/adapter/FuncNodes/"
        "##node_level/obj_ship_uplevel/btn_cost/up_btn/##lv_up_uprank_btn")

    cur_btn = uplevel_btn if uplevel_btn else uprank_btn
    if not cur_btn and (cur_level == cross_level):
        logger.debug("已经达到最高等级")
        return
    cur_btn_bound = engine.get_element_bound(cur_btn)
    cur_btn_center_x = cur_btn_bound.x + cur_btn_bound.width / 2
    cur_btn_center_y = cur_btn_bound.y + cur_btn_bound.height / 2

    def click_up_level():
        engine.click_position(cur_btn_center_x, cur_btn_center_y)

    while cur_level < tar_level:
        cur_level1, cross_level1 = get_cur_level()
        click_up_level()
        if cur_level1 == cross_level1:
            click_up_level()
            # 如果是跨阶那下要检查清空主界面
            sence_lib.clear_blank_close()
            # time.sleep(2)
        cur_level, cross_level = get_cur_level()
        if cur_level == cur_level1 and cross_level == cross_level1:
            # 如果点了还没升级
            logger.error("目标等级是{}，当前等级{}，但是升不动了".format(tar_level, cur_level))
            return False
    return True


def base_cheat():
    cheat_lib.cheat_money(1, 99999999999)
    cheat_lib.cheat_money(2, 99999999999)
    cheat_lib.cheat_money(3, 99999999999)
    cheat_lib.cheat_money(4, 99999999999)
    cheat_lib.cheat_money(1004, 99999999999)


def cheat_ship_all_star(typeid, num=5, start_star=3):
    for star in range(start_star, 10):
        cheat_ship(typeid, star, num)


def ensure_max_ship():
    sence_lib.enter_ship_main()
    buy_btn = engine.find_element("##obj_listbuy_btn")
    engine.click(buy_btn)
    ok_btn = engine.find_element("##Button_sure")
    ship_num, max1 = calc_ship_num()
    if ok_btn:
        engine.click(ok_btn)
        ship_num, max2 = calc_ship_num()
        if max2 > max1:
            ensure_max_ship()


def deal_need(need_list):
    for need in need_list:
        num_layer = (engine.find_elements_path(need.object_name + "/numbers/*"))[0]
        m = re.match(r"\d+/(\d)", engine.get_element_text(num_layer))
        assert m, "没有匹配到需要的数量"
        need_num = int(m.group(1))
        engine.click(need)
        ships = engine.find_elements_path("/UI Root/obj_shiplist_middle/##scorll_partion/content/*")
        assert len(ships) >= need_num, "待选材料不足"
        for i in range(0, need_num):
            engine.click(ships[i])
        assert sence_lib.find_then_click("##choose_btn")


def do_one_up_star():
    need_list = engine.find_elements_path("/UI Root/window_neo_shipyard/adapter/FuncNodes/##node_upstar"
                                          "/obj_ship_upstars/##can_up_star/Object-bottomlist/*")
    deal_need(need_list)
    assert sence_lib.find_then_click("##upstar_btn")
    sence_lib.clear_blank_close()
    return calc_ship_star("/UI Root/window_neo_shipyard/middile/##ship_name_node/obj_shipyard_name/##main_node"
                          "/##star_node/obj_stars_1")


def test_up_star(typeid):
    """
    测试船只的升星逻辑，从6星开始，一直升级到10星
    :param typeid:
    """
    star = 6
    tar_star = 10
    # cheat_ship_all_star(101, 10)
    # 找到一艘6星1级的船
    ship = find_ship(typeid, star, 1)
    assert ship, "测试升星过程中，没找到指定星级的船"
    engine.click(ship)
    # 将船升级到最大等级
    tar_level = 140
    uplevel_ship(tar_level)
    cur_level, _ = get_cur_level()
    assert cur_level == tar_level, "船只升级到{}等级失败，当前{}级".format(tar_level, cur_level)
    assert sence_lib.find_then_click("##Toggle5"), "没有找到改造按钮"
    time.sleep(1)
    for _ in range(star, tar_star):
        star = star + 1
        assert star == do_one_up_star(), "升星失败，当前星为{}".format(star)


def main():
    # base_cheat()
    # ensure_max_ship()
    cheat_ship_all_star(111, 10, 5)
    # ship = find_ship(111, 9, 1)
    # engine.click(ship)
    # uplevel_ship(200)

    test_up_star(111)


if __name__ == '__main__':
    main()
