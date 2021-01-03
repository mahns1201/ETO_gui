from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pandas as pd

root = Tk()

# ==== frame setting ====
root.title("기준증발산량 계산 프로그램")
root.geometry("700x300")
root.resizable(False, False)

# ==== command ====
def warning():
    msgbox.showwarning("경고", "\"metstation_2018.dat\" file에 해당 코드가 없습니다.")

def get_value():
    value = box.get()
    
    return value

def get_csv():
    path = askopenfilename()
    df = pd.read_csv(path, encoding = 'cp949')

    return df

# ==== layout component ====
selection_list = ["최고기온", "최저기온", "상대습도", "평균풍속", "일조시간", "일조량"]
box = ttk.Combobox(root, height=4, values=selection_list, state="readonly")
box.set("항목을 선택하세요.")
# box.grid(row=1, column=0)
box.pack()




browse_btn = Button(root, text = 'Browse', command=get_csv)
browse_btn.pack()
# browse_btn.grid(row=0, column=0, sticky=N+E+W+S, padx=3, pady=3)

frame = Frame(root, relief="solid", bd=1)
frame.pack()
data_label = Label(frame, text="1열: 날짜데이터")
# data_label.grid(row=3, colu)
data_label.pack()

# ==== grid deployment ====

root.mainloop()

'''
btn1 = Button(root, padx=20, pady=20, text = "button 1")
btn1.pack()

btn2 = Button(root, width=20, height=20, text = "button 2")
btn2.pack()

btn3 = Button(root, fg="red", bg="yellow", text="button3")
btn3.pack()

photo = PhotoImage(file="./image/check.png")

btn4 = Button(root, image=photo, command=btncmd)
btn4.pack()
'''