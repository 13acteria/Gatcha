import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import random
import datetime


HEIGHT = 360
WIDTH = 640
DARKGRAY = "#2f3841"
BLUE = "#6495ED"
PATH = r"C:\code\Tkinter\tkinfo_ori.json"


class TurnPageBtn:
    def __init__(self, frame, key:str, format:list=None):
        with open(PATH, 'r', encoding="utf-8") as f:
            contents = json.load(f)
        if format == None:
            format = [i for i in range(len(contents[key][0]))]
        
        self.frame = frame
        self.key = key
        self.format = format
        
        self.btn1 = tk.Button(frame, text="<")
        self.btn2 = tk.Button(frame, text=">")
        self.btn1.grid(row=10, column=0, sticky="w")
        self.btn2.grid(row=10, column=len(format)-1, sticky="e")
        self.btn1.config(command=lambda: self.btnhandler(-10))
        self.btn2.config(command=lambda: self.btnhandler(10))
        
        self.pageVar = tk.StringVar()
        lab = tk.Label(frame, textvariable=self.pageVar)
        lab.grid(row=10, column=1, columnspan=len(format)-2)
        
        self.frame.columnconfigure(tuple(range(len(format))), weight=1)
        self.update()
    
    def update(self):
        with open(PATH, 'r', encoding="utf-8") as f:
            contents = json.load(f)
        self.bound = len(contents[self.key])
        self.curr = -10
        self.btnhandler(10)
    
    def hidebtn(self):
        if not self.curr+10 < self.bound:
            self.btn2.grid_forget()
        else:
            self.btn2.grid(row=10, column=len(self.format)-1, sticky="e")
        if self.curr == 0:
            self.btn1.grid_forget()
        elif self.curr == 10:
            self.btn1.grid(row=10, column=0, sticky="w")
    
    def btnhandler(self, move):
        frameclear(self.frame, head=3)
        self.curr += move
        with open(PATH, 'r', encoding="utf-8") as f:
            contents = json.load(f)
        history_gen(self.frame, contents[self.key], self.format, head=self.curr)
        self.hidebtn()
        self.pageVar.set(f"Page {self.curr//10+1}")

# class RemoveBtn:
#     def __init__(self, , target):
#         self.target = target
#         self.age = age


def dashboard(*args):
    home.pack_forget()
    mission.pack_forget()
    match menu_var.get():
        case "Home":
            home.pack(fill="both", expand=True)
        case "Missions":
            mission.pack(fill="both", expand=True)

def calcupull(*args):
    with open(PATH, 'r', encoding="utf-8") as f:
        contents = json.load(f)
    global howmanypull
    howmanypull = min(contents["sum in puller"], int(coins.get()), 10)
    howmanypull = max(1, howmanypull)
    howmanypull_str.set(f'抽x{howmanypull}')

def history_gen(frame, items:list, format=None, head=0, tail=None):
    if format == None:
        format = [i for i in range(len(items[0]))]
    r = 0
    for item in items[head:tail]:
        c = 0
        for word in format:
            if type(word) == int:
                if word >= 0:
                    text = item[word]
                else:
                    btn = tk.Button(frame, bg="black", text="R", command=lambda:print(r))
                    btn.grid(row=r, column=c, sticky="ew")
                    continue
            else:
                text = word
            lab = tk.Label(frame, text=f"{text}")
            lab.grid(row=r, column=c, sticky="ew")
            c += 1
        r += 1
        if r == 10:
            break

def frameclear(frame, head=0, tail=None):
    for widget in frame.winfo_children()[head:tail]:
        widget.destroy()


def homeselector():
    puller.place_forget()
    add_rwd.place_forget()
    items_in_puller.place_forget()
    rwd_list.place_forget()
    pull_history.place_forget()
    match home_page.get():
        case "pull":
            puller.place(relx=0.5, rely=0.4, anchor="center")
        case "new":
            add_rwd.place(relx=0.5, rely=0.4, anchor="center")
        case "list":
            items_in_puller.place(relx=0.5, y=30, anchor="n", width=400)
        case "get":
            rwd_list.place(relx=0.5, y=30, anchor="n", width=400)
        case "history":
            pull_history.place(relx=0.5, y=30, anchor="n", width=500)

def pull_gen(times):
    with open(PATH, 'r', encoding="utf-8") as f:
        contents = json.load(f)
    msg = [[],[]]
    items = contents["items in puller"]
    
    for i in range(times):
        sum = contents["sum in puller"]
        if sum == 0:
            return msg
        
        r = random.randint(1, sum)
        contents["coins"] -= 1
        contents["sum in puller"] -= 1
        for i in range(len(items)):
            item = items[i]
            r -= (item[2]-item[1])
            if r > 0:
                continue
            
            item[1] += 1
            history = contents["history of puller"]
            history.insert(0, [item[0], item[1], item[2], str(datetime.date.today())])
            msg[0].append(f"{item[0]} {item[1]}/{item[2]}")
        
            if item[1] != item[2]:
                break
            
            items.pop(i)
            contents["history of rewards"].insert(0, [item[0], item[2], str(datetime.date.today())])
            msg[1].append(f"獲得 {item[0]}")
        
        with open(PATH, 'w', encoding="utf-8") as f:
            json.dump(contents, f, indent=4, ensure_ascii=False)
        coins.set(contents["coins"])
    
    return msg

def pullN(n):
    if n == 1:
        if coins.get() == "0":
            messagebox.showerror("", "抽乾了:(")
            return
        with open(PATH, 'r', encoding="utf-8") as f:
            contents = json.load(f)
        if contents["sum in puller"] == 0:
            messagebox.showerror("", "獎池空空如也")
            return
    ok = messagebox.askokcancel("確認視窗", f"確定要進行抽獎{n}次嗎")
    if not ok:
        return
    
    msg = pull_gen(n)
    msgstr = '\n'.join(msg[0])
    messagebox.showinfo("", msgstr)
    if len(msg[1]) != 0:
        msg[1].insert(0, "CONGRATULATION!!")
        msgstr = '\n'.join(msg[1])
        messagebox.showinfo("", msgstr)
    pullitems_page_btns.update()
    rewards_page_btns.update()
    pullhst_page_btns.update()

def addprize():
    name = rwd.get()
    num = int(need.get())
    if num == 0:
        messagebox.showerror("", "數量不能為0")
        return
    ok = messagebox.askokcancel("新增獎品", f"任務名稱: {name}\n需求數量: {num}")
    if not ok:
        return
    
    with open(PATH, 'r', encoding="utf-8") as f:
        contents = json.load(f)
    contents["items in puller"].append([f"{name}", 0, num])
    contents["sum in puller"] += num
    
    with open(PATH, 'w', encoding="utf-8") as f:
        json.dump(contents, f, indent=4, ensure_ascii=False)
    rwd.set('')
    need.set('')
    calcupull()
    pullitems_page_btns.update()


def missionselector():
    msn_history.place_forget()
    add_msn.place_forget()
    match msn_page.get():
        case "new":
            add_msn.place(relx=0.5, rely=0.4, anchor="center")
        case "history":
            msn_history.place(relx=0.5, y=30, anchor="n", width=400)

def getcoin():
    name = msn_name.get()
    if name == "":
        messagebox.showerror("", "任務名稱不能為空")
        return
    coin = int(reward.get())
    ok = messagebox.askokcancel("獲得代幣", f"任務名稱: {name}\n代幣數量: {coin}")
    if not ok:
        return
    
    with open(PATH, 'r', encoding="utf-8") as f:
        contents = json.load(f)
    contents["coins"] += coin
    history = contents["history of missions"]
    history.insert(0, [name, coin, str(datetime.date.today())])
    
    with open(PATH, 'w', encoding="utf-8") as f:
        json.dump(contents, f, indent=4, ensure_ascii=False)
    coins.set(contents["coins"])
    msn_name.set("")
    reward.set("")
    msn_page_btns.update()


# create window
root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}+600+200")
root.title("Happy Gacha")
root.iconbitmap(r"C:\code\Tkinter\img\recycle.ico")
root.config(bg="white")
root.maxsize(1920, 1080)


# create bar frame
nav = tk.Frame(root, bg="skyblue")
nav.pack_propagate(False)
nav.pack(fill="x")

# prepare variable and values of menu
menu_values = ["Home", "Missions"]
menu_var = tk.StringVar()
menu_var.set(menu_values[0])
menu_var.trace("w", dashboard)

# set the option menu for changing the page
menu = tk.OptionMenu(nav, menu_var, *menu_values)
menu.config(bg=BLUE, fg="white")
menu.grid(row=0, column=0)

# show how many coins do I have
img = Image.open(r"C:\code\Tkinter\img\recycle.png")
img = img.resize((22, 22))
tk_img = ImageTk.PhotoImage(img)
coins = tk.StringVar()
howmanypull = 0
howmanypull_str = tk.StringVar()
coins.trace('w', calcupull)
with open(PATH, 'r', encoding="utf-8") as f:
    contents = json.load(f)
coins.set(contents["coins"])
coins_lab = tk.Label(nav, textvariable=coins, font=("Arial", 15), image=tk_img, compound="left")
coins_lab.place(anchor="ne", relx=1, rely=0)


# home frame
home = tk.Frame(root, bg="red")
puller = tk.Frame(home, bg="orange")
add_rwd = tk.Frame(home, bg="orange")
items_in_puller = tk.Frame(home, bg="orange")
rwd_list = tk.Frame(home, bg="orange")
pull_history = tk.Frame(home, bg="orange")
# pull_history.propagate(False)

home_page = tk.StringVar()
home_btn1 = tk.Radiobutton(home, text='轉蛋',variable=home_page, value='pull', command=homeselector)
home_btn1.grid(row=0, column=0)
home_btn2 = tk.Radiobutton(home, text='新增獎品',variable=home_page, value='new', command=homeselector)
home_btn2.grid(row=0, column=1)
home_btn3 = tk.Radiobutton(home, text='獎池物品',variable=home_page, value='list', command=homeselector)
home_btn3.grid(row=0, column=2)
home_btn3 = tk.Radiobutton(home, text='已得獎品',variable=home_page, value='get', command=homeselector)
home_btn3.grid(row=0, column=3)
home_btn4 = tk.Radiobutton(home, text='抽獎紀錄',variable=home_page, value='history', command=homeselector)
home_btn4.grid(row=0, column=4)

home_btn1.select()
homeselector()

btn = tk.Button(puller, text="抽x1", command=lambda: pullN(1))
btn.grid(row=0, column=0, padx=10)
btn = tk.Button(puller, textvariable=howmanypull_str, command=lambda: pullN(howmanypull))
btn.grid(row=0, column=1, padx=10)
calcupull()

rwd_lab = tk.Label(add_rwd, text="獎品名稱:")
rwd_lab.grid(row=0, column=0)
need_lab = tk.Label(add_rwd, text="需求數量:")
need_lab.grid(row=1, column=0)

rwd = tk.StringVar()
rwd_entry = tk.Entry(add_rwd, textvariable=rwd)
rwd_entry.grid(row=0, column=1)
need = tk.StringVar()
need_entry = tk.Entry(add_rwd, textvariable=need)
need_entry.grid(row=1, column=1)

add_rwd_btn = tk.Button(add_rwd, text="新增獎品", command=addprize)
add_rwd_btn.grid(row=2, column=0, columnspan=2)

pullitems_page_btns = TurnPageBtn(items_in_puller, "items in puller", [0, 1, 2])
rewards_page_btns = TurnPageBtn(rwd_list, "history of rewards", [2, 0, 1, -1])
pullhst_page_btns = TurnPageBtn(pull_history, "history of puller", [3, 0, 1, '/', 2])


mission = tk.Frame(root, bg="red")
add_msn = tk.Frame(mission, bg="orange")
msn_history = tk.Frame(mission, bg="orange")

msn_page = tk.StringVar()
msn_btn1 = tk.Radiobutton(mission, text='獲得代幣',
    variable=msn_page, value='new', command=missionselector)
msn_btn1.grid(row=0, column=0)
msn_btn2 = tk.Radiobutton(mission, text='歷史紀錄',
    variable=msn_page, value='history', command=missionselector)
msn_btn2.grid(row=0, column=1)

msn_btn1.select()
missionselector()

msn_label = tk.Label(add_msn, text="任務名稱:")
msn_label.grid(row=0, column=0)
reward_label = tk.Label(add_msn, text="代幣數量:")
reward_label.grid(row=1, column=0)

msn_name = tk.StringVar()
msn_entry = tk.Entry(add_msn, textvariable=msn_name)
msn_entry.grid(row=0, column=1)
reward = tk.StringVar()
reward_entry = tk.Entry(add_msn, textvariable=reward)
reward_entry.grid(row=1, column=1)

add_msn_btn = tk.Button(add_msn, text="確定送出", command=getcoin)
add_msn_btn.grid(row=2, column=0, columnspan=2)

msn_page_btns = TurnPageBtn(msn_history, "history of missions", [2, 0, 1])


dashboard()

root.mainloop()