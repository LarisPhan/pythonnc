# Import
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import math 


if __name__ == '__main__':
    win = tk.Tk()  
    win.title("Bài tập số 1 - Python NC")  # Thêm tiêu đề
    win.geometry("400x300")  # Kích thước
    win.resizable(True, True)

    # Hàm căn giữa màn hình
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Tạo Menu Bar
    menu_bar = tk.Menu(win)
    win.config(menu=menu_bar)

    # Khi nhấn nút Exit
    def on_exit():
        answer = messagebox.askyesnocancel('Xác nhận thoát', 'Bạn có chắc chắn muốn thoát không?')
        if answer:  # Nếu người dùng chọn Yes
            win.quit()
            win.destroy()
            exit()
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=on_exit) 
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Hàm Message Box khi ấn About
    def msgBox():
        messagebox.showinfo('Python Message Info Box', 'Python GUI hiện đang trong giai đoạn phát triển\nRất mong sự thông cảm từ bạn')
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=msgBox)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    # Tạo tabControl
    tabControl = ttk.Notebook(win)
    tabControl.pack(expand=1, fill="both")

    # Thêm Tab:
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text=' Trang chủ ')
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text=' pheptoanCoBan ')
    tab3 = ttk.Frame(tabControl)
    tabControl.add(tab3, text=' giaiPtBac2 ') 


    # ----#----#----#----#----#----#----#----#
    ''' Tab 1 Contents '''
    ### Frame 1
    mighty_1 = ttk.LabelFrame(tab1, text='Welcome!!!')
    mighty_1.pack(padx=8, pady=4, fill='both', expand=True)

    # Thay đổi chức năng khi ấn nút 
    def click_me(): 
        action.configure(text='Hello ' + name.get() + ' ' + number_chosen.get())

    # Hàm chỉ check được 1 
    def checkCallback(*ignoredArgs):
        # Chỉ chọn 1 checkbutton
        if chVarUn.get(): check3.configure(state="disabled")
        else:
            check3.configure(state="normal")
        if chVarEn.get(): check2.configure(state="disabled")
        else:
            check2.configure(state="normal")

    # Hàm xử lý khi chọn Radio Button thay đổi màu cho LabelFrame 
    def change_color(color):
        labels_frame.config(fg=color)

    # Tạo Label với Textbox
    ttk.Label(mighty_1, text="Nhập tên của bạn:").grid(column=0, row=0, sticky='W')
    name = tk.StringVar()
    name_entered = ttk.Entry(mighty_1, textvariable=name)
    name_entered.grid(column=0, row=1, sticky="W")

    # Tạo Label với Combobox
    ttk.Label(mighty_1, text="Chọn một số:").grid(column=1, row=0, sticky='W')
    number = tk.StringVar()
    number_chosen = ttk.Combobox(mighty_1, textvariable=number, state='readonly')
    number_chosen['values'] = (1, 2, 3, 4, 5, 14, 28, 44, 96, 100)
    number_chosen.grid(column=1, row=1)
    number_chosen.current(0)

    action = ttk.Button(mighty_1, text="Click Me!", command=click_me)
    action.grid(column=2, row=1)   

    # Tạo Label với Scrolled text control
    ttk.Label(mighty_1, text="Ghi chú:").grid(column=0, row=2, sticky='W')
    number = tk.StringVar()
    scrol_w=42
    scrol_h=3
    scr = scrolledtext.ScrolledText(mighty_1, width=scrol_w, height=scrol_h, wrap=tk.WORD)
    scr.grid(column=0, row=3, columnspan=3)

    # Place cursor into name Entry
    name_entered.focus() 


    ### Frame 2
    mighty_12 = ttk.LabelFrame(tab1, text='Cảm nhận')
    mighty_12.pack(padx=8, pady=4, fill='both', expand=True)

    # Create 3 checkbuttons
    chVarDis = tk.IntVar()
    check1 = tk.Checkbutton(mighty_12, text="Không chọn được đâu", variable=chVarDis, state='disabled')
    check1.deselect()
    check1.grid(column=0, row=0, sticky=tk.W)                 

    chVarUn = tk.IntVar()
    check2 = tk.Checkbutton(mighty_12, text="Không Like", variable=chVarUn)
    check2.deselect()
    check2.grid(column=1, row=0, sticky=tk.W)

    chVarEn = tk.IntVar()
    check3 = tk.Checkbutton(mighty_12, text="Like", variable=chVarEn)
    check3.deselect()
    check3.grid(column=2, row=0, sticky=tk.W) 

    # Trace the state of the two checkbuttons
    chVarUn.trace("w",lambda unused0,unused1,unused2 : checkCallback())
    chVarEn.trace("w",lambda unused0,unused1,unused2 : checkCallback())

    # Tạo hàm để thay đổi màu của LabelFrame khi chọn Radio Button
    labels_frame = tk.LabelFrame(mighty_12, text='Cảm ơn bạn đã sử dụng!')
    labels_frame.grid(column=0, row=3, columnspan=3, sticky='EW', padx=8, pady=4)

    # Radio Button - Thay đổi màu sắc của LabelFrame
    color_var = tk.StringVar()

    radio1 = ttk.Radiobutton(labels_frame, text="Xanh dương", variable=color_var, value="blue", command=lambda: change_color("blue"))
    radio1.grid(column=0, row=2, sticky='W')
    radio2 = ttk.Radiobutton(labels_frame, text="Vàng Gold", variable=color_var, value="gold", command=lambda: change_color("gold"))
    radio2.grid(column=1, row=2, sticky='W')
    radio3 = ttk.Radiobutton(labels_frame, text="Đỏ", variable=color_var, value="red", command=lambda: change_color("red"))
    radio3.grid(column=2, row=2, sticky='W')
    radio4 = ttk.Radiobutton(labels_frame, text="Xanh lá", variable=color_var, value="green", command=lambda: change_color("green"))
    radio4.grid(column=3, row=2, sticky='W')
    radio5 = ttk.Radiobutton(labels_frame, text="Đen", variable=color_var, value="black", command=lambda: change_color("black"))
    radio5.grid(column=4, row=2, sticky='W')


    # ----#----#----#----#----#----#----#----#
    ''' Tab 2 Contents '''
    mighty_2 = ttk.LabelFrame(tab2, text='Cộng, Trừ, Nhân, Chia')
    mighty_2.grid(column=0, row=0, padx=8, pady=4, sticky="EW", columnspan=3)

    # Hàm tính toán
    def cong_ab():
        try:
            kqcong = float(a.get()) + float(b.get())
            ketqua.set(kqcong)
            ketqua_lb.config(text=f"Kết quả: {kqcong}")
        except ValueError:
            messagebox.showerror('Thông báo lỗi', 'Lỗi: Dữ liệu nhập không hợp lệ! \nVui lòng nhập lại dữ liệu')

    def tru_ab():
        try:
            kqtru = float(a.get()) - float(b.get())
            ketqua.set(kqtru)
            ketqua_lb.config(text=f"Kết quả: {kqtru}")
        except ValueError:
            messagebox.showerror('Thông báo lỗi', 'Lỗi: Dữ liệu nhập không hợp lệ! \nVui lòng nhập lại dữ liệu')

    def nhan_ab():
        try:
            kqnhan = float(a.get()) * float(b.get())
            ketqua.set(kqnhan)
            ketqua_lb.config(text=f"Kết quả: {kqnhan}")
        except ValueError:
            messagebox.showerror('Thông báo lỗi', 'Lỗi: Dữ liệu nhập không hợp lệ! \nVui lòng nhập lại dữ liệu')

    def chia_ab():
        try:
            if float(b.get()) == 0:
                raise ZeroDivisionError
            kqchia = float(a.get()) / float(b.get())
            ketqua.set(kqchia)
            ketqua_lb.config(text=f"Kết quả: {kqchia}")
        except ValueError:
            messagebox.showerror('Thông báo lỗi', 'Lỗi: Dữ liệu nhập không hợp lệ! \nVui lòng nhập lại dữ liệu')
        except ZeroDivisionError:
            messagebox.showerror('Thông báo lỗi', 'Lỗi: Không thể chia cho 0!')

    def reset_values():
        answer = messagebox.askyesnocancel('Xác nhận', 'Bạn có chắc chắn muốn reset không?')
        if answer:  # Nếu người dùng chọn Yes
            a.set("")
            b.set("")
            ketqua.set("")
            ketqua_lb.config(text="Kết quả: ")


    ### Frame "Nhập"
    frame_nhap = ttk.LabelFrame(mighty_2, text="Nhập", padding=(10, 10))
    frame_nhap.grid(column=0, row=0, padx=5, pady=5, sticky='nswe')

    label_a = ttk.Label(frame_nhap, width=8, text="Hệ số a: ")
    label_a.grid(column=0, row=0, padx=10, pady=10)
    label_b = ttk.Label(frame_nhap, width=8, text="Hệ số b: ")
    label_b.grid(column=0, row=1, padx=10, pady=10)

    a = tk.StringVar()
    text_a = ttk.Entry(frame_nhap, width=16, textvariable=a)
    text_a.grid(column=1, row=0, padx=5, pady=5)
    b = tk.StringVar()
    text_b = ttk.Entry(frame_nhap, width=16, textvariable=b)
    text_b.grid(column=1, row=1, padx=5, pady=5)


    ### Frame "Tính"
    frame_tinh = ttk.LabelFrame(mighty_2, text="Tính", padding=(10, 10))
    frame_tinh.grid(column=1, row=0, padx=5, pady=5, sticky='nswe')

    cong = ttk.Button(frame_tinh, width=6, text="+", command=cong_ab)
    cong.grid(column=0, row=0, padx=5, pady=5)
    tru = ttk.Button(frame_tinh, width=6, text="-", command=tru_ab)
    tru.grid(column=1, row=0, padx=5, pady=5)
    nhan = ttk.Button(frame_tinh, width=6, text="*", command=nhan_ab)
    nhan.grid(column=0, row=1, padx=5, pady=5)
    chia = ttk.Button(frame_tinh, width=6, text="/", command=chia_ab)
    chia.grid(column=1, row=1, padx=5, pady=5)

    reset_button = ttk.Button(frame_tinh, text="Reset", command=reset_values)
    reset_button.grid(column=0, row=2, columnspan=2, padx=5, pady=5)


    ### Frame "Kết quả"
    frame_ketqua = ttk.LabelFrame(mighty_2, text="Kết quả", padding=(10, 10))
    frame_ketqua.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky='nswe')

    ketqua = tk.StringVar()
    ketqua_lb = ttk.Label(frame_ketqua, textvariable=ketqua)
    ketqua_lb.grid(column=0, row=0)


    # ----#----#----#----#----#----#----#----#
    ''' Tab 3 Contents '''
    mighty_3 = ttk.LabelFrame(tab3, text='Giải phương trình bậc 2')
    mighty_3.grid(column=0, row=0, padx=8, pady=4, sticky="EW", columnspan=3)

    ### Frame "Nhập hệ số"
    frame_pt = ttk.LabelFrame(mighty_3, text="Nhập hệ số a, b, c", padding=(10, 10))
    frame_pt.grid(column=0, row=0, padx=5, pady=5, sticky='nswe')

    label_a2 = ttk.Label(frame_pt, text="Hệ số a:")
    label_a2.grid(column=0, row=0, padx=10, pady=5)
    label_b2 = ttk.Label(frame_pt, text="Hệ số b:")
    label_b2.grid(column=0, row=1, padx=10, pady=5)
    label_c2 = ttk.Label(frame_pt, text="Hệ số c:")
    label_c2.grid(column=0, row=2, padx=10, pady=5)

    a2 = tk.StringVar()
    text_a2 = ttk.Entry(frame_pt, width=16, textvariable=a2)
    text_a2.grid(column=1, row=0, padx=5, pady=5)

    b2 = tk.StringVar()
    text_b2 = ttk.Entry(frame_pt, width=16, textvariable=b2)
    text_b2.grid(column=1, row=1, padx=5, pady=5)

    c2 = tk.StringVar()
    text_c2 = ttk.Entry(frame_pt, width=16, textvariable=c2)
    text_c2.grid(column=1, row=2, padx=5, pady=5)


    ### Frame "Kết quả" 
    frame_ketqua2 = ttk.LabelFrame(mighty_3, text="Kết quả", padding=(10, 10))
    frame_ketqua2.grid(column=1, row=0, padx=5, pady=5, sticky='nswe')

    ketqua2 = tk.StringVar()
    ketqua_lb2 = ttk.Label(frame_ketqua2, textvariable=ketqua2, width=20)
    ketqua_lb2.grid(column=0, row=0)

    # Hàm giải phương trình bậc 2
    def giai_pt_bac_2():
        try:
            a = float(a2.get())
            b = float(b2.get())
            c = float(c2.get())
            delta = b**2 - 4*a*c
            
            if delta > 0:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                ketqua2.set(f"Có 2 nghiệm: \n x1 = {x1}, \n x2 = {x2}")
            elif delta == 0:
                x = -b / (2*a)
                ketqua2.set(f"Có 1 nghiệm: x = {x}")
            else:
                ketqua2.set("Không có nghiệm thực.")
        except ValueError:
            messagebox.showerror('Thông báo lỗi', 'Lỗi: Dữ liệu nhập không hợp lệ!')

    # Nút tính toán
    btn_giai = ttk.Button(mighty_3, text="Giải", command=giai_pt_bac_2)
    btn_giai.grid(column=0, row=1, padx=5, pady=5)

    # Hàm Reset
    def reset_pt():
        answer = messagebox.askyesnocancel('Xác nhận', 'Bạn có chắc chắn muốn reset không?')
        if answer:  # Nếu người dùng chọn Yes
            a2.set("")
            b2.set("")
            c2.set("")
            ketqua2.set("")

    # Nút Reset
    btn_reset = ttk.Button(mighty_3, text="Reset", command=reset_pt)
    btn_reset.grid(column=1, row=1, padx=5, pady=5)

    # set Focus
    text_a.focus()


    # Căn giữa cửa sổ
    center_window(win)

    # Chạy GUI
    win.mainloop()