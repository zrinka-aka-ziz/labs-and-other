import os
import time
import math

ime_datoteke = 'LeksickiAnalizator.py'
folder_u_kojem_su_testovi = 'testovi'
ukupno = 16

broj_znamenki = int(math.log10(ukupno)) + 1
tocno = 0
netocno = []
for i in range(ukupno):
    start = time.time_ns()
    value = os.popen(f"python {ime_datoteke} < {folder_u_kojem_su_testovi}\\test{i + 1:0{broj_znamenki}d}/test.in > {folder_u_kojem_su_testovi}\\test{i + 1:0{broj_znamenki}d}/moj_rezultat.iz")
    end = time.time_ns()
    value.read()
    rezultat = os.popen(f"FC {folder_u_kojem_su_testovi}\\test{i + 1:0{broj_znamenki}d}\\test.out {folder_u_kojem_su_testovi}\\test{i + 1:0{broj_znamenki}d}\\moj_rezultat.iz").read()
    os.remove(f"{folder_u_kojem_su_testovi}\\test{i + 1:0{broj_znamenki}d}\\moj_rezultat.iz")
    if "no differences encountered" in rezultat:
        print(f"Test {i + 1:02d} OK; Time: {(end - start) / (10 ** 9):.06f} s")
        tocno += 1
    else:
        print(f"Test {i + 1:02d} FAIL; Time: {(end - start) / (10 ** 9):.06f} s")
        print(rezultat)
        netocno.append(i + 1)
print(f"\nTočno: {tocno}, netočno: {len(netocno)}, postotak: {(tocno / ukupno) * 100}%")
if netocno:
    print(f"Netočni: {netocno}")
