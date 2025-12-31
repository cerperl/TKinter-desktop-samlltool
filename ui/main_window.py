import sys
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


import tkinter as tk
from tkinter import messagebox
import threading #线程工具
from api.weather import get_weather
from api.moon_phase import get_moon_phase
import datetime
import json

# 用户数据文件路径（位于 ui/ 下）
USER_DATA_FILE = Path(__file__).resolve().parent / 'user_data.json'


def load_user_data():
        try:
                if USER_DATA_FILE.exists():
                        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                                return json.load(f)
        except Exception as e:
                print(f"读取用户数据失败: {e}")
        return {}


def save_user_data(data: dict):
        try:
                USER_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
                print(f"保存用户数据失败: {e}")


# ========== 1.初始化 & 窗口 ===========
#界面设置
MainWindow = tk.Tk()
MainWindow.title("每日工具箱")
MainWindow.geometry('350x500')
MainWindow.resizable(False, False)
MainWindow.attributes('-alpha', 1)

#背景label
bg_label = tk.Label(MainWindow)
bg_label.place(x=0 ,y=0, relwidth=1, relheight=1)

# ========== 2.布局(Frame / Label/ Button) ===========
#日期
frame_days = tk.Frame(MainWindow, width=320, height=30, bg='lightgray')
frame_days.pack(pady=10)

#日期界面
days_label = tk.Label(frame_days, text='', font=('SimHei', 14))
days_label.place(x=0, y=10)

#天气情况
frame_weather = tk.Frame(MainWindow, width=320, height=200, bg='lightgray')
frame_weather.pack(pady=25)

#天气部分
weather_name = tk.Label(MainWindow, text='今日天气', font=('SimHei', 14), bg='lightgray')
weather_name.place(x=15, y=45)

moon_name = tk.Label(MainWindow, text='月相', font=('SimHei', 14), bg='lightgray')
moon_name.place(x=289, y=45)

defult_weather = 0
weather_text = tk.Text(frame_weather, width=25, height=8, font=("Consolas", 12))
weather_text.place(x=15, y=10)
weather_text.config(state="disabled", bg="lightgray", bd=0)

#月相
moon_text = tk.Text(frame_weather, width=25, height=8, font=("Consolas", 12))
moon_text.place(x=270, y=10)
moon_text.config(state="disabled", bg="lightgray", bd=0)

#等待开发区
frame_todo = tk.Frame(MainWindow, width=320, height=150, bg='lightgray')
frame_todo.place(x=15, y=320)
frame_todo.grid_propagate(False) #锁死frame尺寸
# ========== 3. UI更新函数(只负责config)===========

def update_weather(weather_list):
        """weather_list是get_weather()返回的列表"""
        weather_text.config(state="normal") #先解锁
        weather_text.delete("1.0", tk.END) #清空原内容
        for line in weather_list:
                weather_text.insert(tk.END, line + "\n")

        weather_text.config(state="disabled") #再锁定
        # 更新月相显示
        moon = get_moon_phase()
        moon_text.config(state="normal")
        moon_text.delete("1.0", tk.END)
        moon_text.insert(tk.END, moon)
        moon_text.config(state="disabled")
        
def _weather_worker():
        try: #异常检测
                result = get_weather() #数据获取没问题
                if not result or not isinstance(result, list):
                        raise ValueError("返回数据为空或者格式错误") #手动抛出异常
        except Exception as e:
                result = [f"更新异常: {e}"]

        MainWindow.after(0, update_weather, result)


def fresh_weahter():
       threading.Thread(
        target=_weather_worker, 
        daemon=True
       ).start()
       

weather_button = tk.Button(frame_weather, command=fresh_weahter, text='刷新天气', bg='lightgray')
weather_button.place(x=250, y=150)

# 自动天气更新间隔（毫秒）
WEATHER_UPDATE_INTERVAL =  12 * 60 * 60 * 1000  # 一天刷新

def schedule_weather_update():
        fresh_weahter() #先更新一次
        MainWindow.after(WEATHER_UPDATE_INTERVAL, schedule_weather_update)

#首次启动并更新
fresh_weahter()
MainWindow.after(WEATHER_UPDATE_INTERVAL, schedule_weather_update)

#时间实时显示
def Time_Now():
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_text = time_now
        days_label.config(text=time_now)
        frame_days.after(1000, Time_Now)
Time_Now()

# ========== 4. 加点分配功能()===========       -40 生命 智力 体力 根据输入摄生日来确定初始点数

#文本、按钮设置
settingtext_style = {
    "width": 8,
    "height": 1,
    "font": ("Consolas", 10),
    "bg": "lightgray",
    "bd": 1
}

text_style = {
    "width": 14,
    "height": 1,
    "font": ("Consolas", 12),
    "bg": "lightgray",
    "bd": 1
}

point_button_style = {
        "width": 10,
        "height": 1,
        "font": ("Consolas", 10),
        "bg": "lightgray",
        "bd": 1
}

#生日输入框
age_value = None
# 当前点数（默认值，用户设置生日后会重置）
hp_points = 10
mp_points = 10
sp_points = 10

def day_setting():
        global age_value #外部变量以取生日
        days_window = tk.Toplevel()
        days_window.title("请输入日期")
        days_window.geometry('250x80')
        #输入框
        s1 = tk.StringVar()
        s1.set('19980101')

        tk.Entry(days_window, textvariable=s1, width=15, font=('SimHei', 15)).pack() #输入框

 #确定按钮并返回s1
        def check_string():
                global age_value, hp_points, mp_points, sp_points
                s = s1.get().strip()
                try:
                        if not (s.isdigit() and len(s) == 8):
                                raise ValueError("请输入 8 位数字，格式 YYYYMMDD")
                        birthday = datetime.datetime.strptime(s, "%Y%m%d").date()  # 转 datetime.date
                except Exception as e:
                        messagebox.showerror(title='错误', message=f'格式错误: {e}')
                        return

                today = datetime.date.today()
                # 计算年龄并考虑是否已过生日
                age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
                age_value = age

                # 使用年龄初始化点数并刷新显示
                hp_points, mp_points, sp_points = init_points(age)
                refresh_point_texts()

                messagebox.showinfo(title='成功', message=f'格式正确，年龄：{age} 岁')
                days_left = refresh_countdown(birthday, today)
                refresh_br_config(days_left)
                # 保存生日与当前点数
                save_user_data({
                        'birthday': s,
                        'hp_points': hp_points,
                        'mp_points': mp_points,
                        'sp_points': sp_points
                })
                days_window.destroy()
                
        days_setting_button = tk.Button(days_window, text='确定', command=check_string).pack()


#生日设置按钮
setting_button = tk.Button(
        frame_todo, 
        **settingtext_style, 
        text="setting", 
        command=day_setting
        )
setting_button.grid(row=0, column=3, padx=2, pady=4, sticky="w")

#根据生日设置默认点数
def init_points(age):
        base = 10
        # bonus 基于年龄的十年档位（例：0-9 为 +5，10-19 为 +4 等），并限制在 0..5
        bonus = max(0, min(5, 5 - age // 10))
        hp_points = base + bonus
        mp_points = base + bonus
        sp_points = base + bonus
        return hp_points, mp_points, sp_points


#默认属性文本
hp_text = tk.Text(frame_todo, **text_style)
hp_text.config(state='normal') #写入先解锁
hp_text.insert(tk.END, f"生命：{10}")
hp_text.config(state='disabled') #写入后锁定防止用户编辑
hp_text.grid(row=0, column=0, padx=10, pady=5, sticky="w")

mp_text = tk.Text(frame_todo, **text_style)
mp_text.config(state='normal')
mp_text.insert(tk.END, f"魔力：{10}")
mp_text.config(state='disabled')
mp_text.grid(row=2, column=0, padx=10, pady=5, sticky="w")

sp_text = tk.Text(frame_todo, **text_style)
sp_text.config(state='normal')
sp_text.insert(tk.END, f"体力：{10}")
sp_text.config(state='disabled')
sp_text.grid(row=4, column=0, padx=10, pady=5, sticky="w")



def refresh_point_texts(): #刷新点数显示
        hp_text.config(state='normal')
        hp_text.delete("1.0", tk.END)
        hp_text.insert(tk.END, f"生命：{hp_points}")
        hp_text.config(state='disabled')

        mp_text.config(state='normal')
        mp_text.delete("1.0", tk.END)
        mp_text.insert(tk.END, f"魔力：{mp_points}")
        mp_text.config(state='disabled')

        sp_text.config(state='normal')
        sp_text.delete("1.0", tk.END)
        sp_text.insert(tk.END, f"体力：{sp_points}")
        sp_text.config(state='disabled')


def update_points(age):
        """根据年龄重新初始化点数并刷新显示"""
        global hp_points, mp_points, sp_points
        hp_points, mp_points, sp_points = init_points(age)
        refresh_point_texts()


def inc_hp():
        global hp_points
        hp_points += 1
        refresh_point_texts()
        # 保存最新点数到文件
        data = load_user_data()
        data.update({'hp_points': hp_points, 'mp_points': mp_points, 'sp_points': sp_points})
        save_user_data(data)


def inc_mp():
        global mp_points
        mp_points += 1
        refresh_point_texts()
        # 保存最新点数到文件
        data = load_user_data()
        data.update({'hp_points': hp_points, 'mp_points': mp_points, 'sp_points': sp_points})
        save_user_data(data)


def inc_sp():
        global sp_points
        sp_points += 1
        refresh_point_texts()
        # 保存最新点数到文件
        data = load_user_data()
        data.update({'hp_points': hp_points, 'mp_points': mp_points, 'sp_points': sp_points})
        save_user_data(data)

#加点按纽

hp_button = tk.Button(frame_todo, **point_button_style, text='eating', command=inc_hp)
hp_button.grid(row=0, column=2, padx=10, pady=4, sticky="w")

mp_button = tk.Button(frame_todo, **point_button_style, text='coding', command=inc_mp)
mp_button.grid(row=2, column=2, padx=10, pady=4, sticky="w")

sp_button = tk.Button(frame_todo, **point_button_style, text='exercise', command=inc_sp)
sp_button.grid(row=4, column=2, padx=10, pady=4, sticky="w")


#文本格式：距离生日还有{}天

brithday_countdown = tk.Label(
        frame_todo, 
        text='距离生日还有  天', 
        width=20,
        height=2,
        font=("Consolas", 14),
        bg= "lightgray",
        bd=1
)
brithday_countdown.place(x=0, y=100)

def refresh_countdown(birthday:datetime, today:datetime) -> int:
        # 按公历月/日计算下次生日（最小改动，不处理闰年出生特殊情况）
        target_birthday = datetime.date(today.year, birthday.month, birthday.day)
        if target_birthday < today:
                target_birthday = datetime.date(today.year + 1, birthday.month, birthday.day)
        days_left = (target_birthday - today).days
        return days_left
                
                
def refresh_br_config(days_left):
        # 优先判断生日当天，再判断临近三天，否则显示常规倒计时
        if days_left == 0:
                brithday_countdown.config(text="今天是你的生日，生日快乐")
        elif days_left <= 3:
                brithday_countdown.config(text=f"{days_left}天后是你的生日")
        else:
                brithday_countdown.config(text=f"距离生日还有{days_left}天")

# 启动时读取用户数据并初始化生日倒计时与点数（若有保存）
user_data = load_user_data()
if user_data.get('birthday'):
        try:
                bstr = user_data['birthday']
                birthday = datetime.datetime.strptime(bstr, "%Y%m%d").date()
                today = datetime.date.today()
                # 计算年龄
                age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
                age_value = age
                # 使用保存的点数（若存在）或者按年龄初始化
                if all(k in user_data for k in ('hp_points','mp_points','sp_points')):
                        hp_points = user_data['hp_points']
                        mp_points = user_data['mp_points']
                        sp_points = user_data['sp_points']
                else:
                        hp_points, mp_points, sp_points = init_points(age)
                refresh_point_texts()
                days_left = refresh_countdown(birthday, today)
                refresh_br_config(days_left)
        except Exception as e:
                print(f"解析用户生日失败: {e}")

MainWindow.mainloop()