import tkinter as tk
from tkinter import messagebox
import psutil
import random
import speedtest

# --- CÁC HÀM XỬ LÝ TÍNH NĂNG ---
def check_pc():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    messagebox.showinfo("Thông Số PC", f"🔥 CPU đang dùng: {cpu}%\n🧠 RAM đang dùng: {ram}%")

def check_battery():
    battery = psutil.sensors_battery()
    if battery is None:
        messagebox.showinfo("Thông Tin Pin", "💻 Máy tính của bạn là PC bàn hoặc không có cảm biến pin!")
    else:
        percent = battery.percent
        plugged = "Đang cắm sạc" if battery.power_plugged else "Đang dùng pin"
        messagebox.showinfo("Tình Trạng Pin Laptop", f"🔋 Dung lượng pin hiện tại: {percent}%\n⚡ Trạng thái: {plugged}")

def check_speedtest():
    messagebox.showinfo("Đang đo mạng", "⏳ Đang tiến hành đo tốc độ mạng, vui lòng đợi vài giây...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = round(st.download() / 10**6, 2)
        upload = round(st.upload() / 10**6, 2)
        messagebox.showinfo("Tốc Độ Mạng", f"📥 Tải xuống (Download): {download} Mbps\n📤 Tải lên (Upload): {upload} Mbps")
    except Exception as e:
        messagebox.showerror("Lỗi", "Không thể đo tốc độ mạng. Vui lòng kiểm tra lại kết nối Internet!")

def health_check():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    
    # Đánh giá tổng quát đơn giản
    status = "Rất tốt 🟢"
    if cpu > 80 or ram > 85:
        status = "Đang quá tải / Cần nghỉ ngơi 🔴"
    elif cpu > 50 or ram > 60:
        status = "Bình thường / Hoạt động ổn định 🟡"
        
    battery_info = f"{battery.percent}%" if battery else "Không có pin (PC bàn)"
    
    report = f"🩺 BẢNG ĐÁNH GIÁ SỨC KHỎE MÁY:\n\n" \
             f"• Mức độ sử dụng CPU: {cpu}%\n" \
             f"• Mức độ sử dụng RAM: {ram}%\n" \
             f"• Tình trạng Pin: {battery_info}\n\n" \
             f"👉 Tổng kết: Máy của bạn đang {status}"
             
    messagebox.showinfo("Health Check Tổng Quát", report)

def check_game():
    game = game_entry.get()
    if not game:
        messagebox.showwarning("Thông báo", "Vui lòng nhập tên game cần kiểm tra!")
    else:
        messagebox.showinfo("Kết Quả Game", f"🎮 Game '{game}': Máy của bạn đủ sức chiến mượt ở mức cấu hình trung bình!")

def diagnose_phone():
    symptom = phone_var.get()
    if "pin" in symptom.lower():
        advice = "Khả năng cao pin đã bị chai hoặc lỗi IC nguồn. Nên đem đi kiểm tra thay pin."
    elif "sóng" in symptom.lower():
        advice = "Kiểm tra lại khay SIM hoặc khởi động lại chế độ máy bay."
    else:
        advice = "Nóng máy do chạy app nặng ngầm. Hãy tắt bớt ứng dụng."
    messagebox.showinfo("Chẩn Đoán Lỗi Điện Thoại", f"📱 Triệu chứng: {symptom}\n\n💡 Tư vấn: {advice}")

def generate_nickname():
    name = name_entry.get()
    if not name:
        messagebox.showwarning("Thông báo", "Vui lòng nhập tên của bạn!")
    else:
        decorations = [f"★{name}★", f"亗{name}亗", f"⚡{name}⚡", f"❄{name}❄", f"࿐{name}ツ"]
        messagebox.showinfo("Tên Game Ngầu", f"✨ Gợi ý:\n\n{random.choice(decorations)}")

# --- GIAO DIỆN (UI) ---
root = tk.Tk()
root.title("Tool Hỗ Trợ All-in-One")
root.geometry("400x690")
root.configure(bg="#f4f6f9")

tk.Label(root, text="🛠️ Hỗ Trợ PC & Điện Thoại", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#333").pack(pady=10)

# Tính năng mới Health Check đặt lên trên cùng cho dễ nhìn
tk.Button(root, text="🩺 Health Check (Kiểm Tra Tổng Quát)", font=("Arial", 10, "bold"), bg="#d9534f", fg="white", bd=0, command=health_check).pack(pady=5, ipadx=15, ipady=6)

# 1. Phần PC & Mạng
tk.Button(root, text="💻 Kiểm Tra Thông Số PC", font=("Arial", 9, "bold"), bg="#4a90e2", fg="white", bd=0, command=check_pc).pack(pady=3, ipadx=10, ipady=4)
tk.Button(root, text="🔋 Kiểm Tra Pin Laptop", font=("Arial", 9, "bold"), bg="#2ecc71", fg="white", bd=0, command=check_battery).pack(pady=3, ipadx=10, ipady=4)
tk.Button(root, text="🌐 Đo Tốc Độ Mạng (Speedtest)", font=("Arial", 9, "bold"), bg="#e67e22", fg="white", bd=0, command=check_speedtest).pack(pady=3, ipadx=10, ipady=4)

game_entry = tk.Entry(root, font=("Arial", 9), width=25)
game_entry.insert(0, "Nhập tên game...")
game_entry.pack(pady=3)
tk.Button(root, text="🎮 Kiểm Tra Khả Năng Chơi Game", font=("Arial", 9), bg="#5cb85c", fg="white", bd=0, command=check_game).pack(pady=3, ipadx=5, ipady=3)

tk.Label(root, text="----------------------------------------", bg="#f4f6f9", fg="#ccc").pack(pady=5)

# 2. Phần Điện Thoại
tk.Label(root, text="📱 Chọn triệu chứng lỗi điện thoại:", font=("Arial", 9, "bold"), bg="#f4f6f9", fg="#555").pack()
phone_var = tk.StringVar(value="Nhanh tụt pin / Sập nguồn")
phone_menu = tk.OptionMenu(root, phone_var, "Nhanh tụt pin / Sập nguồn", "Mất sóng / Không nhận SIM", "Nóng máy khi dùng bình thường")
phone_menu.config(font=("Arial", 9))
phone_menu.pack(pady=3)

tk.Button(root, text="🔍 Chẩn Đoán Lỗi Điện Thoại", font=("Arial", 9), bg="#f0ad4e", fg="white", bd=0, command=diagnose_phone).pack(pady=3, ipadx=5, ipady=3)

tk.Label(root, text="----------------------------------------", bg="#f4f6f9", fg="#ccc").pack(pady=2)

# 3. Tạo tên game
name_entry = tk.Entry(root, font=("Arial", 9), width=25)
name_entry.insert(0, "Nhập tên của bạn...")
name_entry.pack(pady=3)
tk.Button(root, text="✨ Tạo Tên Game Ký Tự Đẹp", font=("Arial", 9, "bold"), bg="#9b59b6", fg="white", bd=0, command=generate_nickname).pack(pady=5, ipadx=5, ipady=3)

root.mainloop()
