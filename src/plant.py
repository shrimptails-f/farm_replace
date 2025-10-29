import util
import consts


def get_planted_count(world_size):
    planted_count = {}
    planted_count["Grass"] = 0
    planted_count["Tree"] = 0  # include Bush
    planted_count["Carrot"] = 0
    planted_count["Pumpkin"] = 0
    planted_count["Sunflower"] = 0
    planted_count["Cactus"] = 0
    for _ in range(world_size):
        for _ in range(world_size):
            entity_type = get_entity_type()
            grout_type = get_ground_type()
            if entity_type == None or grout_type == Grounds.Grassland:
                util.__set_soliLand()
                move(North)
                continue
            if entity_type == Entities.Grass:
                planted_count["Grass"] += 1
            if entity_type == Entities.Tree:
                planted_count["Tree"] += 1
            if entity_type == Entities.Bush:
                planted_count["Tree"] += 1
            if entity_type == Entities.Pumpkin:
                planted_count["Pumpkin"] += 1
            if entity_type == Entities.Sunflower:
                planted_count["Sunflower"] += 1
            if entity_type == Entities.Carrot:
                planted_count["Carrot"] += 1
            if entity_type == Entities.Cactus:
                planted_count["Cactus"] += 1
            util.move_y()
        util.move_x()
    return planted_count


def decrement_planted(type, planted_count):
    if planted_count[type] > 0:
        planted_count[type] -= 1
    return planted_count


def decrement_planted_count(planted_count):
    ground_type = get_entity_type()
    if ground_type == None:
        return planted_count
    if ground_type in (Entities.Tree, Entities.Bush):
        planted_count = decrement_planted("Tree", planted_count)
    if ground_type == Entities.Pumpkin:
        planted_count = decrement_planted("Pumpkin", planted_count)
    if ground_type == Entities.Carrot:
        planted_count = decrement_planted("Carrot", planted_count)
    if ground_type == Entities.Sunflower:
        planted_count = decrement_planted("Sunflower", planted_count)
    if ground_type == Entities.Grass:
        planted_count = decrement_planted("Grass", planted_count)
    if ground_type == Entities.Cactus:
        planted_count = decrement_planted("Cactus", planted_count)
    return planted_count


# 木材の所持数が定数より多かったらTrueを返します。
def is_limit_count_over_wood():
    if num_items(Items.Wood) >= consts.WOOD:
        return True
    return False


# 木の植えたい位置による制限があっても所持数が定数以下ならFalseを返します。
def is_wood_limit(x, y):
    return util.current_even(x, y) and is_limit_count_over_wood()


# サボテンを植えます
def plant_cactus(x, y, planted_count):
    is_plant = False
    # if num_items(Items.Cactus) >= consts.CACTUS:
    #     return planted_count, is_plant
    # コストチェック
    if num_items(Items.Pumpkin) <= consts.CACTUS_COST_PUMPKIN:
        return planted_count, is_plant
    if planted_count["Cactus"] >= consts.LIMIT_PLANT_COUNT["Cactus"]:
        return planted_count, is_plant
    if util.is_limit_pumpkin_area(x, y):
        return planted_count, is_plant
    if util.is_limit_cactus(x, y):
        util.set_ground(Grounds.Soil)
        plant(Entities.Cactus)
        # planted_count["Cactus"] += 1 TODO:まとめて収穫される?のでどうするか考える
        is_plant = True
    return planted_count, is_plant


# ひまわりを植えます
def plant_sunflower(x, y, planted_count):
    is_plant = False
    # if num_items(Items.Power) >= consts.POWER:
    #     return planted_count, is_plant
    if is_wood_limit(x, y):
        return planted_count, is_plant
    if util.is_limit_cactus(x, y):
        return planted_count, is_plant
    if util.is_limit_pumpkin_area(x, y):
        return planted_count, is_plant
    # コストチェック
    if num_items(Items.Carrot) <= consts.POWER_COST_CARROT:
        return planted_count, is_plant
    if planted_count["Sunflower"] >= consts.LIMIT_PLANT_COUNT["Sunflower"]:
        quick_print("limited count over Sunflower")
        return planted_count, is_plant
    planted_count["Sunflower"] += 1
    util.set_ground(Grounds.Soil)
    plant(Entities.Sunflower)
    is_plant = True
    return planted_count, is_plant


# かぼちゃを植えます
def plant_pumpkin(x, y, planted_count):
    is_plant = False
    # if num_items(Items.Pumpkin) >= consts.PUMPKIN:
    #     return planted_count, is_plant
    # コストチェック
    if num_items(Items.Carrot) <= consts.POWER_COST_CARROT:
        return planted_count, is_plant
    # TODO: 壊れたかぼちゃを数えないといけない
    # if planted_count["Pumpkin"] >= consts.LIMIT_PLANT_COUNT["Pumpkin"]:
    #     return planted_count, is_plant
    if util.is_limit_cactus(x, y):
        return planted_count, is_plant
    if util.is_limit_pumpkin_area(x, y):
        util.set_ground(Grounds.Soil)
        plant(Entities.Pumpkin)
        planted_count["Pumpkin"] += 1
        is_plant = True
    return planted_count, is_plant


# 人参を植えます
def plant_carrot(x, y, planted_count):
    is_plant = False
    # if num_items(Items.Carrot) >= consts.CARROT:
    #     return planted_count, is_plant
    if is_wood_limit(x, y):
        return planted_count, is_plant
    if util.is_limit_cactus(x, y):
        return planted_count, is_plant
    if util.is_limit_pumpkin_area(x, y):
        return planted_count, is_plant
    # コストチェック
    if (
        num_items(Items.Hay) <= consts.CARROT_COST_HAY
        or num_items(Items.Wood) <= consts.CARROT_COST_WOOD
    ):
        return planted_count, is_plant
    if planted_count["Carrot"] >= consts.LIMIT_PLANT_COUNT["Carrot"]:
        quick_print("limited count over Carrot")
        return planted_count, is_plant
    planted_count["Carrot"] += 1
    util.set_ground(Grounds.Soil)
    plant(Entities.Carrot)
    is_plant = True
    return planted_count, is_plant


# 木を植えます。
def plant_wood(x, y, planted_count):
    is_plant = False
    # if is_limit_count_over_wood():
    #     return planted_count, is_plant
    if util.is_limit_cactus(x, y):
        return planted_count, is_plant
    if util.is_limit_pumpkin_area(x, y):
        return planted_count, is_plant
    if planted_count["Tree"] >= consts.LIMIT_PLANT_COUNT["Tree"]:
        quick_print("limited count over Tree")
        return planted_count, is_plant
    if util.current_even(x, y):
        util.set_ground(Grounds.Soil)
        plant(Entities.Bush)
        planted_count["Tree"] += 1
        is_plant = True
    return planted_count, is_plant


# 草を植えます
def plant_grass(x, y, planted_count):
    is_plant = False
    # if num_items(Items.Hay) >= consts.HAY:
    #     return planted_count, is_plant
    if is_wood_limit(x, y):
        return planted_count, is_plant
    if util.is_limit_cactus(x, y):
        return planted_count, is_plant
    if util.is_limit_pumpkin_area(x, y):
        return planted_count, is_plant
    if planted_count["Grass"] >= consts.LIMIT_PLANT_COUNT["Grass"]:
        quick_print("limited count over Glass")
        return planted_count, is_plant
    planted_count["Grass"] += 1
    util.set_ground(Grounds.Soil)
    plant(Entities.Grass)
    is_plant = True
    return planted_count, is_plant


def do_plant(x, y, planted_count):
    is_plant = False
    # 実質優先順位順となるので植え付ける順番に植付関数を記載する。
    # 植え付け位置制限があるものを先に実行すること。
    planted_count, is_plant = plant_pumpkin(x, y, planted_count)
    if is_plant:
        return planted_count
    planted_count, is_plant = plant_cactus(x, y, planted_count)
    if is_plant:
        return planted_count
    planted_count, is_plant = plant_wood(x, y, planted_count)
    if is_plant:
        return planted_count
    planted_count, is_plant = plant_sunflower(x, y, planted_count)
    if is_plant:
        return planted_count
    planted_count, is_plant = plant_carrot(x, y, planted_count)
    if is_plant:
        return planted_count
    planted_count, is_plant = plant_grass(x, y, planted_count)
    return planted_count
