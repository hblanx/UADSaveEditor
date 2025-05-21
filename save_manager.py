# save_manager.py
import tools


class SaveManager:
    def __init__(self, data, debug=False):
        """
        初始化SaveManager类。

        参数:
            data: 包含游戏数据的字典
            debug: 是否启用调试模式，默认为False
        """
        self.data = data
        self.debug = debug
        self.start_year = self.data["StartYear"]
        self.player_info = self.__find_player_info()
        self.player_name = self.player_info["name"]
        self.government_type = self.player_info["government"]
        self.support_list = self.player_info["percentByParty"]

        print(f"存档信息:{self.start_year}-"
              f"{tools.calculate_current_date(self.start_year, self.get_turn())[0]}, "
              f"国家: {self.player_name}")

    def __find_player_info(self):
        """
        获取非AI玩家的信息。
        返回:返回非AI玩家的信息字典，如果未找到则返回None
        """
        for player in self.data["Players"]:
            if not player["isAi"]:
                return player
        return None

    def accelerate_current_research(self):
        """
        加速当前正在研究的科技项目。
        返回:修改的科技项目数量
        """
        modified_count = 0
        for player in self.data.get('Players', []):
            if player.get('isMain', False):  # 主要针对玩家国家
                for tech in player.get('techonologies', []):
                    if tech.get('progress', 0) < 100.0:
                        tech['progress'] = 99.9  # 保持为float，和原始数据一致
                        modified_count += 1
        return modified_count

    def accelerate_all_research(self):
        """
        加速所有科技研发项目。
        返回:修改的科技项目数量
        """
        modified_count = self.accelerate_current_research()
        # 获取所有科技名称
        all_tech_names = {tech['Key'] for tech in self.data.get('TechYears', [])}

        for player in self.data.get('Players', []):
            if player.get('isMain', False):  # 主要针对玩家国家
                tech_list = player.setdefault('techonologies', [])

                # 构建已有科技名称集合
                existing_names = {tech['name'] for tech in tech_list}

                # 只添加不存在的科技
                for name in all_tech_names - existing_names:
                    tech_list.append({
                        'index': -1,
                        'name': name,
                        'progress': 100.0
                    })
                    modified_count += 1
        return modified_count

    # 基本游戏信息获取与设置方法
    def get_turn(self):
        """
        获取当前回合数。
        返回:当前回合数
        """
        return self.data["CurrentDate"]["turn"]

    def set_turn(self, new_turn):
        """
        设置新的回合数。
        参数:new_turn: 新的回合数
        """
        self.data["CurrentDate"]["turn"] = new_turn

    def get_start_year(self):
        """
        获取游戏开始年份。
        返回:游戏开始年份
        """
        return self.start_year

    def display_current_date(self):
        """
        显示当前日期。
        返回:当前日期的字符串表示
        """
        turn = self.get_turn()
        year, month = tools.calculate_current_date(self.start_year, turn)
        return f"{year}年{month}月"

    def update_turn_by_date(self):
        """
        根据输入的年份和月份更新回合数。
        """
        print(f"当前日期为{self.display_current_date()}")
        try:
            year = int(input("请输入新的年份(如'1899'):"))
            month = int(input("请输入新的月份:"))
            new_turn = tools.calculate_turns_from_date(self.start_year, year, month)
            if new_turn != -1:
                self.set_turn(new_turn)
                print(f"修改日期为{self.display_current_date()}")
            else:
                print("数据错误")
        except ValueError:
            print("请输入有效的数字。")

    # 玩家资源相关方法
    def get_cash(self):
        """
        获取玩家的金钱数额。
        返回:玩家的金钱数额，如果未找到玩家则返回None
        """
        return self.player_info["cash"] if self.player_info else None

    def set_cash(self, new_cash):
        """
        设置玩家的金钱数额。
        参数:new_cash: 新的金钱数额
        返回:操作成功返回True，否则返回False
        """
        if self.player_info:
            self.player_info["cash"] = new_cash
            return True
        return False

    def get_shipyard(self):
        """
        获取玩家的船厂信息。
        返回:玩家的船厂信息，如果未找到玩家则返回None
        """
        return self.player_info["shipyard"] if self.player_info else None

    def set_shipyard(self, new_amount):
        """
        设置玩家的船厂信息。
        参数:new_amount: 新的船厂数额
        返回:操作成功返回True，否则返回False
        """
        if self.player_info:
            self.player_info["shipyard"] = new_amount
            self.player_info["shipyardBuildMonthLeft"] = 1
            return True
        return False

    def get_reputation(self):
        """
        获取玩家的声望。
        返回:玩家的声望，如果未找到玩家则返回None
        """
        return self.player_info["reputation"] if self.player_info else None

    def set_reputation(self, new_reputation):
        """
        设置玩家的声望。
        参数:new_reputation: 新的声望值
        返回:操作成功返回True，否则返回False
        """
        if self.player_info:
            self.player_info["reputation"] = new_reputation
            return True
        return False

    def get_respect(self):
        """
        获取玩家的骚乱值。
        返回:玩家的骚乱值，如果未找到玩家则返回None
        """
        return self.player_info["respect"] if self.player_info else None

    def set_respect(self, new_respect):
        """
        设置玩家的骚乱值。
        参数:new_respect: 新的骚乱值
        返回:操作成功返回True，否则返回False
        """
        if self.player_info:
            self.player_info["respect"] = new_respect
            return True
        return False

    # 船员相关方法
    def get_crew_pool(self):
        """
        获取玩家的船员数。
        返回:玩家的船员数，如果未找到玩家则返回None
        """
        return self.player_info["CrewPool"] if self.player_info else None

    def set_crew_pool(self, new_crew_pool):
        """
        设置玩家的船员数。
        参数:new_crew_pool: 新的船员数
        返回:操作成功返回True，否则返回False
        """
        if self.player_info:
            self.player_info["CrewPool"] = new_crew_pool
            return True
        return False

    def get_average_crew_pool_training(self):
        """
        获取玩家的平均船员训练水平。
        返回:玩家的平均船员训练水平，如果未找到玩家则返回None
        """
        return self.player_info["AverageCrewPoolTraining"] if self.player_info else None

    def set_average_crew_pool_training(self, new_training_level):
        """
        设置玩家的平均船员训练水平。
        参数:new_training_level: 新的平均船员训练水平
        返回:操作成功返回True，否则返回False
        """
        if self.player_info:
            self.player_info["AverageCrewPoolTraining"] = new_training_level
            return True
        return False

    # 政府与政党相关方法
    def get_government_type(self):
        """
        获取玩家的政府类型。
        返回:玩家的政府类型
        """
        return self.government_type

    def set_government_type(self, gid):
        """
        设置玩家的政府类型。
        参数:gid: 新的政府类型ID
        返回:操作成功返回True
        """
        self.government_type = gid
        if self.player_info:
            self.player_info["government"] = gid
        return True

    def get_party_support(self):
        """
        获取玩家的政党支持率。
        返回:玩家的政党支持率列表
        """
        return self.support_list

    def set_party_support(self, support_list):
        """
        设置玩家的政党支持率。
        参数:support_list: 新的政党支持率列表
        返回:操作成功返回True
        """
        self.support_list = support_list
        if self.player_info:
            self.player_info["percentByParty"] = support_list
        return True

    # 玩家国家信息方法
    def get_player_name(self):
        """
        获取玩家操控的国家名称。
        返回:玩家操控的国家名称字符串
        """
        return self.player_name

    def get_data(self):
        """
        获取游戏数据。
        返回:游戏数据字典
        """
        return self.data

    # 特殊加速功能方法
    def instant_construction(self):
        """
        将所有属于玩家的船只的建造、海试或维修时间缩短到1个月。
        返回:修改的船只数量
        """
        wrong_id = '00000000-0000-0000-0000-000000000000'
        i = 0

        for s in self.data['Ships']:
            # status: 1一般，3出海，2建造，11海试，4维修，5过期，10改装
            # currentRole: 0存在舰队，1制海，5防卫
            if s.get('playerName') != self.player_name:  # 是玩家国家
                continue
            if s.get('designId') == wrong_id:  # 不是设计id
                continue
            if s['buildingProgress'] < 100 and s['status'] in [2, 11]:
                s['buildingProgress'] = 99
                i += 1
                if self.debug:
                    try:
                        print(f"加速建造、海试{s['vesselName']}, status:{s['status']}")
                    except Exception as e:
                        print(e)
            if s['repairingProgress'] < 100 and s['status'] == 4:
                s['repairingProgress'] = 99
                i += 1
                if self.debug:
                    try:
                        print(f"加速修复{s['vesselName']}, status:{s['status']}")
                    except Exception as e:
                        print(e)
            if s['status'] == 10:
                s['refitProgress'] = 99
                i += 1
                if self.debug:
                    try:
                        print(f"加速改装{s['vesselName']}, status:{s['status']}")
                    except Exception as e:
                        print(e)
        return i

    def instant_colonial_conquest(self):
        """
        将所有属于玩家的所有入侵事件的吨位降为100，回合数改为1。
        返回:修改的事件数量
        """
        i = 0
        if self.data['ColonialConquestEvents']:
            for e in self.data['ColonialConquestEvents']:
                if e['Attacker'] == self.player_name:
                    e['RequiredTonnage'] = 100
                    e['DurationTotal'] = 1
                    i += 1
        return i

    # 移动相关方法
    def get_moving_groups(self):
        """
        获取所有属于玩家且处于移动状态的船团列表。
        返回:(groups, index_map) 元组，其中：
                groups: 可移动船只的列表
                index_map: 这些船只在self.data中的索引列表
        """
        groups = []
        index_map = []  # 存储筛选后的小组在原始列表中的索引
        for index, group in enumerate(self.data['MovingGroups']):
            if group.get('Player') == self.player_name:
                groups.append(group)
                index_map.append(index)  # 记录筛选后的小组在原始数据中的索引位置
        return groups, index_map

    def instant_move(self, original_index):
        """
        瞬间完成指定船团的移动。
        参数:original_index: 选定的移动小组在self.data中的原始索引
        返回:操作成功返回True，否则返回False
        """
        try:
            group = self.data['MovingGroups'][original_index]
            # FullPath和WorldPos似乎没有作用
            # 更新CurrentPositionIndex为FullPath最后一个元素的索引
            group['CurrentPositionIndex'] = len(group['FullPath']) - 1
            return True
        except Exception as e:
            print(f"移动失败: {e}")
            return False

    # 省份相关方法
    def get_provinces(self):
        """
        获取省份数据。
        返回:省份数据列表
        """
        return self.data["Provinces"]

    def set_provinces(self, provinces):
        """
        设置provinces列表。
        参数:provinces: 需要保存的provinces列表
        返回:操作成功返回True
        """
        self.data["Provinces"] = provinces
        return True

    def get_provinces_not_discovered_oil(self):
        """
        从数据中提取并处理尚未发现石油的省份列表，并创建省份名称到原始Id的映射。
        返回:(provinces, name_to_id_map) 元组，其中：
                provinces: 包含省份名称的列表
                name_to_id_map: 省份名称到Id的映射字典
        """
        provinces = []
        name_to_id_map = {}
        for p in self.data['ProvincesNotYetDiscoveredOil']:
            original_name = p['Id']
            cleaned_name = original_name.replace("_", " ").lower()
            provinces.append(cleaned_name)
            name_to_id_map[cleaned_name] = original_name
        return provinces, name_to_id_map

    def set_is_oil_discovery(self, province_id):
        """
        设置指定的省份发现油田。
        参数:province_id: 要设置油田发现状态的省份的Id
        返回:如果找到对应的省份并成功设置状态，则返回True；否则返回False
        """
        for p in self.data['Provinces']:
            if p['Id'] == province_id:
                p['isOilDiscovery'] = True
                return True
        return False

    # 国家关系相关方法
    def get_attitude(self, country_a, country_b):
        """
        获取两个国家之间的attitude。
        参数:
            country_a: 第一个国家的名称
            country_b: 第二个国家的名称
        返回:如果找到关系并成功获取attitude，则返回attitude值；否则返回None
        """
        relations = self.data['Relations']
        for relation in relations:
            if relation['a'] == country_a and relation['b'] == country_b:
                return relation['attitude']
        return None

    def set_attitude(self, country_a, country_b, new_attitude):
        """
        设置两个国家之间的attitude。
        参数:
            country_a: 第一个国家的名称
            country_b: 第二个国家的名称
            new_attitude: 新的attitude值
        返回:如果找到关系并成功设置attitude，则返回True；否则返回False
        """
        relations = self.data['Relations']
        for relation in relations:
            if relation['a'] == country_a and relation['b'] == country_b:
                relation['attitude'] = new_attitude
                return True
        return False

    def build_relations_matrix(self):
        """
        构建关系矩阵。返回一个二维数组，表示各个国家之间的attitude，以及一个国家名称列表。
        返回:
            (matrix, countries) 元组，其中：
                matrix: 表示国家间关系的二维数组
                countries: 按顺序排列的国家名称列表
        """
        # 收集所有国家名称
        countries = set()
        for relation in self.data['Relations']:
            countries.add(relation['a'])
            countries.add(relation['b'])
        countries = list(countries)

        # 创建二维数组，初始值设为None
        matrix = [[None for _ in countries] for _ in countries]

        # 填充数组
        # 遍历所有关系，将attitude值填入对应的矩阵单元格
        for relation in self.data['Relations']:
            a_index = countries.index(relation['a'])  # 获取国家a在列表中的索引
            b_index = countries.index(relation['b'])  # 获取国家b在列表中的索引
            matrix[a_index][b_index] = relation['attitude']  # 设置a到b的attitude
            matrix[b_index][a_index] = relation['attitude']  # 如果关系是双向的，也设置b到a的attitude

        return matrix, countries