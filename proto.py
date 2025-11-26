from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
import subprocess
import json
import queue
import threading
import time


def DAP_Read(pipe, queue):
    while(True):
        line = pipe.readline()
        print(line.split(" ")[-1].strip())
        queue.put(pipe.read(int(line.split(" ")[-1].strip())))

class DebugBackend:
    def __init__(self):
        self.debugger = subprocess.Popen(["gdb", "-i=dap"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, universal_newlines = True)
        self.stdout = queue.Queue()
        self.reader = threading.Thread(target=DAP_Read, args=(self.debugger.stdout, self.stdout))
        self.reader.start()
        self.sequence = 1
        time.sleep(1)
        while(True):
            try: 
                print(self.stdout.get_nowait())
            except:
                break
    

    def select_program(self, executable):
        data = json.dumps({"seq": self.sequence, "type":"request", "command":f"target exec {executable}"})
        self.sequence += 1
        header = f"Content-Length: {len(data)}\r\n\r\n"
        full_data = "".join([header, data])
        print(f"Writing: {full_data}")
        self.debugger.stdin.write(full_data)
        self.debugger.stdin.flush()
        time.sleep(1)
        while(True):
            try: 
                print(self.stdout.get_nowait())
            except:
                break
        

class DebugFrontend:
    def __init__(self):
        self.backend = DebugBackend()
        self.executable = None
        self.source = None

        self.root = Tk()
        frame = ttk.Frame(self.root, padding = 10)
        frame.grid()

        source_frame = ttk.Frame(self.root, padding = 10)
        source_frame.grid(row = 0, column = 0)
        button_frame = ttk.Frame(self.root, padding = 10)
        button_frame.grid(row = 0, column = 1)
        stdout_frame = ttk.Frame(self.root, padding = 10)
        stdout_frame.grid(row = 1, column = 1)
        locals_frame = ttk.Frame(self.root, padding = 10)
        locals_frame.grid(row = 1, column = 1)
        
        ttk.Button(button_frame, text = "Load EXE", command = self.load_exe).grid(row = 0, column = 0)
        ttk.Button(button_frame, text = "Load Source", command = self.load_source).grid(row = 1, column = 0)
        ttk.Button(button_frame, text = "Run", command = self.run).grid(row = 2, column = 0)
        ttk.Button(button_frame, text = "Set breakpoint", command = self.bp).grid(row = 3, column = 0)
        self.source_window = ttk.Treeview(source_frame)
        self.source_window.grid(row = 0, column = 0)
        self.root.mainloop()

    def bp(self):
        pass

    def run(self):
        if self.executable == None:
            print("Trying to run without an executable")

    def load_exe(self):
        self.executable = filedialog.askopenfilename()
        self.backend.select_program(self.executable)

    def load_source(self):
        self.source = filedialog.askopenfilename()
        self.show_source()

    def show_source(self):
        with open(self.source) as f:
            for line in f:
                self.source_window.insert("", "end", text = line)

if __name__ == "__main__":
    DebugFrontend()
