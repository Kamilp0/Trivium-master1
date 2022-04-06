from re import sub, split

def aux_to_cnf(aux_system):
    cnf_equations = []

    for i in range(len(aux_system)):
        l = list(aux_system[i][0])
        
        if len(l) == 2:
            cnf_equations.append(f"(~a{i + 1} | {l[0]}) & (~a{i + 1} | {l[1]}) & (a{i + 1} | ~{l[0]} | ~{l[1]})")
        elif len(l) == 3:
            cnf_equations.append(f"(~a{i + 1} | {l[0]}) & (~a{i + 1} | {l[1]}) & (~a{i + 1} | {l[2]}) & (a{i + 1} | ~{l[0]} | ~{l[1]} | ~{l[2]})")
        else:
            raise Exception("wtf")
    
    return cnf_equations

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

def system_to_cnf(linear_equations, aux_system):
    cnf = aux_to_cnf(aux_system)
    to_cnf_file(linear_equations, cnf)