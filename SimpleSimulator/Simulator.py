def decimalToBinary(n):
    return bin(n).replace("0b", "")


def binaryToDecimal(n):
    return int(n, 2)


code = {"add": "00000", "sub": "00001", "mov": "00010", "ld": "00100", "st": "00101", "mul": "00110",
        "div": "00111", "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101",
        "cmp": "01110",
        "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011"}
typeE = {"jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010"}
typeB = {"rs": "01000", "ls": "01001", "mov": "00010"}
typeA = {"add": "00000", "sub": "00001", "xor": "01010", "or": "01011", "and": "01100", "mul": "00110"}
typeC = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}
typeD = {"ld": "00100", "st": "00101"}
typeF = {"hlt": "10011"}
reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
       "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
mem_addr = {}
D = ["00100", "00101"]
E = ["01111", "10000", "10001", "10010"]
rf = {"000": "0000000000000000", "001": "0000000000000000", "010": "0000000000000000", "011": "0000000000000000",
      "100": "0000000000000000", "101": "0000000000000000", "110": "0000000000000000", "111": "0000000000000000"}

fg = ["00000", "00001", "00010", "00100", "00101", "00110", "00111", "01000", "01001", "01010", "01011", "01100",
      "01101", "01110", "01111", "10011", "00011"]


def leng(str):
    a = ''
    i = 0
    for i in range(len(str)):
        if str[i] == "1":
            a = (i) * '0' + (16 - i) * '1'
            break
    return a


def resetflags():
    rf['111'] = "0000000000000000"


import sys


def main():
    instruction = [line.rstrip() for line in sys.stdin.readlines()]
    while len(instruction) < 256:
        instruction.append("0000000000000000")
        continue
    skip = []
    a = 0
    c = 0
    halt = 0
    main.apoint = []
    main.cpoint = []
    while halt != 1:
        abc = False
        i = instruction[a]
        if instruction[a] == "1001100000000000":
            halt = 1
        if a in skip:
            fill = decimalToBinary(a)
            pc = (8 - len(fill)) * "0" + fill
            print(pc, end=' ')
            for k in rf:
                print(rf[k], end=' ')
            print()
            main.apoint.append(a)
            main.cpoint.append(c)
            a += 1
            c += 1

            continue
        if i[0:5] in fg and i[13:16] != "111":
            resetflags()

        if i[0:5] == "00011":
            rf[i[10:13]] = rf[i[13:16]]
        elif i[0:5] == "01101":
            fill = decimalToBinary(binaryToDecimal('1111111111111111') - binaryToDecimal(rf[i[13:16]]))
            fill = (16 - len(fill)) * "0" + fill
            rf[i[10:13]] = fill
        elif i[0:5] == "01110":
            if rf[i[10:13]] == rf[i[13:16]]:
                rf['111'] = '0000000000000001'
            elif binaryToDecimal(rf[i[10:13]]) < binaryToDecimal(rf[i[13:16]]):
                rf['111'] = '0000000000000100'
            else:
                rf['111'] = '0000000000000010'
        elif i[0:5] == "00111":
            fill = decimalToBinary(binaryToDecimal(rf[i[10:13]]) // binaryToDecimal(rf[i[13:16]]))
            fill = (16 - len(fill)) * "0" + fill
            rf['000'] = fill
            fill = decimalToBinary(binaryToDecimal(rf[i[10:13]]) % binaryToDecimal(rf[i[13:16]]))
            fill = (16 - len(fill)) * "0" + fill
            rf['001'] = fill
        elif i[0:5] == "00100":
            rf[i[5:8]] = mem_addr[i[8:16]]
        elif i[0:5] == "00101":
            fill = binaryToDecimal(i[8:16])
            mem_addr[i[8:16]] = rf[i[5:8]]
            instruction[fill] = rf[i[5:8]]

        elif i[0:5] == "01111":  # Daksh
            fill = decimalToBinary(a)
            pc = (8 - len(fill)) * "0" + fill
            print(pc, end=' ')
            for k in rf:
                print(rf[k], end=' ')
            print()
            temp = binaryToDecimal(i[8:])
            main.apoint.append(a)
            main.cpoint.append(c)
            a = temp
            c += 1

            continue

        elif i[0:5] == "10000":
            if rf["111"] == "0000000000000100":
                resetflags()
                fill = decimalToBinary(a)
                pc = (8 - len(fill)) * "0" + fill
                print(pc, end=' ')
                for k in rf:
                    print(rf[k], end=' ')
                print()
                temp = binaryToDecimal(i[8:])
                main.apoint.append(a)
                main.cpoint.append(c)
                a = temp
                c += 1

                continue
            else:
                resetflags()
                fill = decimalToBinary(a)
                pc = (8 - len(fill)) * "0" + fill
                print(pc, end=' ')
                for k in rf:
                    print(rf[k], end=' ')
                print()
                temp = binaryToDecimal(i[8:])
                skip.append(temp)
                main.apoint.append(a)
                main.cpoint.append(c)
                a += 1
                c += 1

                continue

        elif i[0:5] == "10001":
            if rf["111"] == "0000000000000010":
                resetflags()
                fill = decimalToBinary(a)
                pc = (8 - len(fill)) * "0" + fill
                print(pc, end=' ')
                for k in rf:
                    print(rf[k], end=' ')
                print()
                temp = binaryToDecimal(i[8:])
                main.apoint.append(a)
                main.cpoint.append(c)
                a = temp
                c += 1

                continue
            else:
                resetflags()
                fill = decimalToBinary(a)
                pc = (8 - len(fill)) * "0" + fill
                print(pc, end=' ')
                for k in rf:
                    print(rf[k], end=' ')
                print()
                temp = binaryToDecimal(i[8:])
                skip.append(temp)
                main.apoint.append(a)
                main.cpoint.append(c)
                a += 1
                c += 1

                continue

        elif i[0:5] == "10010":
            if rf["111"] == "0000000000000001":
                resetflags()
                fill = decimalToBinary(a)
                pc = (8 - len(fill)) * "0" + fill
                print(pc, end=' ')
                for k in rf:
                    print(rf[k], end=' ')
                print()
                temp = binaryToDecimal(i[8:])
                main.apoint.append(a)
                main.cpoint.append(c)
                a = temp
                c += 1

                continue
            else:
                resetflags()
                fill = decimalToBinary(a)
                pc = (8 - len(fill)) * "0" + fill
                print(pc, end=' ')
                for k in rf:
                    print(rf[k], end=' ')
                print()
                temp = binaryToDecimal(i[8:])
                skip.append(temp)
                main.apoint.append(a)
                main.cpoint.append(c)
                a += 1
                c += 1

                continue
        elif i[0:5] == "00010":
            rf[i[5:8]] = "0" * 8 + i[8:]

        elif i[0:5] == "01000":
            temp1 = binaryToDecimal(i[8:])
            temp2 = binaryToDecimal(rf[i[5:8]])
            fi = temp2 >> temp1
            fi = decimalToBinary(fi)

            rf[i[5:8]] = "0" * (16 - len(fi)) + fi

        elif i[0:5] == "01001":
            temp1 = binaryToDecimal(i[8:])
            temp2 = binaryToDecimal(rf[i[5:8]])
            fi = temp2 << temp1
            fi = decimalToBinary(fi)

            rf[i[5:8]] = "0" * (16 - len(fi)) + fi

        elif i[0:5] == '00000':  # add                                      #Saurav
            rf["111"] = "0000000000000000"
            if (binaryToDecimal(rf[i[10:13]]) + binaryToDecimal(rf[i[13:16]])) > 255:
                rf["111"] = "0000000000001000"
                abc = True
                rf[i[7:10]] = "0000000000000000"
            else:
                help = decimalToBinary(binaryToDecimal(rf[i[10:13]]) + binaryToDecimal(rf[i[13:16]]))
                help = (16 - len(help)) * "0" + help
                rf[i[7:10]] = help
        elif i[0:5] == '00001':  # sub
            rf["111"] = "0000000000000000"
            if (binaryToDecimal(rf[i[10:13]]) - binaryToDecimal(rf[i[13:16]])) < 0:
                rf["111"] = "0000000000001000"
                abc = True
                rf[i[7:10]] = "0000000000000000"
            else:
                help = decimalToBinary(binaryToDecimal(rf[i[10:13]]) - binaryToDecimal(rf[i[13:16]]))
                help = (16 - len(help)) * "0" + help
                rf[i[7:10]] = help
        elif i[0:5] == '00110':  # mul
            rf["111"] = "0000000000000000"
            if (binaryToDecimal(rf[i[10:13]]) * binaryToDecimal(rf[i[13:16]])) > 255:
                rf["111"] = "0000000000001000"
                abc = True
                rf[i[7:10]] = "0000000000000000"
            else:
                help = decimalToBinary(binaryToDecimal(rf[i[10:13]]) * binaryToDecimal(rf[i[13:16]]))
                help = (16 - len(help)) * "0" + help
                rf[i[7:10]] = help
        elif i[0:5] == '01010':  # XOR
            help = decimalToBinary(binaryToDecimal(rf[i[10:13]]) ^ binaryToDecimal(rf[i[13:16]]))
            help = (16 - len(help)) * "0" + help
            rf[i[7:10]] = help
        elif i[0:5] == '01011':  # OR
            help = decimalToBinary(binaryToDecimal(rf[i[10:13]]) | binaryToDecimal(rf[i[13:16]]))
            help = (16 - len(help)) * "0" + help
            rf[i[7:10]] = help
        elif i[0:5] == '01100':
            help = decimalToBinary(binaryToDecimal(rf[i[10:13]]) & binaryToDecimal(rf[i[13:16]]))
            help = (16 - len(help)) * "0" + help
            rf[i[7:10]] = help
        if i[0:5] != "01110" and abc == False:
            resetflags()
        fill = decimalToBinary(a)
        pc = (8 - len(fill)) * "0" + fill
        print(pc, end=' ')
        for k in rf:
            print(rf[k], end=' ')
        print()
        main.apoint.append(a)
        main.cpoint.append(c)
        c += 1
        a += 1

    for m in instruction:
        print(m)


if __name__ == "__main__": main()

import matplotlib.pyplot as plt

plt.scatter(main.cpoint, main.apoint)
plt.title('Memory Access v/s Cycle')
plt.xlabel('Cycle')
plt.ylabel('Memory')
plt.show()
