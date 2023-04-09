from potentials.config import calculate_fun, save_results_fun



def calc(qs={(50, 50): 1}, real_size=(600, 600), radius_e=10, k=1):
    try:
        # TODO: передача аргументов из вне(из GUI)
        print('calculating')
        # qs = {}
        # for i in range(10):
        #     qs[randint(0, real_width),
        #        randint(0, real_height)] = uniform(-1000, 1000)  # randint(1, 100) / 100
        # for fi in range(360):
        #     qs[real_width / 2 + 100 * cos(fi / 180 * pi), real_height / 2 + 100 * sin(fi / 180 * pi)] = 1

        # qs[150, 150] = -1
        # qs[600, 600] = 1

        results = calculate_fun(qs, real_size, radius_e, k)
        # save_results_fun('potentials/modules/calc/' + calc_filename, results)

        print('calculated')
        return results
    except Exception as ex:
        print(ex)
