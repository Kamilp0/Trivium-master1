from file_handler import *
from bivium_class import BiviumSystem
import time

var_list = input("Scegliere le variabili da fissare: ").rstrip().split()

for i in range(1, 101):
    t0 = time.time()
    system = BiviumSystem()

    system.substitute_bits(var_list)
    system.find_free_bits()

    system.create_simple_nonlinear_aux()

    system.sat_solve()
    """
    f = open_file(f"crypto_test/gauss_benchmark/{i}", "cnf")
    system.print_cnf()
    close_file(f)
    """

    t1 = time.time()
    print(t1-t0)