from re import sub, split
from multiprocessing import Process
from sympy.logic.boolalg import to_cnf
from process import start_and_wait, output, index_div

def anf_to_cnf(equations):
    cnf_equations = []

    for expression in equations:
        cnf_equations.append(str(to_cnf(expression)))

    output.put(cnf_equations)

def build_cnf_row(expression, var_dict, var_index, xor = False):

    var_list = []

    for variable in expression:
            
        if variable[0] != "-":
            var = variable
            pre_op = ""
        else:
            var = variable[1:]
            pre_op = "-"

        if var not in var_dict:
            var_dict[var] = var_index
            var_index += 1

        var_list.append(f"{pre_op}{var_dict[var]}")

    return f"\n{'x' if xor else ''}{' '.join(var_list)} 0", var_index

def to_cnf_file(linear_equations, non_linear_equations):

    var_dict = {}
    var_index = 1
    cnf_system = ""
    num_rows = 0

    for anf_equation in linear_equations:
        cnf_row, var_index = build_cnf_row(anf_equation.split(), var_dict, var_index, True)
        cnf_system += cnf_row
        num_rows += 1
        
    for cnf_equation in non_linear_equations:
        for literal in sub("[()]", "", cnf_equation.replace("~", "-")).split(" & "):
            cnf_row, var_index = build_cnf_row(literal.split(" | "), var_dict, var_index)
            cnf_system += cnf_row
            num_rows += 1

    print(f"p cnf {var_index - 1} {num_rows}" + cnf_system)

    return var_dict

def system_to_cnf(linear_equations, non_linear_equations):
    l = len(non_linear_equations)
    processes = [Process(target = anf_to_cnf, args = (non_linear_equations[index_div(l, i, 8):index_div(l, i + 1, 8)], )) for i in range(8)]

    return to_cnf_file(linear_equations, start_and_wait(processes))

"""
f = open("true_sat.txt", "r")
a = f.readlines()
for x in range(len(a)):
    a[x] = a[x].replace("\n", "")

equations_to_cnf([], a, "test")
"""