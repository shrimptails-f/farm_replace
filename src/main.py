import plant
import util
import do_harvest

world_size = get_world_size()
planted_count = plant.get_planted_count(world_size)


while True:
    smp = None  # sunflower_max_position
    smv = 0  # sunflower_max_value
    for _ in range(world_size):
        x = get_pos_x()
        for _ in range(world_size):
            y = get_pos_y()
            entity_type = get_entity_type()

            # ひまわーの測定と記録
            smv, smp = do_harvest.get_sunflower_record(entity_type, smp, smv, x, y)
            # ひまわりとサボテン以外収穫
            planted_count = do_harvest.do_harvest(entity_type, planted_count)
            planted_count = plant.do_plant(x, y, planted_count)
            util.do_water(entity_type)
            util.move_y()
        util.move_x()

    # ひまわり収穫
    if smp == None:
        continue
    planted_count = do_harvest.harvest_sunflower(planted_count, smp)
    planted_count = do_harvest.harvest_cactus(world_size, planted_count)
