import os
import re


import ujson as json
import tools


class JsonLoader:
    def __init__(self, debug=False):
        """
        初始化JsonLoader类。
        :param debug: 是否为调试模式。调试模式下会从测试目录读取存档文件。
        """
        self.debug = debug
        if self.debug:
            self.directory = "./test_save"
        else:
            self.directory = tools.get_game_save_directory()
        self.selected_file_path = None  # 保存当前选中的文件路径
        try:
            self.__save_files = self.__find_save_files()
        except Exception as e:
            print(f"读取存档出现错误: {e}")
            self.__save_files = []

    def __find_save_files(self):
        """
        在指定目录下查找所有符合格式的存档文件。
        :return: 包含所有找到的存档文件路径的列表。
        """
        save_files = []
        for filename in os.listdir(self.directory):
            if re.match(r'save_\d+\.json', filename):
                full_path = os.path.join(self.directory, filename)
                save_files.append(full_path)
        return save_files

    def select_save_file(self):
        """
        提示用户选择存档文件。
        :return: 用户选择的存档文件的路径。
        """
        print(f"识别到存档路径为:{self.directory}")
        if not self.__save_files:
            print("没有识别到有效的JSON存档，请检查是否将普通存档转化为JSON存档。")
            choice = input("按[0]打开存档位置后退出，按下回车直接退出: ")
            if choice == "0":
                try:
                    os.startfile(self.directory)
                except Exception as e:
                    print("存档文件夹不存在")
            return None
        else:
            print("请选择一个存档进行加载：")
            for i, filename in enumerate(self.__save_files):
                print(f"[{i + 1}]", end=" ")
                print(filename.split('\\')[-1])
            print("[0] 打开存档位置")

        while True:
            choice = input("输入数字选择存档（直接按下回车退出）：")
            if choice == "":
                return None

            try:
                selected_index = int(choice) - 1
                if 0 <= selected_index < len(self.__save_files):  # 选择存档
                    self.selected_file_path = self.__save_files[selected_index]  # 保存选中的文件路径
                    return self.selected_file_path
                elif selected_index == -1:  # 打开存档文件夹
                    if self.debug:
                        save_path = os.getcwd()
                        save_path = os.path.join(save_path, self.directory)
                        os.startfile(save_path)
                    else:
                        os.startfile(self.directory)
                else:
                    print("选择无效，请重新输入")
            except ValueError:
                print("选择无效，请重新输入")

    def read_json_file(self, filepath):
        # 使用不同编码读取json文件
        logs = ""
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'utf-16', 'gbk']
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    data = json.load(file)
                    return data
            except Exception as e:
                logs += str(e) + "\n"
        print(f"尝试所有编码均失败。\n错误日志：{logs}")
        return None

    def save_json_file(self, data, backup=False):
        """
        将数据保存到JSON文件。
        :param data: 要保存的数据。
        :param backup: 是否创建文件的备份。
        """
        if backup:
            pass

        try:
            with open(self.selected_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
            print(f"{os.path.basename(self.selected_file_path)},文件已保存。")
        except Exception as e:
            print(f"保存文件出错: {e}")
