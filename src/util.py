import consts


# 直感と反しているのでラップする
def move_x(x=0):
    x += 1
    for i in range(x):
        move(East)


# 直感と反しているのでラップする
def move_y(y=0):
    y += 1
    for i in range(y):
        move(North)


# 偶数チェック
def __is_even(n):
    return n % 2 == 0


# かぼちゃの植える座標の場合、Trueを返します。
def is_limit_pumpkin_area(x, y):
    if (x) <= 3 and (y) <= 3:
        return True
    return False


# かぼちゃの植える座標の場合、Trueを返します。
def is_limit_cactus(x, y):
    x_low = consts.CACTUS_LOWER_LIMIT
    x_up = consts.CACTUS_UP_LIMIT
    r_up = consts.CACTUS_RIGHT_LIMIT
    if (x) >= x_low and (x) <= x_up and (y) <= r_up:
        return True
    return False


# 木を植えるマスか判定します
def current_even(x, y):
    if __is_even(x + 1) == False:
        if __is_even(y + 1):
            return True
    if __is_even(x + 1):
        if __is_even(y + 1) == False:
            return True
    return False


# 畑を草状態にします。草状態ならそのままにします
def __set_glassLand():
    if get_ground_type() != Grounds.Grassland:
        till()


# 畑を耕した状態にします。耕した状態ならそのままにします。
def __set_soliLand():
    if get_ground_type() != Grounds.Soil:
        till()


# 受け取った引数のタイプの状態の畑にするか、受け取った引数のタイプを維持します。
def set_ground(type):
    if type == Grounds.Grassland:
        __set_glassLand()
    elif type == Grounds.Soil:
        __set_soliLand()


# 水を0.5以上所持していたら0.25水をやります。
def do_water(entity_type):
    if entity_type == None:
        return
    if get_ground_type() == Grounds.Grassland:
        return
    if num_items(Items.Water) >= 0.75 and get_water() < 0.75:
        use_item(Items.Water)
        use_item(Items.Water)
        use_item(Items.Water)
