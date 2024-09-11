from tkinter import *
from tkinter import ttk
import threading
import time
from tkinter import StringVar, Label, Tk
from translator import translate, open_file
#from core import CPU


def xor(a, b):
    return (a and not b) or (not a and b)

sr = "0123456789ABCDEF"
def to_hex(n):
    s = ""
    while n > 0:
        s = sr[n%16]+s
        n = n // 16
    return s

class CPU:
    out_reg = 0
    flags = [
        0, # equal
        0, # bg
        0  # overflow
        ]
    memory = []
    registers = [
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        ]
    
    def init(self):
        self.stopped = 1
        self.counter = 5
        self.registers = [
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        "0000",
        ]
        self.flags = [
        0, # equal
        0, # bg
        0  # overflow
        ]
        self.int_vect = [
        0 # overflow
        ]
        self.intr = [
        0 # overflow
        ]
        self.int_return = 0
        self.int_type = 0
        sext.delete("1.0", END)
    
    def tick(self):
        if 1 in self.intr and int_vect[self.intr.index(1)] != 0 and  self.int_return == 0:
            self.int_type = self.intr.index(1)
            self.int_return = self.counter
            self.counter = self.int_vect[self.intr.index(1)]
        self.execc()
        self.counter += 1
        if self.flags[2]:
            self.intr[0] = 1
        #print(self.counter)
        #print(self.memory)
        
    def execc(self):
        cmd = '0'*(16-len(bin(int(self.memory[self.counter],16))[2:])) + bin(int(self.memory[self.counter],16))[2:]
        #print(cmd)
        instr = int(cmd[-5:],2)
        #print(cmd[-5:], instr)
        regs = [
            cmd[-8:-5],
            cmd[-11:-8],
            cmd[-14:-11]
            ]
        if instr > 20 and instr < 29:
            self.flags[0] = int(self.registers[int(regs[1],2)],16) == int(self.registers[int(regs[2],2)],16)
            self.flags[1] = int(self.registers[int(regs[1],2)],16) > int(self.registers[int(regs[2],2)],16)
        match instr:
            case 0:
                print("NOP")
            case 3:
                self.registers[int(regs[0],2)] = self.memory[self.counter+1]
                self.counter += 1
            case 4:
                self.memory[self.counter+1] = self.registers[int(regs[0],2)]
                self.counter += 1
            case 1:
                self.registers[int(regs[1],2)] = self.memory[int(self.registers[int(regs[0],2)],16)]
            case 2:
                self.memory[int(self.registers[int(regs[0],2)],16)] = self.registers[int(regs[1],2)]
            case 21:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) + int(self.registers[int(regs[2],2)],16))
            case 22:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) - int(self.registers[int(regs[2],2)],16))
            case 23:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) & int(self.registers[int(regs[2],2)],16))
            case 24:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) | int(self.registers[int(regs[2],2)],16))
            case 25:
                self.registers[int(regs[0],2)] = to_hex(xor(int(self.registers[int(regs[1],2)],16),int(self.registers[int(regs[2],2)],16)))
            case 26:
                self.registers[int(regs[0],2)] = to_hex(~int(self.registers[int(regs[1],2)],16))
            case 27:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) << int(self.registers[int(regs[2],2)],16))
            case 28:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) >> int(self.registers[int(regs[2],2)],16))
            case 24:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) | int(self.registers[int(regs[2],2)],16))
            case 25:
                self.registers[int(regs[0],2)] = to_hex(xor(int(self.registers[int(regs[1],2)],16),int(self.registers[int(regs[2],2)],16)))
            case 26:
                self.registers[int(regs[0],2)] = to_hex(~int(self.registers[int(regs[1],2)],16))
            case 27:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) << int(self.registers[int(regs[2],2)],16))
            case 28:
                self.registers[int(regs[0],2)] = to_hex(int(self.registers[int(regs[1],2)],16) >> int(self.registers[int(regs[2],2)],16))
            case 8:
                self.counter = int(self.registers[int(regs[0],2)],16)
            case 9:
                if self.flags[0]: self.counter = int(self.registers[int(regs[0],2)],16) - 1
            case 10:
                if not self.flags[0]: self.counter = int(self.registers[int(regs[0],2)],16) - 1
            case 11:
                if self.flags[1]: self.counter = int(self.registers[int(regs[0],2)],16) - 1
            case 12:
                if not self.flags[1]: self.counter = int(self.registers[int(regs[0],2)],16) - 1
            case 5:
                print(cmd)
                print(cmd[:2])
                if cmd[:2] == "00":
                    sext.insert(END, self.registers[int(regs[0],2)][2:])
                elif cmd[:2] == "01":
                    sext.insert(END, self.registers[int(regs[0],2)][:2])
                elif cmd[:2] == "10":
                    print("nothing")
                    #sext.insert(END, self.registers[int(regs[0],2)][:2])    
            case 7:
                if self.int_return == 0:
                    self.stopped = 1
                else:
                    self.counter = self.int_return - 1
                    self.int_return = 0
                    self.intr[self.int_type] = 0
        #print(regs)

CPU_inst = CPU()

def update_text(text_field, new_text):
    text_field.delete("1.0", END)  # Очистка текстового поля
    text_field.insert(END, new_text)  # Вставка нового текста

def worker_thread(memory_field, registers_field, reglable):
    # Симуляция длительной операции
    while True:
        if not CPU_inst.stopped:
            if CPU_inst.counter >= len(CPU_inst.memory):
                CPU_inst.stopped = 1
                vext.delete("1.0", END)
                vext.insert(END, "STOP")
                continue
            CPU.tick(CPU_inst)
            # Безопасное обновление текстового поля (необходим механизм блокировки)
            memory_field.after(0, lambda: update_text(memory_field, "\n".join(CPU_inst.memory)))
            #registers_field.after(0, lambda: update_text(registers_field, "\n".join(CPU_inst.registers) + f"\n{CPU_inst.flags}"))
            reglable.set(f"IP - {to_hex(CPU_inst.counter)}\n" + "\n".join(CPU_inst.registers) + f"\nFLAGS\n{CPU_inst.flags}")
            
            time.sleep(0.25)  # Пауза для симуляции
        else:
            time.sleep(1) 


def trs():
    text_content = text.get('1.0','end')
    print(text_content)
    out = translate(text_content.strip().split("\n"))
    print(out)
    hext.delete('1.0', 'end')
    hext.insert('1.0', "\n".join(out))

def reset_sim():
    CPU.init(CPU_inst)
    rtext.set(f"IP - {to_hex(CPU_inst.counter)}\n" + "\n".join(CPU_inst.registers) + f"\nFLAGS\n{CPU_inst.flags}")
    print("RESETED")

def start():
    if not CPU_inst.stopped:
        CPU_inst.stopped = 1
        vext.delete("1.0", END)
        vext.insert(END, "STOP")
    else:
        CPU_inst.stopped = 0
        CPU_inst.memory = hext.get('1.0','end').strip().split("\n")
        vext.delete("1.0", END)
        vext.insert(END, "START")


#Само окно
root = Tk()
root.geometry('800x600')
root.resizable(False, False)
root.title("EMU ETHER-16")


rtext = StringVar()
rtext.set("ОЖыДАНИЕ ПРОГРАММЫ")
rlable = Label(root, textvariable=rtext)
rlable.grid(column=3, row=1)

#Разбивка окна на таблицу 5x5
cr_num = 16
for c in range(cr_num): root.columnconfigure(index=c, weight=1) #Столбцы
for r in range(cr_num): root.rowconfigure(index=r, weight=1) #Строчки

#Кнопки в верхнем ряду (скорее всего цикл придётся вручную расписать)
for c in range(4):
        btn = ttk.Button(
            root,
            text="translate",
            command=trs
            )
        btn.grid(row=0, column=c, ipadx=2, ipady=2, padx=2, pady=2)
btn = ttk.Button(
            root,
            text="RESET",
            command=reset_sim
            )
btn.grid(row=0, column=4, ipadx=2, ipady=2, padx=2, pady=2)

#Кнопка справа снизу
button = ttk.Button(
            root,
            text="Start/Stop",
            command=start
            )
button.grid(row=2, column=3, ipadx=2, ipady=2, padx=2, pady=2)

#Сами поля ввода
text = Text(root, height=22, width=20)
hext = Text(root, height=22, width=20)
sext = Text(root, height=22, width=15)
vext = Text(root, height=1, width=15)


vext.delete("1.0", END)
vext.insert(END, "STOP")

#Расположение полей ввода
text.grid(column=0, row=1)
hext.grid(column=1, row=1)
sext.grid(column=2, row=1)
vext.grid(column=2, row=2)

CPU.init(CPU_inst)
# Запуск потока
thread = threading.Thread(target=worker_thread, args=(hext,sext, rtext))
thread.start()

root.mainloop()




