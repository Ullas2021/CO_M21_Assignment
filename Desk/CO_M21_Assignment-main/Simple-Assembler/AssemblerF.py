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
D = ["00100", "00101"]
E = ["01111", "10000", "10001", "10010"]
import sys


def main():
    a = []
    instructionTracker = []
    bin = ""
    vcount = 1
    lcount = 0
    lno = 0
    mc = []
    label = []
    lorder = {}
    v = []
    vstore = []
    vorder = []
    f = 0
    fc = 0
    user_in = [line.rstrip() for line in sys.stdin.readlines()]
    for k in user_in:

        if "hlt" in k.split():
            f = 1
            fc+=1
       
    if f == 0:
        print("hlt statement missing!")
    elif "hlt" not in user_in[-1].split():
        print("hlt has not been used as last instruction")
    else:
        for k in user_in:
            
            if fc>1:
                print("multiple hlt statements encountered!")
                break
            a = k.split()

            if len(a) == 0:
                lno += 1
                continue
            if a[0] == "hlt":
                mc.append("1001100000000000")
                break
            if a[0] != "hlt":
                pos = 0
                xyz = False
                if a[0][-1] == ":":
                    lorder[a[0][0:-1]] = "0" * (8 - len(decimalToBinary(lcount))) + decimalToBinary(lcount)
                    del a[0]

                if a[0] in code and a[0] != "mov":
                    for i in range(len(a)):
                        if a[i] == "FLAGS":
                            print("Illegal use of FLAGS register!: line no.", lno)
                            xyz=True
                            break
                if xyz:
                    break
                if a[0] == "mov" and a[1] == "FLAGS":
                    print("Illegal use of FLAGS register!: line no.", lno)
                    break

                if a[0] not in code and a[0] != "var":
                    print("Instruction undefined! : line no.", lno)
                    break

                instructionTracker.append(a[0])

                for i in range(len(instructionTracker)):

                    if instructionTracker[i] in code:
                        pos = i

                        if "var" in instructionTracker[pos::]:
                            print("code structure violation: line no.", lno)
                            xyz=True
                            break
                if xyz:
                    break

                if (a[0] in typeE and len(a) != 2):
                    print("Parameters Missing!! : line no.", lno)
                    break

                if (a[0] in typeB and len(a) != 3):
                    print("Parameters Missing!! : line no.", lno)
                    break

                if (a[0] in typeD and len(a) != 3):
                    print("Parameters Missing!! : line no.", lno)
                    break

                if (a[0] in typeC and len(a) != 3):
                    print("Parameters Missing!! : line no.", lno)
                    break

                if (a[0] in typeA and len(a) != 4):
                    print("Parameters Missing!! : line no.", lno)
                    break

                if a[0] == "var":
                    v.append(a[1])
                    lno+=1

                if (a[0] in typeA):

                    if a[1] not in reg or a[2] not in reg or a[3] not in reg:
                        print("illegal reg reference!: line no.", lno)
                        break

                    bin = code[a[0]] + "00" + reg[a[1]] + reg[a[2]] + reg[a[3]]
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if (a[0] in typeE):
                    if a[1] in v:
                        print("label cannot be initialised with name similar to var , error in line no.", lno)
                        break

                    label.append(a[1])

                if (a[0] in typeB and a[2] not in reg):
                    if a[1] not in reg:
                        print("Illegal register reference!! : line no.", lno)
                        break
                    if not (0 <= int(a[2][1:]) <= 255 and a[2][0] == "$"):
                        print("Invalid integer input !! : line no.", lno)
                        break

                if a[0] == "jmp" or a[0] == "jlt" or a[0] == "jgt" or a[0] == "je":

                    bin = code[a[0]] + "000"
                    vstore.append(a[1])
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                    if a[0] == "jmp":
                        z = 0
                    # jump to address
                    if a[0] == "jlt":
                        z = 0
                    # jump to address
                    if a[0] == "jgt":
                        z = 0
                    # jump to address
                    if a[0] == "je":
                        z = 0
                    # jump to address
                    else:
                        z = 0
                if ((a[0] == "mov" and a[2][0] == "$") or a[0] == "rs" or a[0] == "ls") and (a[2] not in reg):
                    binaryvalue = decimalToBinary(int(a[2][1:]))

                    imm = "0" * (8 - len(str(binaryvalue))) + str(binaryvalue)

                    bin = code[a[0]] + reg[a[1]] + imm
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if (a[0] == "mov" and a[2] in reg):

                    if a[1] not in reg or a[2] not in reg:
                        print("illegal register reference!:  line no.", lno, "\r")
                        break

                    bin = typeC["mov"] + "00000" + reg[a[1]] + reg[a[2]]
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if (a[0] in typeC) and (a[0] != "mov"):

                    if a[1] not in reg or a[2] not in reg:
                        print("illegal register reference! : line no.", lno, "\r")
                        break

                    bin = code[a[0]] + "00000" + reg[a[1]] + reg[a[2]]
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if a[0] in typeD:

                    if a[1] not in reg or a[2] not in v:
                        print("Illegal Load Instruction! :line no.", lno)
                        break

                    bin = code[a[0]] + reg[a[1]]
                    vstore.append(a[2])
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if a[0] in typeF:
                    mc.append("1001100000000000")
                    break

                lno = lno + 1

        comp = []
        binval = ""
        it = {}
        m = 0
        lomp = []
        for i in range(len(label)):
            if label[i] in lorder:
                lomp.append(lorder[label[i]])
            else:
                print("memory address is undefined!")
                break

        for i in range(len(v)):
            binval = decimalToBinary(vcount)
            comp.append(binval)
            comp[i] = "0" * (8 - len(comp[i])) + comp[i]
            vcount += 1

        for i in v:
            it[i] = m
            m += 1

        for i in vstore:

            if i in it:
                vorder.append(it[i])

        for i in range(len(mc)):

            if len(mc[i]) == 8 and mc[i][:5] in D:

                mc[i] = mc[i] + comp[vorder[0]]
                del vorder[0]

            elif len(mc[i]) == 8 and mc[i][:5] in E:

                mc[i] = mc[i] + lomp[0]
                lomp.pop(0)

        for i in mc:
            print(i)


def decimalToBinary(n):
    return bin(n).replace("0b", "")


if __name__ == "__main__": main()
