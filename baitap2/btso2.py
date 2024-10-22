import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from psycopg2 import sql
from PIL import Image, ImageTk
import os


class DatabaseApp:
    def __init__(self, win):
        self.win = win
        self.win.title("Hệ thống quản lý sinh viên")

        # Đường dẫn hình ảnh
        self.PATH_IMAGES = os.path.join(os.path.dirname(__file__), 'img', 'BB1msMpy.png')

        # Kích thước cửa sổ
        self.win.geometry("550x700")
        self.win.resizable(True, True)

        # Thông tin kết nối cơ sở dữ liệu
        self.db_name = tk.StringVar(value='quanlysinhvien')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='thongtin')
        self.delete_field = tk.StringVar()
        self.delete_value = tk.StringVar()
        self.filter_field = tk.StringVar()
        self.filter_value = tk.StringVar()

        self.columns = []  # Danh sách các cột

        # Tạo giao diện
        self.create_widgets()

        # Tạo menu bar
        menu_bar = tk.Menu(self.win)

        def exit():
            answer = messagebox.askyesnocancel('Message Box', 'Bạn có chắc chắn muốn thoát không?')
            if answer:  # Yes
                self.win.quit()
                self.win.destroy()

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        def msgBox():
            messagebox.showinfo('Message Box', 'Ứng dụng hiện đang trong giai đoạn phát triển')

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=msgBox)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.win.config(menu=menu_bar)

    def create_widgets(self):
        # Create a tab control
        self.tab_control = ttk.Notebook(self.win)
        
        # Create tabs
        self.connection_tab = ttk.Frame(self.tab_control)
        self.operation_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.connection_tab, text=" Kết nối cơ sở dữ liệu ")
        self.tab_control.add(self.operation_tab, text=" Quản lý sinh viên ")
        
        self.tab_control.pack(expand=1, fill='both')

        # Thêm hình nền
        self.add_background_image(self.connection_tab, self.PATH_IMAGES)

        # Connection section trong Tab 1
        connection_frame = tk.LabelFrame(self.connection_tab, text="Thông tin kết nối", padx=10, pady=10)
        connection_frame.pack(padx=10, pady=10, expand=True)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Operation section trong Tab 2
        operation_frame = tk.LabelFrame(self.operation_tab, text="Thao tác với dữ liệu sinh viên", padx=10, pady=10)
        operation_frame.pack(padx=10, pady=10, expand=True)

        tk.Label(operation_frame, text="Tên bảng dữ liệu:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(operation_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(operation_frame, text="Tải dữ liệu", command=self.load_data).grid(row=1, columnspan=2, padx=10, pady=10)

        # Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(self.operation_tab, columns=("MSSV", "Họ tên", "Giới tính", "Quê quán"), show='headings')
        self.tree.heading("MSSV", text="MSSV")
        self.tree.heading("Họ tên", text="Họ tên")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.heading("Quê quán", text="Quê quán")

        self.tree.column("MSSV", width=100)
        self.tree.column("Họ tên", width=175)
        self.tree.column("Giới tính", width=75)
        self.tree.column("Quê quán", width=150)

        self.tree.pack(pady=10, padx=10, fill='x')

        # Insert section
        insert_frame = tk.LabelFrame(operation_frame, text="Thêm thông tin sinh viên", padx=10, pady=10)
        insert_frame.grid(row=2, columnspan=2, padx=10, pady=10)

        self.col1_mssv = tk.StringVar()
        self.col2_hoten = tk.StringVar()
        self.col3_gender = tk.StringVar(value="Nam") 
        self.col4_quequan = tk.StringVar()

        tk.Label(insert_frame, text="MSSV:", width=8).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.col1_mssv, width=17).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Họ tên:", width=8).grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.col2_hoten, width=30).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(insert_frame, text="Giới tính:", width=8).grid(row=1, column=0, padx=5, pady=5)
        gender_options = ["Nam", "Nữ", "Khác"]
        gender_combobox = ttk.Combobox(insert_frame, textvariable=self.col3_gender, values=gender_options, width=14)
        gender_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Quê quán:", width=8).grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.col4_quequan, width=30).grid(row=1, column=3, padx=5, pady=5)

        tk.Button(insert_frame, text="Thêm sinh viên", command=self.insert_data).grid(row=3, columnspan=4, pady=10)

        # Delete section
        delete_frame = tk.LabelFrame(operation_frame, text="Xóa thông tin sinh viên", padx=10, pady=10)
        delete_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

        tk.Label(delete_frame, text="Cột:", width=8).grid(row=0, column=0, padx=5, pady=5)
        self.delete_field_combobox = ttk.Combobox(delete_frame, textvariable=self.delete_field, width=17)
        self.delete_field_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(delete_frame, text="Giá trị:", width=8).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(delete_frame, textvariable=self.delete_value, width=20).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(delete_frame, text="Xóa sinh viên", command=self.delete_data).grid(row=2, columnspan=2, pady=10)

        # Filter section
        filter_frame = tk.LabelFrame(operation_frame, text="Lọc thông tin sinh viên", padx=10, pady=10)
        filter_frame.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(filter_frame, text="Cột:", width=8).grid(row=0, column=0, padx=5, pady=5)
        self.filter_field_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_field, width=17)
        self.filter_field_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Giá trị:", width=8).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(filter_frame, textvariable=self.filter_value, width=20).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(filter_frame, text="Lọc sinh viên", command=self.filter_data).grid(row=2, columnspan=2, pady=10)

        # Căn giữa các frame
        for frame in [insert_frame, delete_frame, filter_frame]:
            frame.grid_configure(padx=10)

    def add_background_image(self, frame, image_path):
        try:
            image = Image.open(image_path)
            self.bg_image = ImageTk.PhotoImage(image)

            background_label = tk.Label(frame, image=self.bg_image)
            background_label.place(relwidth=1, relheight=1)

            background_label.lower()  # Đưa label xuống dưới cùng
        except FileNotFoundError:
            messagebox.showerror("Error", "Hình ảnh không tìm thấy: " + image_path)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Success", "Kết nối cơ sở dữ liệu thành công!")
            
            # Chuyển tab
            self.tab_control.select(self.operation_tab)
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi kết nối: {str(e)}")

    def load_data(self):
        try:
            # Lấy tên cột từ cơ sở dữ liệu
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (self.table_name.get(),))
            columns = self.cursor.fetchall()
            self.columns = [col[0] for col in columns]  # Cập nhật danh sách cột
            
            # Tải dữ liệu sinh viên
            self.cursor.execute(f"SELECT * FROM {self.table_name.get()}")
            rows = self.cursor.fetchall()

            self.tree.delete(*self.tree.get_children())  # Clear current content
            for row in rows:
                self.tree.insert("", tk.END, values=row)

            # Cập nhật giá trị cho combobox
            self.delete_field_combobox['values'] = self.columns
            self.filter_field_combobox['values'] = self.columns

        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi tải dữ liệu: {str(e)}")

    def insert_data(self):
        try:
            insert_query = sql.SQL(f"INSERT INTO {self.table_name.get()} (mssv, hoten, gioitinh, quequan) VALUES (%s, %s, %s, %s)")
            self.cursor.execute(insert_query, (self.col1_mssv.get(), self.col2_hoten.get(), self.col3_gender.get(), self.col4_quequan.get()))
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Success", "Thêm sinh viên thành công!")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi thêm sinh viên: {str(e)}")

    def delete_data(self):
        try:
            delete_query = sql.SQL(f"DELETE FROM {self.table_name.get()} WHERE {self.delete_field.get()} = %s")
            self.cursor.execute(delete_query, (self.delete_value.get(),))
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Success", "Đã xóa sinh viên thành công!")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi xóa sinh viên: {str(e)}")

    def filter_data(self):
        try:
            filter_query = sql.SQL(f"SELECT * FROM {self.table_name.get()} WHERE {self.filter_field.get()} = %s")
            self.cursor.execute(filter_query, (self.filter_value.get(),))
            rows = self.cursor.fetchall()

            self.tree.delete(*self.tree.get_children())  # Clear current content
            for row in rows:
                self.tree.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi lọc sinh viên: {str(e)}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()