import ctypes
import os
import difflib


def calculate_current_date(start_year, turns):
    if start_year < 1890 or turns < 0:
        print("数据错误")
        return -1, -1

    years_passed = turns // 12
    current_month = turns % 12 + 1  # +1 月份从1月开始
    current_year = start_year + years_passed

    return current_year, current_month


def calculate_turns_from_date(start_year, current_year, current_month):
    if start_year < 1890 or current_year < start_year or current_month < 1 or current_month > 12:
        # 数据错误
        return -1

    year_difference = current_year - start_year
    turns = year_difference * 12 + current_month - 1  # -1 是因为月份从1开始

    return turns


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def print_logo():
    print('''   _    _           _____    _____                     ______     _  _  _               
  | |  | |   /\    |  __ \  / ____|                   |  ____|   | |(_)| |              
  | |  | |  /  \   | |  | || (___    __ _ __   __ ___ | |__    __| | _ | |_  ___   _ __ 
  | |  | | / /\ \  | |  | | \___ \  / _` |\ \ / // _ \|  __|  / _` || || __|/ _ \ | '__|
  | |__| |/ ____ \ | |__| | ____) || (_| | \ V /|  __/| |____| (_| || || |_| (_) || |   
   \____//_/    \_\|_____/ |_____/  \__,_|  \_/  \___||______|\__,_||_| \__|\___/ |_|  --by hblanx
   ''')


def get_game_save_directory():
    user_home_directory = os.path.expanduser('~')  # 获取用户主目录
    game_save_directory = os.path.join(user_home_directory, "AppData", "LocalLow", "Game Labs",
                                       "Ultimate Admiral Dreadnoughts")
    return game_save_directory

def print_relations_matrix(matrix, countries):
    """
    打印国家间的关系矩阵。
    :param matrix: 包含国家间关系值的二维数组。
    :param countries: 国家名称列表，用于标识矩阵中的行和列。
    """
    length = 8 # 假设国家名称不超过length个字符
    # 打印表头
    header = " " * length
    for country in countries:
        header += f"{country:>{length}}"  # 为每个国家名称分配length个字符宽度
    print(header)

    # 打印每一行
    for i, row in enumerate(matrix):
        row_str = f"{countries[i]:<{length}}"  # 左对齐国家名称
        for cell in row:
            if cell is not None:
                row_str += f"{cell:.0f}".rjust(length)  # 格式化为整数并右对齐
            else:
                row_str += " " * length  # 空单元格
        print(row_str)

class GovernmentMapping:
    def __init__(self):
        pass

# 测试代码
if __name__ == '__main__':
    try:
        # 测试计算当前日期
        year, month = calculate_current_date(1890, 431)
        print(f"当前日期是：{year}年{month}月")

        # 测试反推回合数
        turns = calculate_turns_from_date(1890, 1900, 1)
        print(f"回合数是：{turns}")

        year, month = calculate_current_date(1890, turns)
        print(f"修改后日期是：{year}年{month}月")
    except ValueError as e:
        print(e)


def fuzzy_search(user_input, options, cutoff=0.3, n=5):
    """
    提供模糊搜索功能，并允许用户从相似项中选择一个。

    :param user_input: 用户输入的值。
    :param options: 可选择的列表（如省份或国家名称列表）。
    :param cutoff: 相似度的最低阈值，默认为0.3。
    :param n: 返回最接近的选项数量，默认为5。
    :return: 用户选择的项或新的搜索关键词。
    """
    # 使用 difflib 获取与输入相似的建议列表
    if user_input in options:
        return user_input
    suggestions = difflib.get_close_matches(user_input, options, n=n, cutoff=cutoff)
    if suggestions:
        print("您可能在寻找: ")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

        # 让用户选择一个项，输入数字或重新搜索
        choice_input = input("请选择一个选项（输入数字）或者输入完整名称进行设置：").lower()
        if choice_input.isdigit() and 1 <= int(choice_input) <= len(suggestions):
            # 如果用户输入数字，返回对应的选择项
            return suggestions[int(choice_input) - 1]
        else:
            # 如果输入非数字，返回重新搜索的关键词
            return choice_input
    else:
        print("未找到匹配的选项，请重新输入。")
        return None


# 全局政府类型映射字典
GOVERNMENT_MAPPING = {
    0: "君主专制",
    1: "君主立宪",
    2: "代议政治",
}

def get_government_name_by_id(gid):
    """
    根据ID获取政府名称。
    """
    return GOVERNMENT_MAPPING[gid]

def list_government_types():
    """
    返回所有政府类型及其对应的ID。
    """
    msg = ''
    for gid, gname in GOVERNMENT_MAPPING.items():
        msg += f"{gid}: {gname}\n"
    return msg

def get_float_input(prompt, allow_empty=True):
    """
    获取用户浮点数输入，支持空输入和错误处理
    非浮点数返回None
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_empty:
            return None
        try:
            return float(user_input)
        except ValueError:
            print("输入无效，请输入一个有效的数字。")

def get_int_input(prompt, allow_empty=True, min_value=None, max_value=None):
    """获取用户整数输入，支持空输入、范围限制和错误处理"""
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_empty:
            return None
        try:
            value = int(user_input)
            if min_value is not None and value < min_value:
                print(f"输入必须大于或等于 {min_value}。")
                continue
            if max_value is not None and value > max_value:
                print(f"输入必须小于或等于 {max_value}。")
                continue
            return value
        except ValueError:
            print("输入无效，请输入一个有效的整数。")