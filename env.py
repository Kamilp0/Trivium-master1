import sys
import random
from copy import deepcopy
from itertools import combinations, chain
from re import compile, match
from multiprocessing import Process
from file_handler import open_file, close_file
from process import start_and_wait, index_div, output
from bivium_class import BiviumSystem, equation_to_string, is_linear, is_contained

def create_aux_var(self, monomial_comb):

        aux_system = []

        for monomial_set in monomial_comb:

            occurrences = 0

            for equation, _ in z:
                if is_contained(equation, monomial_set):
                    occurrences += 1
                        
            monomial_val = (len(monomial_set) - 1) * occurrences

            if monomial_val > 6:
                aux_system.append((list(monomial_set), monomial_val))

        output.put(aux_system)
        
def fix_top(z, keystream, kx, ky, kw, n):

    for i in range(n):
        global_occ_top = system.variable_occurrences(z)
        global_occ_top = [(var, occ) for var, occ in sorted(global_occ_top.items(), key = lambda item: item[1], reverse = True)]

        if global_occ_top[0][1] == 0:
            break

        else:
            system.substitute_bits([global_occ_top[0][0]])
            system.fixed.append(global_occ_top[0][0])
            system.find_free_bits()

###OPTIMAL SEARCH
def random_bases(bases_to_try, z, keystream):

    good_bases = []
    len_goal = 177 - len(bases_to_try[0])

    for base in bases_to_try:
        z_copy = deepcopy(z)
        substitute_bits(z_copy, keystream, base)
        free_bit_test = find_free_bits(z_copy, keystream)

        if len(free_bit_test) == len_goal:
            good_bases.append(base)

    output.put(good_bases)

def find_lower_bases(base_list, z, keystream, begin, end):

    lower_bases = []
    len_goal = 178 - len(base_list[0])
     
    for base in base_list:
        for i in range(begin, end if end <= len(base) else len(base)):
            base_tested = base[:i] + base[i + 1:]
            z_copy = deepcopy(z)
            substitute_bits(z_copy, keystream, base_tested)
            free_bit_test = find_free_bits(z_copy, keystream)

            if len(free_bit_test) == len_goal:
                lower_bases.append(base_tested)

    output.put(lower_bases)

def find_alternative_bases(bases_to_modify, z, keystream):

    var_list = [(f"x{i:02}", True) for i in range(1, 94)] + [(f"y{i:02}", True) for i in range(1, 85)]
    alternative_bases = []

    for base in bases_to_modify:
        for i in range(len(base)):
            for var in var_list:

                if var not in base:
                    z_copy = deepcopy(z)
                    test_base = [*base]
                    test_base[i] = var
                    substitute_bits(z_copy, keystream, test_base)
                    free_bit_test = find_free_bits(z_copy, keystream)

                    if len(free_bit_test) == 118:
                        alternative_bases.append(test_base)

    output.put(alternative_bases)

###UNDO / REDO
def save_state(past_actions, next_actions, system):
    next_actions = []
    past_actions.append(system.copy())

def undo(past_actions, next_actions):
    if past_actions == []:
        print("Nessuna azione da ripristinare")
    else:
        global system
        next_actions.append(system)
        
        old_system = past_actions.pop()
        system = old_system.copy()

def redo(past_actions, next_actions):
    if next_actions == []:
        print("Nessuna azione da ripristinare")
    else:
        global system
        next_system = next_actions.pop()
        past_actions.append(next_system)

        system = next_system.copy()

 ##########
### MAIN ###
 ##########

if __name__ == "__main__":

    #inizializza il sistema (con soli '1')
    system = BiviumSystem()

    #variabili undo/redo
    past_actions = []
    next_actions = []

    #variabili
    lowered_base = []
    starting_base = ["x90", "y66", "y81", "x91", "y67", "y82", "y40", "y55", "y39", "y54", "x78", "y69", "x79", "y70", "x76", "y52", "x75","y51", "x61", "y37", "y64", "y79", "x93", "y84","y42", "y57", "x73", "y49", "x60", "y36", "x81", "y72", "y63", "y78", "x72", "y48", "y34", "x31", "y61", "y76","x65", "y46", "x70", "y83", "y68", "y53", "y27", "x35", "x62", "x77", "y80", "y65", "y71", "y56", "x47", "y62", "x86", "y11", "y25", "y35", "x84"]
    next_bases = []

    print("Per info sui comandi scrivi 'help'\n")

    for line in sys.stdin:
        
        line_words = line.rstrip().split()

        command = line_words[0]
        args = line_words[1:]

        if command == "new" and args == []: #genera casualmente un keystream

            save_state(past_actions, next_actions, system)

            system = BiviumSystem()
            print(f"KEYSTREAM: {''.join(map(lambda x: f'{int(x)}', system.keystream))}", end = '\n\n')

        elif command == "new_1" and args == []:

            save_state(past_actions, next_actions, system)

            system = BiviumSystem(all_one = True)
            print(f"KEYSTREAM: {''.join(map(lambda x: f'{int(x)}', system.keystream))}", end = '\n\n')

        elif command == "fix" and args != [] : #fissa dei bit e osserva le equazioni

            save_state(past_actions, next_actions, system)

            fixed_bits = []
            bad_arg = False

            for arg in args:

                single_r = match("^(k|x|y|w)(\d+)$", arg)
                range_r = match("^(x|y|w)(\d+)-(\d+)$", arg)
                print(single_r)

                if single_r and single_r.group(1) == "x" and 1 <= int(single_r.group(2)) <= 93:
                    fixed_bits.append(f"x{int(single_r.group(2))}")

                elif single_r and single_r.group(1) == "y" and 1 <= int(single_r.group(2)) <= 84:
                    fixed_bits.append(f"y{int(single_r.group(2))}")

                elif single_r and single_r.group(1) == "w" and 1 <= int(single_r.group(2)) <= 111:
                    fixed_bits.append(f"w{int(single_r.group(2))}")

                elif single_r and single_r.group(1) == "k" and 1 <= int(single_r.group(2)) <= 66:
                    for var,  in system.z_free_bits[int(single_r.group(2)) - 1][0][1:]:
                        fixed_bits.append(var)

                elif range_r and range_r.group(1) == "x" and 0 < int(range_r.group(2)) < int(range_r.group(3)) < 94:
                    for i in range(int(range_r.group(2)), int(range_r.group(3)) + 1):
                        fixed_bits.append(f"x{i}")

                elif range_r and range_r.group(1) == "y" and 0 < int(range_r.group(2)) < int(range_r.group(3)) < 85:
                    for i in range(int(range_r.group(2)), int(range_r.group(3)) + 1):
                        fixed_bits.append(f"y{i}")

                elif range_r and range_r.group(1) == "w" and 0 < int(range_r.group(2)) < int(range_r.group(3)) < 111:
                    for i in range(int(range_r.group(2)), int(range_r.group(3)) + 1):
                        fixed_bits.append(f"w{i}")

                else:
                    print(f"{arg}: Bad Arg")
                    bad_arg = True
                    break

            if not bad_arg:
                system.simplify(fixed_bits)
            
        elif command == "fix_top" and len(args) == 1 and args[0].isdigit():

            save_state(past_actions, next_actions, system)

            for i in range(int(args[0])):
                global_occ_top = system.variable_occurrences()
                global_occ_top = [(var, occ) for var, occ in sorted(global_occ_top.items(), key = lambda item: item[1], reverse = True)]

                if global_occ_top[0][1] == 0:
                    break

                else:
                    var = global_occ_top[0][0]

                    system.simplify([var])

                    starting_base.append((var, True))

        elif command == "lower" and args == []:
            
            if next_bases == []:
                bases_to_improve = [[(var, True) for var in starting_base]]
            else:
                bases_to_improve = next_bases
                next_bases = []

            go_on = True

            while go_on:
                answer = input("Vuoi ridurre le basi o trovarne di nuove? (r/a)")

                if answer == "r":
                    l = len(bases_to_improve[0]) 
                    processes = [Process(target = find_lower_bases, args = (bases_to_improve, z_with_free_bit, keystream, index_div(l, x, 8), index_div(l, x + 1, 8))) for x in range(8)]
                    
                else:
                    l = len(bases_to_improve) 
                    processes = [Process(target = find_alternative_bases, args = (bases_to_improve[index_div(l, x, 8):index_div(l, x + 1, 8)], z_with_free_bit, keystream)) for x in range(8)]
                
                next_bases.extend(start_and_wait(processes))

                if next_bases != []:
                    file = open_file(f"bases_{len(next_bases[0])}")
                    print(f"{len(next_bases)}\n")
                    for base in next_bases:
                        for var, _ in base:
                            print(var, end = ' ') 
                        print()
                    close_file(file)

                    answer = input(f"Hai ottenuto {len(next_bases)} nuove basi. Vuoi continuare? (s/n)")
                    bases_to_improve = next_bases
                    next_bases = []

                else:
                    answer = input("Non hai ottenuto nuove basi. Vuoi continuare? (s/n)")

                go_on = answer[0] == "s"

        #elif len(command) == 2 and command[0] == "best_base" and command[1].isdigit():


        elif command == "create" and len(args) == 2 and args[0].isdigit() and args[1].isdigit():
            global_occ_top = variable_occurrences(z_with_free_bit)
            top_var = [(var, True) for var, _ in sorted(global_occ_top.items(), key = lambda item: item[1], reverse = True)]
            n = int(args[0])
            k = int(args[1])

            bases_to_try = list(combinations(top_var[:n], k))
            l = len(bases_to_try)
            next_bases = []
            
            processes = [Process(target = random_bases, args = (bases_to_try[index_div(l, x, 7):index_div(l, x + 1, 7)], z_with_free_bit, keystream)) for x in range(7)]
            
            next_bases.extend(start_and_wait(processes))

            if next_bases != []:
                print(f"{len(next_bases)} basi trovate")

                file = open_file(f"bases_{len(next_bases[0]) - 1}")
                print(f"{len(next_bases)}\n")
                for base in next_bases:
                    for var, _ in base:
                        print(var, end = ' ') 
                    print()
                close_file(file)
            else:
                print("Nessuna base trovata...")

        elif command == "reduce" and len(args) == 1 and args[0].isdigit():
            
            long_equations = []

            for equation, const in z_with_free_bit:
                if count_var(equation) > 8:
                    long_equations.append((equation, const))

            monomial_occ = monomial_occurrences(long_equations)[:int(args[0])]

            most_freq_monomials = [monomial for monomial, _ in monomial_occ]
            monomial_comb = list(chain.from_iterable(combinations(most_freq_monomials, i) for i in range(2, 7)))
            l = len(monomial_comb)

            processes = [Process(target = create_aux_var, args = (long_equations, monomial_comb[index_div(l, x, 8):index_div(l, x + 1, 7)])) for x in range(8)]
            aux_system.extend(start_and_wait(processes))
            """
            aux_system_app = aux_system.copy()
            for aux_equation in aux_system_app:
                for check_equation in aux_system_app:
                    if aux_equation != check_equation and is_contained(check_equation, aux_equation):
                        aux_system.remove(aux_equation)
                        break
            """
            
            check = True

            while check:
                check = False
                for (aux1, val1), (aux2, val2) in combinations(aux_system, 2):
                    for equation, _ in long_equations:
                        if is_contained(equation, aux1) and is_contained(equation, aux2) and any(i in aux1 for i in aux2):
                            if val1 > val2:
                                aux_system.remove((aux2, val2))
                            else:
                                aux_system.remove((aux1, val1))
                            check = True
                            break
                    if check:
                        break

            aux_system = [aux_eq for aux_eq, _ in aux_system]

            for aux_equation in aux_system:
                for equation, _ in long_equations:
                    if is_contained(equation, aux_equation):
                        for monomial in aux_equation:
                            equation.remove(monomial)

                        equation.append({f"a{aux_index}"})
                aux_index += 1

        elif command == "aux_selection" and args == []:
            system.create_nonlinear_aux()    

        elif command == "add_aux" and args == []:

            add = compile("\s*\+\s*")
            mul = compile("\s*\*\s*")

            expr = input("Inserisci l'espressione da sostituire: ").strip()
            aux_expr = add.split(expr)

            for i in range(len(aux_expr)):
                aux_expr[i] = set(mul.split(aux_expr[i]))

            system.add_aux(aux_expr)

        elif command == "aux_simple" and args == []:
            system.create_simple_nonlinear_aux()

        elif command == "unknown_var" and args == []:
            var_list = [f"x{i:02}" for i in range(1, 94)] + [f"y{i:02}" for i in range(1, 85)]
            print(", ".join([var for var in var_list if var not in system.free and var not in system.fixed]))
            
        elif command == "fixed" and args == []:
            system.print_history()
        
        elif command == "free" and args == []:
            system.print_history(False)

        elif command == "find" and len(args) == 1:
            for i in range(66):
                if {args[0]} in system.z_free_bits[i][0]:
                    print(equation_to_string(system.z_free_bits[i], i), end = "\n\n")

        elif command == "rref" and len(args) == 3 and args[0].isdigit() and args[1].isdigit() and args[2].isdigit():
            save_state(past_actions, next_actions, system)
            system.reduced_echelon_form(int(args[0]) - 1, int(args[1]), int(args[2]))

        elif command == "solve" and args == []:
            system.sat_solve(system.incognite)

        elif command == "sfb" and args != []:
            system.substitute_free_bits(args)

        elif command[:5] == "print" and 0 <= len(args) <= 2:
            if len(args) == 1 and args[0] != "nofb" or len(args) == 2:
                file = open_file(args[0] if len(args) == 1 else args[1])

            nofb = args != [] and args[0] == "nofb"

            if command == "print":
                system.print(nofb)
            elif command == "print_smaller":
                system.print_smaller(nofb)
            elif command == "print_info":
                system.print_info(nofb)
            elif command == "print_sympy":
                system.print_sympy(nofb)
            elif command == "print_cnf":
                system.print_cnf(nofb)
            elif command == "print_sage":
                system.print_sage(nofb)
            elif command == "print_aux":
                system.print_aux()
            else:
                print("Comando di print inesistente.")

            if len(args) == 1 and args[0] != "nofb" or len(args) == 2:
                close_file(file)

        elif command == "undo" and args == []:
            undo(past_actions, next_actions)
            
        elif command == "redo" and args == []:
            redo(past_actions, next_actions)
            
        elif command == "help" and args == []:
            print("\n+new: genera il sistema di equazioni completo, generando dei bit casuali per i registri iniziali e il relativo keystream")
            print("\n+fix <var_list>: fissa le variabili passate in input nel sistema di equazioni corrente \nesempio 'fix x92 x83 y12'\n        'fix x9-34' (fissa le variabili da x9 a x34)")
            print("\n+fix_top <int>: fissa le <int> variabili pi?? frequenti nel sistema")
            print("\n+add_aux: genera una nuova variabile ausiliaria che corrisponde all'espressione passata in input")
            print("\n+aux_simple: genera le variabili ausiliarie con tutti i monomi con pi?? di una variabile")
            print("\n+fixed: stampa le variabili che hai fissato fin'ora")
            print("\n+free: stampa le variabili gratuite che hai ottenuto")
            print("\n+find <var>: stampa le equazioni contenenti quella variabile ('find x9')")
            print("\n+rref <begin> <end> <step>: applica le riduzioni di Gauss-Jordan al sottosistema scelto")
            print("\n+print <args>: stampa il sistema corrente ('print test' redireziona l'output sul file test.txt)")
            print("\n+print_smaller <args>: stampa le equazioni aventi 3 o meno variabili, nelle prime 66 ('print_easy test' redireziona l'output sul file test.txt)")
            print("\n+print_info <args>: stampa le prime 66 equazioni, segnando per ciascuna la frequenza globale e locale di ogni variabile ('print_occ test' redireziona l'output sul file test.txt)")
            print("\n+print_sympy <args>: stampa il sistema corrente in formato convertibile da sympy('print_sat test' redireziona l'output sul file test.txt)")
            print("\n+print_cnf <args>: stampa il sistema corrente in formato cnf")
            print("\n+print_aux: stampa il sistema che definisce le variabili ausiliarie")
            print("\n+solve: risolve il sistema corrente con SAT solver")
            print("\n\n-----COMANDI NUOVI-----\n")
            print("\n+calcola_keystream: ricava 250 bit di keystream a partire da chiave e IV, e crea un nuovo sistema")
            print("\n+incognite <args>: scegli i bit da trovare (inserisce nel sistema di equazioni le variabili note con il loro valore, ma non le inconite)")
            print("\n+solve_new: risolvi il sistema, stampa informazioni sulla performance")
            print("\n+exit: esci dalla shell interattiva\n")

        elif command == "calcola_keystream":
            system = BiviumSystem("dai")

        elif command == "incognite":
            system.incognite()
        
        elif command == "exit" and args == []:
            print("Session Closed.")
            break
        
        elif command == "variabili":
            kx = [f"x{n}" for n in range(1, 94)]
            ky = [f"y{n}" for n in range(1, 85)]
            kw = [f"w{n}" for n in range(1, 112)]
            print(kx, ky, kw)
            
        elif command == "test":
            variabili = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61', 'x62', 'x63', 'x64', 'x65', 'x66', 'x67', 'x68', 'x69', 'x70', 'x71', 'x72', 'x73', 'x74', 'x75', 'x76', 'x77', 'x78', 'x79', 'x80', 'x81', 'x82', 'x83', 'x84', 'x85', 'x86', 'x87', 'x88', 'x89', 'x90', 'x91', 'x92', 'x93', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'y10', 'y11', 'y12', 'y13', 'y14', 'y15', 'y16', 'y17', 'y18', 'y19', 'y20', 'y21', 'y22', 'y23', 'y24', 'y25', 'y26', 'y27', 'y28', 'y29', 'y30', 'y31', 'y32', 'y33', 'y34', 'y35', 'y36', 'y37', 'y38', 'y39', 'y40', 'y41', 'y42', 'y43', 'y44', 'y45', 'y46', 'y47', 'y48', 'y49', 'y50', 'y51', 'y52', 'y53', 'y54', 'y55', 'y56', 'y57', 'y58', 'y59', 'y60', 'y61', 'y62', 'y63', 'y64', 'y65', 'y66', 'y67', 'y68', 'y69', 'y70', 'y71', 'y72', 'y73', 'y74', 'y75', 'y76', 'y77', 'y78', 'y79', 'y80', 'y81', 'y82', 'y83', 'y84', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10', 'w11', 'w12', 'w13', 'w14', 'w15', 'w16', 'w17', 'w18', 'w19', 'w20', 'w21', 'w22', 'w23', 'w24', 'w25', 'w26', 'w27', 'w28', 'w29', 'w30', 'w31', 'w32', 'w33', 'w34', 'w35', 'w36', 'w37', 'w38', 'w39', 'w40', 'w41', 'w42', 'w43', 'w44', 'w45', 'w46', 'w47', 'w48', 'w49', 'w50', 'w51', 'w52', 'w53', 'w54', 'w55', 'w56', 'w57', 'w58', 'w59', 'w60', 'w61', 'w62', 'w63', 'w64', 'w65', 'w66', 'w67', 'w68', 'w69', 'w70', 'w71', 'w72', 'w73', 'w74', 'w75', 'w76', 'w77', 'w78', 'w79', 'w80', 'w81', 'w82', 'w83', 'w84', 'w85', 'w86', 'w87', 'w88', 'w89', 'w90', 'w91', 'w92', 'w93', 'w94', 'w95', 'w96', 'w97', 'w98', 'w99', 'w100', 'w101', 'w102', 'w103', 'w104', 'w105', 'w106', 'w107', 'w108', 'w109', 'w110', 'w111']
            incognite = ""
            mode = "testing"
            for i in range(200):
                incognite += variabili[i]
                incognite += " "
                for j in range(10):

                    key = hex(random.randint(75557863725914323419136, 1208925819614629174706175))
                    iv = hex(random.randint(75557863725914323419136, 1208925819614629174706175))

                    system = BiviumSystem(mode, key, iv, incognite)
                    print("Nuovo sistema creato.\nIncognite: " + incognite + " ")
                    system.create_simple_nonlinear_aux()
                    print("calcolo...")
                    system.sat_solve(system.incognite)
                    print("risolto!\n")

        else:
            print("Comando non riconosciuto")