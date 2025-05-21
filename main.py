# main.py
import tools
from json_loader import JsonLoader
from save_manager import SaveManager


def display_country_properties_menu():
    print("\n修改国家属性菜单：")
    print("[1] 查看和修改时间")
    print("[2] 查看和修改金钱")
    print("[3] 查看和修改船厂吨位")
    print("[4] 查看和修改声望")
    print("[5] 修改船员数和训练程度")
    print("[6] 查看和修改骚乱")
    print("[7] 查看和修改政体")
    print("[8] 修改GDP")
    print("[9] 返回主菜单")

def display_map_menu():
    print("\n地图与国家关系菜单：")
    print("[1] 快速完成所有入侵事件")
    print("[2] 提前开发石油")
    print("[3] 修改国家间的关系")
    print("[4] 返回主菜单")

def display_event_acceleration_menu():
    print("\n事件加速菜单：")
    print("[1] 快速建造船只")
    print("[2] 快速移动")
    print("[3] 快速研发正在研发的科技")
    print("[4] 快速研发所有科技")
    print("[5] 返回主菜单")

def display_main_menu():
    print("\n主菜单：")
    print("[1] 修改国家属性")
    print("[2] 修改地图与国际关系")
    print("[3] 事件加速")
    print("[4] 保存退出")
    print("[5] 直接退出")


def main(debug=False):
    tools.print_logo() # 打印标题
    if debug == True:
        print("!这是debug模式!")
    if not debug and not tools.is_admin():
        # 如果不是管理员身份，显示提示并退出
        input("请以管理员权限运行此程序,按下回车退出...")
        return

    loader = JsonLoader(debug=debug)

    selected_file = loader.select_save_file()
    if not selected_file:
        return

    json_data = loader.read_json_file(selected_file)
    if not json_data:
        input("无法读取JSON数据。按下回车退出...")
        return

    sm = SaveManager(json_data, debug=debug)
    del(json_data)

    while True:
        display_main_menu()
        main_choice = input("请选择一个操作：")
        if main_choice == '1':

            while True:
                display_country_properties_menu()
                country_choice = input("请选择一个操作：")
                if country_choice == '1':
                    sm.update_turn_by_date()
                elif country_choice == '2':
                    handle_cash(sm)
                elif country_choice == '3':
                    handle_shipyard(sm)
                elif country_choice == '4':
                    handle_reputation(sm)
                elif country_choice == '5':
                    handle_crew(sm)
                elif country_choice == '6':
                    handle_respect(sm)
                elif country_choice == '7':
                    handle_government_type(sm)
                elif country_choice == '8':
                    modify_usa_provinces_income(sm)
                elif country_choice == '9':
                    break
                else:
                    print("无效的选择，请重新输入。")
        elif main_choice == '2':
            while True:
                display_map_menu()
                event_choice = input("请选择一个事件操作：")
                if event_choice == '1':
                    instant_colonial_conquest(sm)
                if event_choice == '2':
                    discover_oil(sm)
                if event_choice == '3':
                    handle_relations(sm)
                if event_choice == '4':
                    break
        elif main_choice == '3':
            while True:
                    display_event_acceleration_menu()
                    event_acceleration_choice = input("请选择一个操作：")
                    if event_acceleration_choice == '1':
                        instant_construction(sm)
                    elif event_acceleration_choice == '2':
                        instant_movement(sm)  # 处理快速移动的逻辑
                    elif event_acceleration_choice == '3':
                        accelerate_current_research(sm)  # 处理快速研发当前科技的逻辑
                    elif event_acceleration_choice == '4':
                        accelerate_all_research(sm) # 处理快速研发所有科技的逻辑
                    elif event_acceleration_choice == '5':
                        break
                    else:
                        print("无效的选择，请重新输入。")
        elif main_choice == '4':
            loader.save_json_file(data=sm.get_data())
            break
        elif main_choice == '5':
            break
        else:
            print("无效的选择，请重新输入。")

    input("按下回车退出...")

def accelerate_current_research(sm):
    """加速当前正在研究的科技项目"""
    modified_count = sm.accelerate_current_research()
    print(f"成功加速{modified_count}个正在研发的科技项目(部分研究不会跳出弹窗)")

def accelerate_all_research(sm):
    """加速所有科技研发项目"""
    modified_count = sm.accelerate_all_research()
    print(f"成功添加并研发{modified_count}个科技项目")


def modify_usa_provinces_income(sm):
    """修改 IncomeGrowth，从而提升 GDP 和海军预算"""
    print(f"""\
【功能介绍】
你将要修改你控制的所有地区的增长的经济（IncomeGrowth）数值。
每个地区每回合会带来一定的经济增长，这些增长会影响国家的 GDP。
而 GDP 决定了你每回合能获得多少海军资金。
注意：
- 这个修改不是直接加钱或增加GDP，而是修改"增长的经济"。
- 建议设置较大的倍率（如10倍或100倍），才能在下一回合看到显著效果。
""")

    # 计算当前总IncomeGrowth
    total_income_growth = 0
    name = sm.get_player_name()
    provinces = sm.get_provinces()
    for p in provinces:
        if p.get("Controller") == name:
            total_income_growth += p.get("IncomeGrowth", 0)

    multiplier = tools.get_float_input(f"当前可修改经济为：{total_income_growth}，请输入增长倍率：")
    if multiplier is None:
        print("已取消修改。")
        return

    modified_count = 0
    name = sm.get_player_name()
    provinces = sm.get_provinces()
    for p in provinces:
        if p.get("Controller") == name:
            old_growth = p.get("IncomeGrowth", 0)
            p["IncomeGrowth"] = old_growth * multiplier
            modified_count += 1

    sm.set_provinces(provinces)
    print(f"已修改 {modified_count} 个地区的增长的经济，倍率为{multiplier}。")



def handle_cash(sm):
    """处理玩家金钱的修改操作"""
    current_cash = sm.get_cash()
    print(f"当前金钱：{current_cash}")
    new_cash_multiplier = tools.get_float_input("请输入金钱的变化倍数，如 1.5 表示翻 1.5 倍（直接回车保持不变）：\n")
    if new_cash_multiplier is not None:
        new_cash = int(current_cash * new_cash_multiplier)
        sm.set_cash(new_cash)
        print(f"金钱已更新为：{sm.get_cash()}")
    else:
        print("已取消修改。")

def handle_shipyard(sm):
    """处理造船厂最大吨位的修改操作"""
    current_amount = sm.get_shipyard()
    print(f"当前船厂吨位：{current_amount}")
    new_amount = tools.get_int_input("请输入新的造船厂最大吨位，建造中的造船厂将在下一回合建好（直接回车保持不变）：\n", min_value=0)
    if new_amount is not None:
        sm.set_shipyard(new_amount)
        print(f"船厂吨位已更新为：{sm.get_shipyard()}")


def handle_reputation(sm):
    """处理声望的修改操作"""
    current_reputation = sm.get_reputation()
    print(f"当前声望：{current_reputation}")
    new_reputation = tools.get_int_input("请输入新的声望数值（直接回车保持不变）：\n", min_value=0)
    if new_reputation is not None:
        sm.set_reputation(new_reputation)
        print(f"声望已更新为：{sm.get_reputation()}")

def handle_crew(sm):
    """处理船员数"""
    current_crew = sm.get_crew_pool()
    print(f"当前船员数：{current_crew}")
    new_training = tools.get_float_input("请输入新的平均船员训练水平（直接回车保持不变）：\n")
    if new_training is not None:
        sm.set_AverageCrewPoolTraining(new_training)
        print(f"平均船员训练水平已更新为：{sm.get_AverageCrewPoolTraining()}")

    # 处理平均船员训练水平
    current_training = sm.get_AverageCrewPoolTraining()
    print(f"当前平均船员训练水平：{current_training}")
    new_crew = tools.get_int_input("请输入新的船员数（直接回车保持不变）：\n")
    if new_crew is not None:
        sm.set_crew_pool(new_crew)
        print(f"船员数已更新为：{sm.get_crew_pool()}")


def instant_construction(sm):
    """快速建造"""
    i = sm.instant_construction()
    print(f"成功加速{i}艘船")

def instant_colonial_conquest(sm):
    """快速殖民地入侵"""
    i = sm.instant_colonial_conquest()
    print(f"成功加速{i}个事件")

def discover_oil(sm):
    """发现石油"""
    # 获取尚未发现石油的省份列表及其名称到Id的映射
    provinces, name_to_id_map = sm.get_provinces_not_discovered_oil()
    search_again = False  # 标记是否需要重新进行模糊搜索

    while True:
        if not search_again:
            # 获取用户输入，用于模糊搜索省份
            user_input = input("输入游戏内的省份名称进行模糊搜索（按下回车退出）:\n ").lower()
        else:
            # 如果需要重新搜索，使用上一次输入的省份名称
            user_input = search_again
            search_again = False

        # 回车退出循环
        if user_input == '':
            break

        # 调用工具函数进行模糊搜索
        selected_province = tools.fuzzy_search(user_input, provinces)

        if selected_province and selected_province in name_to_id_map:
            # 根据省份名称获取原始省份Id
            original_province_id = name_to_id_map[selected_province]
            # 设置省份的油田发现状态
            if sm.set_isOilDiscovery(original_province_id):
                print(f"成功设置{original_province_id}")
                break  # 成功设置后退出循环
            else:
                print(f"设置:{original_province_id}失败")
        elif selected_province is None:
            # 无匹配结果的情况下，返回重新输入
            continue
        else:
            # 如果选择了新的搜索关键词
            search_again = selected_province

def handle_relations(sm):
    """处理国际关系"""
    # 打印关系矩阵
    relations_matrix, countries = sm.build_relations_matrix()
    tools.print_relations_matrix(relations_matrix, countries)

    while True:
        # 初始化国家变量，存储输入的国家名称
        country_names = list(None for _ in range(2))

        # 循环获取两个国家的名称
        for i in range(2):
            # 根据索引调整提示内容
            prompt = f"输入第{i+1}个国家的名称（按下回车退出）: \n"

            # 获取用户输入
            user_input = input(prompt).lower()
            if user_input == '':  # 用户按下回车退出
                return  # 退出函数

            # 使用模糊搜索工具函数来查找并确认国家名称
            selected_country = tools.fuzzy_search(user_input, countries)
            if not selected_country:
                break  # 退出当前循环，重新开始整个输入流程
            country_names[i] = selected_country  # 将确认的国家名称存储在 country_names 列表中

        # 如果循环未被中断，说明已获取有效的两个国家名称
        if None not in country_names:
            country_a, country_b = country_names  # 解包国家名称

            # 输入 attitude 值
            new_attitude = tools.get_float_input("输入新的 attitude 值，范围在-100到100之间: ", allow_empty=False)
            if new_attitude is None or not -100 <= new_attitude <= 100:
                print("无效的 attitude 值，请重新输入。")
                continue

            # 设置两个国家之间的 attitude
            success = sm.set_attitude(country_a, country_b, new_attitude)

            if success:
                print(f"成功设置 {country_a} 和 {country_b} 之间的 attitude 为 {new_attitude}")
            else:
                print(f"设置 {country_a} 和 {country_b} 之间的 attitude 失败")


def instant_movement(sm):
    """快速移动"""
    moving_groups, index_map = sm.get_moving_groups()
    if not moving_groups:
        print("当前没有移动的船团。")
        return

    print("可以瞬间完成移动的船团：")
    for index, group in enumerate(moving_groups, start=1):
        print(f"[{index}]"
              f" 从{group['From'] if group['From'] else '海上'}"
              f"到{group['To'] if group['To'] else '海上'}，"
              f"共{len(group['Vessels'])}艘船。")
    try:
        print("注意：在使用瞬间移动功能后，船团的图标会乱飘，请放心下一回合后会恢复正常。如果必须要操作，找到乱飘的图标后即可正常操作。")
        choice = tools.get_int_input("请输入要瞬间完成移动的船团编号（按下回车取消）：", min_value=1,
                                     max_value=len(moving_groups))
        if choice is None:
            print("操作已取消。")
            return
        choice = choice - 1
        original_index = index_map[choice]  # 使用映射找到原始列表中的索引
        sm.instant_move(original_index)  # 传入原始索引到 instant_move 方法
        print("船团已瞬间移动至目的地。")
    except (ValueError, IndexError):
        print("请输入有效的编号。")


def handle_respect(sm):
    """修改骚乱值"""
    print(f"当前骚乱值:{sm.get_respect()}")
    new_respect = tools.get_float_input("请输入新的骚乱值（直接回车保持不变）：\n")
    if new_respect is not None:
        sm.set_respect(new_respect)
        print(f"骚乱已更新为：{sm.get_respect()}")

def handle_government_type(sm):
    """处理政府类型/政体"""
    # 初始化政府系统
    government_id = sm.get_government_type()
    new_government_id = None
    percent_by_party = sm.get_party_support()

    # 显示当前状态
    print(f"当前政体类型：{['君主专制', '君主立宪', '代议政治'][government_id]}")
    print("当前派别支持率（极左、左、中、右、极右）：")
    parties = ["极左", "左", "中", "右", "极右"]
    for i, percent in enumerate(percent_by_party):
        print(f"{parties[i]}: {percent}%")

    # 选择新的政府类型
    while True:
        new_government_id = tools.get_int_input(
            "请输入新的政体ID编号（0: 君主专制, 1: 君主立宪, 2: 代议政治，直接回车保持不变）：\n", min_value=0, max_value=2)
        if new_government_id is not None:
            sm.set_government_type(new_government_id)
            break  # 有效输入，跳出循环

    # 显示派别支持率并让用户选择
    while True:
        print("选择支持一个派别:")
        for i, party in enumerate(parties):
            print(f"{i}: {party}")

        selected_party_input = input("请输入要支持的派别编号（回车退出）：")
        if selected_party_input.strip() == '':  # 如果输入为空，直接退出
            return

        try:
            selected_party_index = int(selected_party_input)
            if selected_party_index < 0 or selected_party_index >= len(parties):
                print("无效的派别编号，请输入有效的编号。")
            else:
                # 设置选择的派别支持率
                percent_by_party = [2.0] * len(parties)  # 初始化所有派别支持率为2
                percent_by_party[selected_party_index] = 92.0  # 设置所选派别支持率为92
                sm.set_party_support(percent_by_party)  # 更新支持率
                break  # 有效输入，跳出循环
        except ValueError:
            print("请输入一个有效的数字。")  # 非法输入提示

    # 显示更新后的状态
    print(f"更新后的：{['君主专制', '君主立宪', '代议政治'][new_government_id]}")
    print("更新后的派别支持率：")
    for i, percent in enumerate(percent_by_party):
        print(f"{parties[i]}: {percent}%")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # 当命令行包含--debug时，args.debug 为 True，否则为 False
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    # 解析命令行参数并返回参数
    args = parser.parse_args()
    main(debug=args.debug)
