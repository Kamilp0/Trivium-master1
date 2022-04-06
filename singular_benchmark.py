import re
from bivium_class import BiviumSystem
from file_handler import open_file, close_file

monomial_ordering = input("Inserire l'ordinamento per monomi (lp, rp, dp, Dp): ")
alg = input("Scegliere l'algoritmo: ")
var_list = input("Scegliere le variabili da fissare: ").rstrip().split()

start_code = f"""ring b = 2, (x01, x02, x03, x04, x05, x06, x07, x08, x09, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83, x84, x85, x86, x87, x88, x89, x90, x91, x92, x93, y01, y02, y03, y04, y05, y06, y07, y08, y09, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31, y32, y33, y34, y35, y36, y37, y38, y39, y40, y41, y42, y43, y44, y45, y46, y47, y48, y49, y50, y51, y52, y53, y54, y55, y56, y57, y58, y59, y60, y61, y62, y63, y64, y65, y66, y67, y68, y69, y70, y71, y72, y73, y74, y75, y76, y77, y78, y79, y80, y81, y82, y83, y84), {monomial_ordering};
ideal I = """

end_code = f""", x01^2 + x01, x02^2 + x02, x03^2 + x03, x04^2 + x04, x05^2 + x05, x06^2 + x06, x07^2 + x07, x08^2 + x08, x09^2 + x09, x10^2 + x10, x11^2 + x11, x12^2 + x12, x13^2 + x13, x14^2 + x14, x15^2 + x15, x16^2 + x16, x17^2 + x17, x18^2 + x18, x19^2 + x19, x20^2 + x20, x21^2 + x21, x22^2 + x22, x23^2 + x23, x24^2 + x24, x25^2 + x25, x26^2 + x26, x27^2 + x27, x28^2 + x28, x29^2 + x29, x30^2 + x30, x31^2 + x31, x32^2 + x32, x33^2 + x33, x34^2 + x34, x35^2 + x35, x36^2 + x36, x37^2 + x37, x38^2 + x38, x39^2 + x39, x40^2 + x40, x41^2 + x41, x42^2 + x42, x43^2 + x43, x44^2 + x44, x45^2 + x45, x46^2 + x46, x47^2 + x47, x48^2 + x48, x49^2 + x49, x50^2 + x50, x51^2 + x51, x52^2 + x52, x53^2 + x53, x54^2 + x54, x55^2 + x55, x56^2 + x56, x57^2 + x57, x58^2 + x58, x59^2 + x59, x60^2 + x60, x61^2 + x61, x62^2 + x62, x63^2 + x63, x64^2 + x64, x65^2 + x65, x66^2 + x66, x67^2 + x67, x68^2 + x68, x69^2 + x69, x70^2 + x70, x71^2 + x71, x72^2 + x72, x73^2 + x73, x74^2 + x74, x75^2 + x75, x76^2 + x76, x77^2 + x77, x78^2 + x78, x79^2 + x79, x80^2 + x80, x81^2 + x81, x82^2 + x82, x83^2 + x83, x84^2 + x84, x85^2 + x85, x86^2 + x86, x87^2 + x87, x88^2 + x88, x89^2 + x89, x90^2 + x90, x91^2 + x91, x92^2 + x92, x93^2 + x93, y01^2 + y01, y02^2 + y02, y03^2 + y03, y04^2 + y04, y05^2 + y05, y06^2 + y06, y07^2 + y07, y08^2 + y08, y09^2 + y09, y10^2 + y10, y11^2 + y11, y12^2 + y12, y13^2 + y13, y14^2 + y14, y15^2 + y15, y16^2 + y16, y17^2 + y17, y18^2 + y18, y19^2 + y19, y20^2 + y20, y21^2 + y21, y22^2 + y22, y23^2 + y23, y24^2 + y24, y25^2 + y25, y26^2 + y26, y27^2 + y27, y28^2 + y28, y29^2 + y29, y30^2 + y30, y31^2 + y31, y32^2 + y32, y33^2 + y33, y34^2 + y34, y35^2 + y35, y36^2 + y36, y37^2 + y37, y38^2 + y38, y39^2 + y39, y40^2 + y40, y41^2 + y41, y42^2 + y42, y43^2 + y43, y44^2 + y44, y45^2 + y45, y46^2 + y46, y47^2 + y47, y48^2 + y48, y49^2 + y49, y50^2 + y50, y51^2 + y51, y52^2 + y52, y53^2 + y53, y54^2 + y54, y55^2 + y55, y56^2 + y56, y57^2 + y57, y58^2 + y58, y59^2 + y59, y60^2 + y60, y61^2 + y61, y62^2 + y62, y63^2 + y63, y64^2 + y64, y65^2 + y65, y66^2 + y66, y67^2 + y67, y68^2 + y68, y69^2 + y69, y70^2 + y70, y71^2 + y71, y72^2 + y72, y73^2 + y73, y74^2 + y74, y75^2 + y75, y76^2 + y76, y77^2 + y77, y78^2 + y78, y79^2 + y79, y80^2 + y80, y81^2 + y81, y82^2 + y82, y83^2 + y83, y84^2 + y84;
ideal G = groebner(I, "{alg}");

exit;
"""

rref = input("Vuoi eseguire la riduzione di Gauss-Jordan? ").split()

for i in range(1, 101):

    system = BiviumSystem()

    if rref[0] == "s":
        system.reduced_echelon_form(begin = int(rref[1]), end = int(rref[2]), step = int(rref[3]), fb = False)

    z = system.z
    first_ideal = ""

    for k in range(len(z)):
        if z[k][0] != []:
            first_ideal += f"{' + '.join([' * '.join(x) for x in z[k][0]])}"
            if system.keystream[k] ^ z[k][1]:
                first_ideal += " + 1,"
            else:
                first_ideal += ","

    f = open_file(f"singular_test/slimgb_benchmark/{i}")
    
    var_ideal = []

    for var in var_list:
        single_r = re.match("^(x|y)(\d+)$", var)

        if single_r and single_r.group(1) == "x" and 1 <= int(single_r.group(2)) <= 93:
            var_ideal.append(f"x{single_r.group(2)}{' + 1' if system.kx[int(single_r.group(2)) - 1] else ''}")

        elif single_r and single_r.group(1) == "y" and 1 <= int(single_r.group(2)) <= 84:
            var_ideal.append(f"y{single_r.group(2)}{' + 1' if system.ky[int(single_r.group(2)) - 1] else ''}")

        else:
            raise Exception("boh")

    print(f"{start_code}{first_ideal}{','.join(var_ideal)}{end_code}")

    close_file(f)