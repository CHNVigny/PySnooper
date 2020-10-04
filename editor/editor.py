import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pysnooper
import json
import os
import sys
current_dir = os.getcwd()    # obtain work dir
sys.path.append(current_dir) # add work dir to sys path
import mysocket
import threading
import json
import queue
import time

path = r"C:\Users\94519\Desktop\checkpoint.txt"

class MyThreading(threading.Thread):
    def __init__(self, socket, queue, server = True):###这里应该加一个参数name
        """
        server: True == 是服务器
        send: True == 是发送线程
        """
        threading.Thread.__init__(self)
        self.socket = socket
        self.server = server
        self.queue = queue
#        self.socket.accept()


    def run(self):
        #线程内要做的事，线程都是接收数据的线程。
        while 1:
            dict_json = self.recv_func()
            # if str:
            #     print(str)
            dict_s = json.loads(dict_json)
            self.queue.put(dict_s)
            #print(type(dict_s))


    def send_func(self, str):
        pass

    def recv_func(self):
        return self.socket.recv()



class Menubar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 14)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File", accelerator="Ctrl+N",
                                  command=parent.new_file)

        file_dropdown.add_command(label="Open File", accelerator="Ctrl+O",
                                  command=parent.open_file)

        file_dropdown.add_command(label="Save", accelerator="Ctrl+S",
                                  command=parent.save)

        file_dropdown.add_command(label="Save As", accelerator="Ctrl+Shift+S",
                                  command=parent.save_as)

        file_dropdown.add_separator()

        file_dropdown.add_command(label="Exit",
                                  command=parent.master.destroy)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes",
                                   command=self.show_release_notes)

        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                   command=self.show_about_messagebox)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

    def show_about_messagebox(self):
        box_title = "About PyText"
        box_message = "一个简单的基于tkinter开发的文本编辑器。"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "python tkinter 文本编辑器 1.0版本 by 风花雪月！"
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 14)

        self.status = tk.StringVar()
        self.status.set("PyText - 0.1 Gutenberg")

        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                         bg="lightgrey", anchor="sw", font=font_specs)

        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            #self.status.set("你的文件已保存！")
            self.status.set("Saved！")
        else:
            #self.status.set("PyText - 0.1 Gutenberg")
            self.status.set("PyText - 0.1")


class PyText:

    def __init__(self, master, socket: mysocket = None, server: bool = True):
        master.title('Untitled - PyText')
        master.geometry("800x600")
        font_specs = ("ubuntu", 16)
        self.master = master
        self.filename = None
        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.bind_shortcuts()
        self.config_dict = {
            "show_about_messagebox": "self.show_about_messagebox",
            "show_release_notes": "self.show_release_notes",
            "set_windows_title": "self.set_windows_title",
            "new_file": "self.new_file",
            "open_file": "self.open_file",
            "save": "self._call_save",
            "save_as": "self.save_as"
        }
        #######checkpoint#####
        self.checkpoint_id = 0#记录检查点的编号。
        self._run_trace = {}#记录程序的运行路径。
        self._synced_checkpoint = []#记录已经同步的检查点
        self.server = server
        self.socket = socket
        #######socket#########
        self.socket = socket
        self.server = server#是否是server，是的话有一个self.socket.accept(),否的话有一个self.socket.connect()
        #设计的功能是客户端用来被同步，服务端是给用户操作的。默认是服务端server。
        #paper里写的是服务端用来被同步，客户端用来给用户操作。
        self.queue_listen = queue.Queue()#这一条是监听队列
        self.queue_send = queue.Queue()#这一条是发送队列
        self.threading = MyThreading(self.socket, self.queue_listen)#多线程用于监听所以给它监听队列
        ###########读写文件####################
        #self.f =  open(path,"w",encoding="utf-8")


##########################socket######################################
    def server_or_client(self):
        if self.server:
            self.socket.accept()
            self.threading.start()
            while 1:
                if self.queue_send.empty():
                    continue
                else:
                    self.socket.send(json.dumps(self.queue_send.get()))
        else:
            self.socket.connect()##ClientSocket在初始化的时候已经给出了host和port。
            self.threading.start()
            while 1:
                if self.queue_send.empty():
                    continue
                else:
                    self.socket.send(json.dumps(self.queue_send.get()))#{"1": "ok"/"1": "fail"}


##########################操作检查点###################################
    @pysnooper.snoop()
    def add_checkpoint_to_run_trace(self, checkpoint: dict):#checkpoint是一个字典。{"id":1, "function":"function", "parameters": []}
        self._run_trace[str(checkpoint["id"])] = checkpoint

    @pysnooper.snoop()
    def add_synced_checkpoint(self, id: int):
        if int(id) not in self._synced_checkpoint:
            self._synced_checkpoint.append(int(id))

    @pysnooper.snoop()
    def modify_run_trace(self, checkpoint: dict):#比较checkpoint加同步程序状态加记录同步过的检查点加修改trace
        if checkpoint != self._run_trace[str(checkpoint["id"])]:
            if self.sync(checkpoint):#同步
                self.add_synced_checkpoint(checkpoint["id"])#记录同步过了的检查点
            self._run_trace[str(checkpoint["id"])] = checkpoint
            return 1
        else:
            return 0#表示无需修改。

    @pysnooper.snoop()
    def sync(self, checkpoint: dict):#利用checkpoint进行程序同步（暂时只同步save）
        if checkpoint["function"] == "save":
            self.active_call_function(checkpoint["function"], *checkpoint["textarea_content"])
            self._synced_checkpoint.append(checkpoint["id"])
            return 1
        elif checkpoint["function"] == "open_file":
            self.active_call_function(checkpoint["function"])
            return 1
        return 0

####################################################################################
    @pysnooper.snoop()
    def show_about_messagebox(self):
        self.menubar.show_about_messagebox()

    @pysnooper.snoop()
    def show_release_notes(self):
        self.menubar.show_release_notes()

    @pysnooper.snoop()
    def set_windows_title(self, name=None):
        if name:
            self.master.title(name + "- PyText")
        else:
            self.master.title('Untitled - PyText')

    @pysnooper.snoop()
    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_windows_title()

    @pysnooper.snoop()
    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("Python Files", "*.py"),
                       ("JavaScript Files", "*.js"),
                       ("Html Files", "*.html"),
                       ("CSS Documents", "*.css"),
                       ("Markdown Documents", "*.md")

                       ]
        )

        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.set_windows_title(self.filename)

    @pysnooper.snoop()
    def save(self, *args):

        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                self.statusbar.update_status(True)

            except Exception as e:
                print(e)
        else:
            self.save_as()

        #创建检查点
        checkpoint = {}
        checkpoint["id"] = self.checkpoint_id
        self.checkpoint_id += 1
        checkpoint["function"] = "save"
        checkpoint["textarea_content"] = [textarea_content]
        self.add_checkpoint_to_run_trace(checkpoint)
        checkpoint_str = json.dumps(checkpoint)
        #self.f.write(checkpoint_str + "\n")




    @pysnooper.snoop()
    def _call_save(self, textarea_content):
        if self.filename:
            try:
                save_textarea_content = textarea_content
                self.textarea.delete(1.0, tk.END)
                with open(self.filename, "w") as f:
                    self.textarea.insert(1.0, save_textarea_content)
                    f.write(save_textarea_content)
                self.statusbar.update_status(True)

            except Exception as e:
                print(e)
        #这个路径上有bug。要解决考虑将另一边的filename传过来，以写的方式打开。
        else:
            self.save_as()

    @pysnooper.snoop()
    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                           ("Text Files", "*.txt"),
                           ("Python Files", "*.py"),
                           ("JavaScript Files", "*.js"),
                           ("Html Files", "*.html"),
                           ("CSS Documents", "*.css"),
                           ("Markdown Documents", "*.md")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)

            self.filename = new_file
            self.set_windows_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    @pysnooper.snoop()
    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.update_status)

    @pysnooper.snoop()
    def active_call_function(self, function, *args, **kws):
        be_called_function_name = self.config_dict[function]
        if be_called_function_name:
        # 就直接调用。如果有其他参数，一样地传就好了
        # 另外也可以是"be_called_function_name"是"be_called_function"，然后eval(be_called_function_name)()
            eval(be_called_function_name)(*args, **kws)
        else:
            print("no function")


@pysnooper.snoop()
def wrapper(function, *args, **kws):
    eval(function)(*args, **kws)

@pysnooper.snoop()
def editortest():
    master = tk.Tk()
    pt = PyText(master)
    #pt.active_call_function("show_about_messagebox")
    master.mainloop()
    #master.quit()

@pysnooper.snoop()



def nomainlooptest():
    master = tk.Tk()
    #LABEL = Label(ROOT, text="Hello, world!")
    #LABEL.pack()
    pt = PyText(master)
    LOOP_ACTIVE = True
    f = open(path,'r')
    opened = 0
    done = 0
    while LOOP_ACTIVE:
        master.update()

        if not opened:
            pt.active_call_function("open_file")
            opened = 1

        while not done:
            checkpoint_str = f.readline()
            if checkpoint_str != '':
                checkpoint = json.loads(checkpoint_str)
                pt.sync(checkpoint)
                time.sleep(1)
            else:
                done = 1
            #if USER_INPUT == "exit":
                #master.quit()
                #LOOP_ACTIVE = False
            #elif USER_INPUT == "save":
            #LABEL = Label(ROOT, text=USER_INPUT)
            #LABEL.pack()

                #pt.active_call_function("save", *["abdcefg\n"])
                #continue
            #else:
                #continue

"""
from Tkinter import *

ROOT = Tk()

def ask_for_userinput():
    user_input = raw_input("Give me your command! Just type \"exit\" to close: ")
    if user_input == "exit":
        ROOT.quit()
    else:
        label = Label(ROOT, text=user_input)
        label.pack()
        ROOT.after(0, ask_for_userinput)

LABEL = Label(ROOT, text="Hello, world!")
LABEL.pack()
ROOT.after(0, ask_for_userinput)
ROOT.mainloop()
"""
@pysnooper.snoop()
def ask_for_userinput(ROOT, pt):
    #ROOT = tk.Tk()
    #pt =  pt = PyText(ROOT)
    user_input = input("Give me your command! Just type \"exit\" to close: ")
    if user_input == "exit":
        ROOT.quit()
    elif user_input == "save":
        #label = Label(ROOT, text=user_input)
        #label.pack()
        pt.active_call_function("open_file")
        pt.active_call_function("save", *["abdcefg\n"])
        ROOT.after(0, ask_for_userinput, *[ROOT, pt])

@pysnooper.snoop()
def aftertest():
    master = tk.Tk()
    pt = PyText(master)
    master.after(0, ask_for_userinput, *[master, pt])
    master.mainloop()

@pysnooper.snoop()
def threadtest():
    import threading
    pass










if __name__ == '__main__':
    # master = tk.Tk()
    # pt = PyText(master)
    # master.mainloop()
    #editortest()
    nomainlooptest()
    #aftertest()