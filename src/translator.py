dick_op= {
    'JMP' : 8,
    'JFE' : 9,
    'JFN' : 10,
    'JFB' : 11,
    'JFL' : 12,
    'LDR' : 1,
    'LDN' : 3,
    'STR' : 2,
    'STN' : 4,
    'OUT' : 5,
    'SUM' : 21,
    'SUB' : 22,
    'AND' : 23,
    'OR' : 24,
    'XOR' : 25,
    'SHL' : 27,
    'SHR' : 28,
    'NOT' : 26
    }

sr = "0123456789ABCDEF"
def to_hex(n):
    s = ""
    while n > 0:
        s = sr[n%16]+s
        n = n // 16
    return s

def open_file(inp_file):
    lines = []
    with open(inp_file) as file:
        for i in file:
            lines.append(i.strip())
    return lines

def write_file(code, file_name = "a.hex"):
    with open(file_name, "w") as file:
        file.writelines("\n".join(code))

def translate(lines):
    out = []
    for i in range(len(lines)):
        print(f"line {i} - {lines[i]}"); p_op_code = lines[i].split()[0]
        if dick_op.get(p_op_code) and i == 0:
            for j in range(5):
                out.append("0000")
        if dick_op.get(p_op_code):
            print(f"OPCODE {dick_op[p_op_code]}")
            cmd = "0"*(5-len(bin(dick_op[p_op_code])[2::]))+ bin(dick_op[p_op_code])[2::]
            registers = lines[i][5:].split('R')
            reg_bin = []
            for i in registers:
                reg_bin.append("0"*(3-len(bin(int(i.strip()))[2::])) + bin(int(i.strip()))[2::])
                print("0"*(3-len(bin(int(i.strip()))[2::])) + bin(int(i.strip()))[2::], end=' ')
                print()
            reg_bin.reverse()
            cmd = "0"*(16-len("".join(reg_bin)+cmd)) + "".join(reg_bin)+cmd
            print("cmd:", end=" ")
            print(cmd, "0"*(4-len(to_hex(int(cmd,2)))) + to_hex(int(cmd,2)))
            cmd = "0"*(4-len(to_hex(int(cmd,2)))) + to_hex(int(cmd,2))
            out.append(cmd)
        else:
            out.append(lines[i])
    return out
"""
inp_file = input("Введите имя файла: ")
code = open_file(inp_file)
out = translate(code)
print(out)
write_file(out)
"""       
