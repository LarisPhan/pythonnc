from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
import psycopg2
from psycopg2 import sql
from database import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Route trang đăng nhập (mặc định)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        user = request.form['user']
        password = request.form['password']
        
        # Tạo kết nối với thông tin từ form
        db = Database(db_name='dbtest', user=user, password=password, host='localhost', port=5432)
        if db.connect():
            # Lưu thông tin đăng nhập trong session
            session['user'] = user
            session['password'] = password
            db.cur.close()  # Đóng cursor
            db.conn.close()  # Đóng kết nối
            
            # Kết nối thành công, chuyển đến trang home
            return redirect(url_for('home'))
        else:
            # Kết nối thất bại, hiển thị thông báo lỗi
            flash("Kết nối không thành công. <br> Vui lòng kiểm tra lại thông tin đăng nhập.", 'error')
    
    return render_template('index.html')


# Trang Home
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Kiểm tra session trước khi truy cập trang home
    if 'user' in session and 'password' in session:
        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        
        if db.connect():
            if request.method == 'POST':
                search_type = request.form['search_type']
                search_value = request.form['search_value']
                
                # Tìm kiếm theo loại đã chọn
                if search_type == 'mssv':
                    query = "SELECT * FROM thongtin WHERE mssv = %s"
                    db.cur.execute(query, (search_value,))
                elif search_type == 'hoten':
                    query = "SELECT * FROM thongtin WHERE hoten ILIKE %s"  # Sử dụng ILIKE để tìm kiếm không phân biệt chữ hoa chữ thường
                    db.cur.execute(query, ('%' + search_value + '%',))
                
                data = db.cur.fetchall()
            else:
                # Nếu không có tìm kiếm, lấy tất cả sinh viên
                db.cur.execute('SELECT * FROM thongtin')
                data = db.cur.fetchall()

            db.cur.close()
            db.conn.close()
            return render_template('home.html', data=data)
    
    # Nếu không có thông tin đăng nhập, chuyển về trang đăng nhập
    flash("Bạn cần đăng nhập để truy cập trang này.", 'error')
    return render_template('index.html')


# Add thong tin [addinfor.html]
@app.route('/home/addinfor', methods=['GET'])
def addinfor():
    return render_template('addinfor.html')

@app.route('/home/add', methods=['POST'])
def add_data():
    # Kiểm tra session trước khi cho phép thêm dữ liệu
    if 'user' in session and 'password' in session:
        # Lấy dữ liệu từ form
        new_mssv = request.form['mssv']
        new_hoten = request.form['hoten']
        new_gioitinh = request.form['gioitinh']
        new_quequan = request.form['quequan']
        
        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                # Thêm dữ liệu vào bảng thongtin
                insert_query = "INSERT INTO thongtin (mssv, hoten, gioitinh, quequan) VALUES (%s, %s, %s, %s)"
                db.cur.execute(insert_query, (new_mssv, new_hoten, new_gioitinh, new_quequan))
                db.conn.commit()
                flash("Thêm dữ liệu thành công.", 'success')
            except Exception as e:
                flash(f"Lỗi khi thêm dữ liệu: {e}", 'error')
            finally:
                db.cur.close()
                db.conn.close()
                
    # Chuyển hướng tới trang home sau khi thêm thành công
    return redirect(url_for('home'))


# Update thong tin [updateinfor.html]
@app.route('/home/update/<mssv>', methods=['GET', 'POST'])
def update_data(mssv):
    db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
    
    if db.connect():
        if request.method == 'POST':
            # Lấy dữ liệu từ form
            new_hoten = request.form['hoten']
            new_gioitinh = request.form['gioitinh']
            new_quequan = request.form['quequan']

            try:
                # Cập nhật dữ liệu vào bảng thongtin
                update_query = "UPDATE thongtin SET hoten = %s, gioitinh = %s, quequan = %s WHERE mssv = %s"
                db.cur.execute(update_query, (new_hoten, new_gioitinh, new_quequan, mssv))
                db.conn.commit()
                flash("Cập nhật dữ liệu thành công.", 'success')
            except Exception as e:
                flash(f"Lỗi khi cập nhật dữ liệu: {e}", 'error')
            finally:
                db.cur.close()
                db.conn.close()
            
            return redirect(url_for('home'))
        
        # Lấy thông tin sinh viên
        select_query = "SELECT hoten, gioitinh, quequan FROM thongtin WHERE mssv = %s"
        db.cur.execute(select_query, (mssv,))
        student_info = db.cur.fetchone()
        db.cur.close()
        
        if student_info:
            return render_template('updateinfor.html', mssv=mssv, hoten=student_info[0], gioitinh=student_info[1], quequan=student_info[2])
    
    flash("Không tìm thấy thông tin sinh viên.", 'error')
    return redirect(url_for('home'))


# Delete thong tin 
@app.route('/home/delete/<mssv>', methods=['POST'])
def delete_data(mssv):
    db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
    
    if db.connect():
        try:
            # Xóa dữ liệu khỏi bảng thongtin
            delete_query = "DELETE FROM thongtin WHERE mssv = %s"
            db.cur.execute(delete_query, (mssv,))
            db.conn.commit()
            flash("Xóa dữ liệu thành công.", 'success')
        except Exception as e:
            flash(f"Lỗi khi xóa dữ liệu: {e}", 'error')
        finally:
            db.cur.close()
            db.conn.close()
    
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5050)
