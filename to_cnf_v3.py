from pycryptosat import Solver
import time

def solve(main_system, aux_system):
    start = time.time()
    sat = Solver()

    var_dict = {}
    var_index = 1

    for equation, const in main_system:
        xor_clause = []

        for var, in equation:
            if var not in var_dict:
                var_dict[var] = var_index
                xor_clause.append(var_index)
                var_index += 1
            else:
                xor_clause.append(var_dict[var])

        sat.add_xor_clause(xor_clause, const)

    for i in range(len(aux_system)):

        l = list(aux_system[i][0])
        
        if f"a{i + 1}" not in var_dict:
                var_dict[f"a{i + 1}"] = var_index
                var_index += 1
            
        for var in l:
            if var not in var_dict:
                var_dict[var] = var_index
                var_index += 1

        if len(l) == 2:
            sat.add_clauses([[-var_dict[f'a{i + 1}'], var_dict[l[0]]], [-var_dict[f'a{i + 1}'], var_dict[l[1]]], [var_dict[f'a{i + 1}'], -var_dict[l[0]], -var_dict[l[1]]]])
        elif len(l) == 3:
            sat.add_clauses([[-var_dict[f'a{i + 1}'], var_dict[l[0]]], [-var_dict[f'a{i + 1}'], var_dict[l[1]]], [-var_dict[f'a{i + 1}'], var_dict[l[2]]], [var_dict[f'a{i + 1}'], -var_dict[l[0]], -var_dict[l[1]], -var_dict[l[2]]]])
        elif len(l) == 4:
            sat.add_clauses([[-var_dict[f'a{i + 1}'], var_dict[l[0]]], [-var_dict[f'a{i + 1}'], var_dict[l[1]]], [-var_dict[f'a{i + 1}'], var_dict[l[2]]], [-var_dict[f'a{i + 1}'], var_dict[l[3]]], [var_dict[f'a{i + 1}'], -var_dict[l[0]], -var_dict[l[1]], -var_dict[l[2]], -var_dict[l[3]] ]])
        elif len(l) == 5:
            sat.add_clauses([[-var_dict[f'a{i + 1}'], var_dict[l[0]]], [-var_dict[f'a{i + 1}'], var_dict[l[1]]], [-var_dict[f'a{i + 1}'], var_dict[l[2]]], [-var_dict[f'a{i + 1}'], var_dict[l[3]]], [var_dict[f'a{i + 1}'], var_dict[l[4]]], [var_dict[f'a{i + 1}'], -var_dict[l[0]], -var_dict[l[1]], -var_dict[l[2]], -var_dict[l[3]], -var_dict[l[4]] ]])
        elif len(l) == 6:
            sat.add_clauses([[-var_dict[f'a{i + 1}'], var_dict[l[0]]], [-var_dict[f'a{i + 1}'], var_dict[l[1]]], [-var_dict[f'a{i + 1}'], var_dict[l[2]]], [-var_dict[f'a{i + 1}'], var_dict[l[3]]], [var_dict[f'a{i + 1}'], var_dict[l[4]]], [var_dict[f'a{i + 1}'], var_dict[l[5]]], [var_dict[f'a{i + 1}'], -var_dict[l[0]], -var_dict[l[1]], -var_dict[l[2]], -var_dict[l[3]], -var_dict[l[4]], -var_dict[l[5]] ]])
        else:
            raise ValueError(f"Variabile ausiliaria a{i + 1} troppo grande!")

    result = sat.solve()[1]
    end = time.time()
    exec_time = end-start
    return (var_dict, result, exec_time)
    
def system_to_cnf(main_system, aux_system):
    var_dict = {}
    var_index = 1
    cnf_system = []
    num_rows = 0

    for equation, const in main_system:
        cnf_system.append(f"\nx{'' if const else '-'}")

        for var, in equation:
            if var not in var_dict:
                var_dict[var] = var_index
                cnf_system.append(f"{var_index} ")
                var_index += 1
            else:
                cnf_system.append(f"{var_dict[var]} ")

        cnf_system.append("0")
        num_rows += 1

    for i in range(len(aux_system)):

        l = list(aux_system[i][0])
        
        if f"a{i + 1}" not in var_dict:
                var_dict[f"a{i + 1}"] = var_index
                var_index += 1
            
        for var in l:
            if var not in var_dict:
                var_dict[var] = var_index
                var_index += 1

        if len(l) == 2:
            cnf_system.append(f"\n-{var_dict[f'a{i + 1}']} {var_dict[l[0]]} 0\n-{var_dict[f'a{i + 1}']} {var_dict[l[1]]} 0\n{var_dict[f'a{i + 1}']} -{var_dict[l[0]]} -{var_dict[l[1]]} 0")
            num_rows += 3
        elif len(l) == 3:
            cnf_system.append(f"\n-{var_dict[f'a{i + 1}']} {var_dict[l[0]]} 0\n-{var_dict[f'a{i + 1}']} {var_dict[l[1]]} 0\n-{var_dict[f'a{i + 1}']} {var_dict[l[2]]} 0\n{var_dict[f'a{i + 1}']} -{var_dict[l[0]]} -{var_dict[l[1]]} -{var_dict[l[2]]} 0")
            num_rows += 4
        else:
            raise ValueError(f"Variabile ausiliaria a{i + 1} troppo grande!")

    print(f"p cnf {var_index - 1} {num_rows}" + "".join(cnf_system))

    return var_dict