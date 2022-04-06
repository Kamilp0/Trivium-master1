from bivium_class import BiviumSystem
from file_handler import *

system = BiviumSystem()
system.create_simple_nonlinear_aux()           

var_list = [f"x{i}" for i in range(93)] + [f"y{i}" for i in range(84)] + [f"a{i}" for i in range(len(system.aux_system))]

f = open_file("matrix_prof")

print(f"{len(system.keystream)} {len(var_list)}")
print(" ".join(var_list))

for i in range(len(system.keystream)):

    line = f"R{i} "

    for var in var_list:
        if var[0] == "a":
            var_to_check = f"{var[0]}{(int(var[1:]) + 1)}"
        else:
            var_to_check = f"{var[0]}{(int(var[1:]) + 1):02}"

        if {var_to_check} in system.z_free_bits[i][0]:
           line += "1 "
        else:
            line += "0 "

    print(line)

close_file(f)