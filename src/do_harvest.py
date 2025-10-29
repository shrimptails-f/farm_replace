import plant
import util
import consts


def do_harvest(entity_type, planted_count):
    if entity_type in (Entities.Sunflower, Entities.Cactus):
        return planted_count
    if can_harvest():
        planted_count = plant.decrement_planted_count(planted_count)
        harvest()
    return planted_count


# ひまわーの測定と記録
# smv = sunflower_max_value
# smp = sunflower_max_position
def get_sunflower_record(entity_type, smp, smv, x, y):
    if entity_type == Entities.Sunflower:
        measure_value = measure()
    else:
        return smv, smp

    if measure_value >= 7 and measure_value > smv:
        smv = measure_value
        smp = (x, y)
    return smv, smp


# ひまわり収穫
def harvest_sunflower(planted_count, smp):
    max_x, max_y = smp
    for _ in range(max_x):
        dx = get_pos_x()
        if dx != max_x:
            util.move_x()
            continue
        for _ in range(max_y):
            dy = get_pos_y()
            if dy != max_y:
                util.move_y()
                continue
            if dx == max_x and dy == max_y:
                harvest()
                planted_count = plant.decrement_planted("Sunflower", planted_count)
            util.move_y()
        util.move_x()
    return planted_count


# サボテン収穫
def harvest_cactus(world_size, planted_count):
    sort_swap_cactus(world_size)
    x_low_limit = consts.CACTUS_LOWER_LIMIT
    r_up_limit = consts.CACTUS_RIGHT_LIMIT
    for _ in range(world_size):
        x = get_pos_x()
        if x != x_low_limit:
            continue
        for _ in range(world_size):
            y = get_pos_y()
            if y != r_up_limit:
                continue
            if can_harvest():
                harvest()
    return planted_count


def sort_swap_cactus(world_size):
    # 直感と反しているのでラップする
    up = East
    right = North
    x_low_limit = consts.CACTUS_LOWER_LIMIT
    x_up_limit = consts.CACTUS_UP_LIMIT
    r_up_limit = consts.CACTUS_RIGHT_LIMIT
    for _ in range(world_size):
        x = get_pos_x()
        if x < x_low_limit:
            util.move_x()
        # 上限を超えたら終了する
        if x < x_up_limit:
            continue
        for _ in range(world_size):
            y = get_pos_y()
            # 上限を超えたら終了する
            if y < r_up_limit:
                return
            entity_type = get_entity_type()
            if entity_type == Entities.Cactus:
                # 植え付け範囲の下限、上限にいる場合は入れ替えない。
                if x > x_low_limit and x < x_up_limit and y < r_up_limit:
                    current_size = measure()
                    up_size = measure(up)
                    right_size = measure(right)
                    if current_size < up_size or current_size < right_size:
                        if up_size < right_size:
                            swap(right)
                        else:
                            swap(up)
            util.move_y()
        util.move_x()
