from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pandas as pd
import ET0Calculator as eto

# frame setting
root = Tk()

root.title("기준증발산량 계산 프로그램")
root.geometry("438x111")
root.resizable(True, True)

# global variable
selection_list = ["날짜", "최고기온", "최저기온", "상대습도", "평균풍속", "일조시간", "일조량"]
key_order_time = ["날짜", "최고기온", "최저기온", "상대습도", "평균풍속", "일조시간"]
key_order_amount = ["날짜", "최고기온", "최저기온", "상대습도", "평균풍속", "일조시간"]

# command
def run():
    SOLAR = 0
    Metstation = filename.get()
    Metstation = Metstation.split('/')
    Metstation = Metstation[-1]
    Metstation = Metstation[3:6]
    all_value = get_all_value()

    if all_value.find("선택하세요.") == -1: 
        if "일조시간" in all_value and "일조량" in all_value: solar_warning()
        if all_value.find("일조시간") != -1: SOLAR = 1
        elif all_value.find("일조량") != -1: SOLAR = 2

    else: select_warning()

    df = rearrange_csv(SOLAR)
    # file_parse(df)
    eto.fileET_calculation(Metstation, SOLAR)
    root.destroy()

def get_hedaer():
    path = filename.get()
    df = pd.read_csv(path, encoding="cp949")

    header = list(df)

    return header

def open_csv():
    path = askopenfilename()
    filename.set(path)

    header = get_hedaer()
    
    data_label_col1.config(text=header[0])
    data_label_col2.config(text=header[1])
    data_label_col3.config(text=header[2])
    data_label_col4.config(text=header[3])
    data_label_col5.config(text=header[4])
    data_label_col6.config(text=header[5])

def make_new_header():
    new_header = []
    new_header.append(box_1.get())
    new_header.append(box_2.get())
    new_header.append(box_3.get())
    new_header.append(box_4.get())
    new_header.append(box_5.get())
    new_header.append(box_6.get())

    return new_header

def rearrange_csv(SOLAR):
    path = filename.get()
    df = pd.read_csv(path, encoding = 'cp949')

    header = get_hedaer()
    new_header = make_new_header()

    df.rename(columns={header[0]:new_header[0], header[1]:new_header[1],
                        header[2]:new_header[2], header[3]:new_header[3],
                        header[4]:new_header[4], header[5]:new_header[5]}, inplace=True) 

    if SOLAR == 1:
        df = df[[key_order_time[0], key_order_time[1], key_order_time[2], 
                key_order_time[3], key_order_time[4], key_order_time[5]]]

    elif SOLAR == 2:
        df = df[[key_order_amount[0], key_order_amount[1], key_order_amount[2], 
                key_order_amount[3], key_order_amount[4], key_order_amount[5]]]

    df.to_csv("MET090.csv", header=True, index=False, encoding="cp949")


def reset():
    box_1.set("선택하세요.")
    box_2.set("선택하세요.")
    box_3.set("선택하세요.")
    box_4.set("선택하세요.")
    box_5.set("선택하세요.")
    box_6.set("선택하세요.")

def get_all_value():
    all_value = box_1.get() + box_2.get() + box_3.get() + box_4.get() + box_5.get() + box_6.get()

    return all_value

def output(output):
    pass

# Exception
def metstation_warning():
    msgbox.showwarning("경고", "\"metstation_2018.dat\" file에 해당 코드가 없습니다.")

def select_warning():
    msgbox.showwarning("경고", "데이터를 모두 다 선택해주세요.")

def solar_warning():
    msgbox.showwarning("경고", "일조시간과 일조량 중 하나만 골라주세요.")




# layout component
box_1 = ttk.Combobox(root, width=10, height=4, values=selection_list, state="readonly")
box_1.set("선택하세요.")
box_2 = ttk.Combobox(root, width=10, height=4, values=selection_list, state="readonly")
box_2.set("선택하세요.")
box_3 = ttk.Combobox(root, width=10, height=4, values=selection_list, state="readonly")
box_3.set("선택하세요.")
box_4 = ttk.Combobox(root, width=10, height=4, values=selection_list, state="readonly")
box_4.set("선택하세요.")
box_5 = ttk.Combobox(root, width=10, height=4, values=selection_list, state="readonly")
box_5.set("선택하세요.")
box_6 = ttk.Combobox(root, width=10, height=4, values=selection_list, state="readonly")
box_6.set("선택하세요.")

browse_btn = Button(root, text = 'Browse', command=open_csv)

filename = StringVar()
filename_display = Entry(root, textvariable=filename, width=30, state="disabled")

frame_col1 = Frame(root, relief="solid", bd=1)
frame_col2 = Frame(root, relief="solid", bd=1)
frame_col3 = Frame(root, relief="solid", bd=1)
frame_col4 = Frame(root, relief="solid", bd=1)
frame_col5 = Frame(root, relief="solid", bd=1)
frame_col6 = Frame(root, relief="solid", bd=1)

data_label_col1 = Label(frame_col1, text="1열")
data_label_col2 = Label(frame_col2, text="2열")
data_label_col3 = Label(frame_col3, text="3열")
data_label_col4 = Label(frame_col4, text="4열")
data_label_col5 = Label(frame_col5, text="5열")
data_label_col6 = Label(frame_col6, text="6열")


reset_btn = Button(root, text = 'RESET', command=reset)
progress_display = Text(root, height=10, state="disabled")
check_btn = Button(root, text="실행", command=run)


# grid deployment
browse_btn.grid(row=0, column=0, sticky=N+E+W+S, padx=3, pady=3)

filename_display.grid(row=0, column=1, columnspan=10, sticky=N+E+W+S, padx=1, pady=3)

data_label_col1.pack()
data_label_col2.pack()
data_label_col3.pack()
data_label_col4.pack()
data_label_col5.pack()
data_label_col6.pack()

frame_col1.grid(row=1, column=1, sticky=N+E+W+S, padx=1, pady=1)
frame_col2.grid(row=1, column=3, sticky=N+E+W+S, padx=1, pady=1)
frame_col3.grid(row=1, column=5, sticky=N+E+W+S, padx=1, pady=1)
frame_col4.grid(row=2, column=1, sticky=N+E+W+S, padx=1, pady=1)
frame_col5.grid(row=2, column=3, sticky=N+E+W+S, padx=1, pady=1)
frame_col6.grid(row=2, column=5, sticky=N+E+W+S, padx=1, pady=1)

box_1.grid(row=1, column=2, sticky=N+E+W+S, padx=3, pady=1)
box_2.grid(row=1, column=4, sticky=N+E+W+S, padx=3, pady=1)
box_3.grid(row=1, column=6, sticky=N+E+W+S, padx=3, pady=1)
box_4.grid(row=2, column=2, sticky=N+E+W+S, padx=3, pady=1)
box_5.grid(row=2, column=4, sticky=N+E+W+S, padx=3, pady=1)
box_6.grid(row=2, column=6, sticky=N+E+W+S, padx=3, pady=1)

reset_btn.grid(row=1, column=0, rowspan=2, sticky=N+E+W+S, padx=3, pady=1)
# progress_display.grid(row=3, column=0, columnspan=7, sticky=N+E+W+S, padx=1, pady=3)
check_btn.grid(row=3, column=6, sticky=N+E+W+S, padx=3, pady=1)

root.mainloop()