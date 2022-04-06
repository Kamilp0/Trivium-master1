from bivium_class import BiviumSystem
from file_handler import *

system = BiviumSystem()

var_list = [f"x{i}" for i in range(93)] + [f"y{i}" for i in range(84)]

for j in range(0, 3):
    f = open_file(f"s_{j}")

    print(f"22 {len(var_list)}")
    print(" ".join(var_list))

    k = 0

    for i in range(j, 66, 3):

        line = f"R{k} "

        for var in var_list:
            
            var_to_check = f"{var[0]}{(int(var[1:]) + 1):02}"

            if {var_to_check} in system.z_free_bits[i][0]:
                line += "1 "
            else:
                line += "0 "

        k += 1
        print(line)

    close_file(f)