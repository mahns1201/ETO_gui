from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pandas as pd

root = Tk()

# frame setting
root.title("기준증발산량 계산 프로그램")
root.geometry("700x300")
root.resizable(False, False)

# command
def warning():
    msgbox.showwarning("경고", "\"metstation_2018.dat\" file에 해당 코드가 없습니다.")

def get_value():
    value = box_1.get()
    
    return value

def get_csv():
    path = askopenfilename()
    df = pd.read_csv(path, encoding = 'cp949')

    return df

# layout component
selection_list = ["최고기온", "최저기온", "상대습도", "평균풍속", "일조시간", "일조량"]
box_1 = ttk.Combobox(root, height=4, values=selection_list, state="readonly")
box_1.set("항목을 선택하세요.")
box_2 = ttk.Combobox(root, height=4, values=selection_list, state="readonly")
box_2.set("항목을 선택하세요.")
box_3 = ttk.Combobox(root, height=4, values=selection_list, state="readonly")
box_3.set("항목을 선택하세요.")
box_4 = ttk.Combobox(root, height=4, values=selection_list, state="readonly")
box_4.set("항목을 선택하세요.")
box_5 = ttk.Combobox(root, height=4, values=selection_list, state="readonly")
box_5.set("항목을 선택하세요.")

browse_btn = Button(root, text = 'Browse', command=get_csv)
frame_col1 = Frame(root, relief="solid", bd=1)
frame_col2 = Frame(root, relief="solid", bd=1)
frame_col3 = Frame(root, relief="solid", bd=1)
frame_col4 = Frame(root, relief="solid", bd=1)
frame_col5 = Frame(root, relief="solid", bd=1)
frame_col6 = Frame(root, relief="solid", bd=1)

data_label_col1 = Label(frame_col1, text="1열: 날짜데이터")
data_label_col2 = Label(frame_col2, text="2열")
data_label_col3 = Label(frame_col3, text="3열")
data_label_col4 = Label(frame_col4, text="4열")
data_label_col5 = Label(frame_col5, text="5열")
data_label_col6 = Label(frame_col6, text="6열")

# ==== grid deployment ====
browse_btn.pack()
data_label_col1.pack()
data_label_col2.pack()
data_label_col3.pack()
data_label_col4.pack()
data_label_col5.pack()
data_label_col6.pack()
frame_col1.pack()
frame_col2.pack()
frame_col3.pack()
frame_col4.pack()
frame_col5.pack()
frame_col6.pack()
box_1.pack()
box_2.pack()
box_3.pack()
box_4.pack()
box_5.pack()


# box_1.grid(row=1, column=0)
# browse_btn.grid(row=0, column=0, sticky=N+E+W+S, padx=3, pady=3)
# data_label.grid(row=3, colu)

root.mainloop()

'''
code example

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