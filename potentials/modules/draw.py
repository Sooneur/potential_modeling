from PIL import Image


radius_e = 0.1


# TODO: Переделать разделенные данные картинки в класс
def draw(potentials: list, pic_size: tuple, real_pic: float, safe_zones: list, safe_radius: int, n: int, e: float):
    width, height = pic_size
    width_m, height_m = round(width / real_pic), round(height / real_pic)
    image = Image.new('RGB', pic_size, 'white')
    pixels = image.load()
    toggle_all = True
    moving_e = False
    # TODO: вынести
    plus_val = []
    minus_val = []
    vals = []
    es = {}
    for y in range(height_m):
        for x in range(width_m):
            if safe_zones[y][x] <= safe_radius:
                potentials[y][x] = "-"

            if safe_zones[y][x] == 0:
                potentials[y][x] = "*"

            if potentials[y][x] in ("*", "-"):
                continue
            # TODO: наладить структуру для отрицательных
            # TODO: toggle: расчет полей по полным данным - по отдельным
            if toggle_all:
                vals.append(float(potentials[y][x]))
            else:
                if float(potentials[y][x]) < 0:
                    minus_val.append(float(potentials[y][x]))
                else:
                    plus_val.append(float(potentials[y][x]))

    # TODO: Распределение уровней по полной длине трека(всем значением)
    d_potentials = {}
    if vals:
        val_max, val_min = max(vals), min(vals)
        step = (val_max - val_min) / n
        level_to_color = 256 / n
        levels = {}
        if moving_e:
            for val in vals:
                if abs(step - (val - val_min)) % step <= e:
                    if levels.get(val // step, False):
                        levels[val // step].append(val)
                    else:
                        levels[val // step] = [val]

            for key in levels.keys():
                nums = levels[key]
                nums.sort()
                # nums = nums[int((len(nums)) / 2 ** key):int(len(nums)) - int(len(nums) / 2 ** key)]
                try:
                    es[key] = (max(nums) - min(nums)) / 2 / 1.08 ** abs(key)
                except Exception as e:
                    print(e)
                    print(key, len(nums), nums)
                    print(len(levels[key]), levels[key])
                    print()

    if plus_val:
        plus_max, plus_min = max(plus_val), min(plus_val)
        plus_step = (plus_max - plus_min) / n
    if minus_val:
        minus_max, minus_min = max(minus_val), min(minus_val)
        minus_step = (minus_max - minus_min) / n

    for y in range(height):
        for x in range(width):
            x_m, y_m = min(width_m - 1, round(x / real_pic)), min(height_m - 1, round(y / real_pic))
            if potentials[y_m][x_m] == "*":
                pixels[x, y] = 0, 0, 0
                continue

            if potentials[y_m][x_m] == "-":
                pixels[x, y] = 0, 255, 0
                continue

            # TODO: как быстро рисовать погрешности
            # 0
            if vals:
                level = abs(step - (float(potentials[y_m][x_m]) - val_min))
                if moving_e:
                    if level % step <= es.get(int(level // step), 0):
                        color = int(level / step * level_to_color ** 110)
                        if float(potentials[y_m][x_m]) > 0:
                            pixels[x, y] = color, 0, 0
                        else:
                            pixels[x, y] = 0, 0, color
                else:
                    if level % step <= e:
                        color = int(level / step * level_to_color)
                        if float(potentials[y_m][x_m]) > 0:
                            pixels[x, y] = color, 0, 0
                        else:
                            pixels[x, y] = 0, 0, color

            if minus_val:
                if abs(minus_step - (float(potentials[y_m][x_m]) - minus_min)) % minus_step <= e:
                    pixels[x, y] = 0, 0, 255
            if plus_val:
                if abs(plus_step - (float(potentials[y_m][x_m]) - plus_min)) % plus_step <= e:
                    pixels[x, y] = 255, 0, 0
            # 1
            # k = min_p
            # while k < max_p:
            #     if abs(float(potentials[y_m][x_m]) - k) <= e:
            #         pixels[x, y] = 255, 0, 0
            #         break
            #     k += step.

    return image
