
# ---------------------------- CONSTANTS ------------------------------- #
import tkinter
import pygame
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
rep = 0
timer = ''


# ---------------------------- TIMER RESET ------------------------------- # 
def reset():
    global rep
    click.play()
    start_button.config(state="normal")
    window.after_cancel(timer)
    tomato.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark.config(text='')
    rep = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_count():
    global rep
    start_button.config(state="disabled")
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    rep += 1
    if rep % 2 != 0:
        ping_sound.play()
        timer_label.config(text="WORK", fg=GREEN)
        countdown(work_sec)
    elif rep % 8 == 0:
        ping2_sound.play()
        timer_label.config(text="BREAK", fg=RED)
        countdown(long_break_sec)
    elif rep % 2 == 0:
        ping2_sound.play()
        timer_label.config(text="BREAK", fg=PINK)
        countdown(short_break_sec)

    '''Tại sao ko gọi countdown luôn mà gọi start_count
    tại vì ko gọi full chắc năng coundown(25) vào command của button được, phải bỏ (25) ra'''


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):
    global timer
    count_min = int(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    """itemconfig là 1 func cần phải bỏ vào biến và **kwarg, bởi vậy phải cho nó vào một biến (timer_text)
    chứ ko bỏ vào chính nó đc"""
    tomato.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, countdown, count-1)
    elif count == 0:
        window.lift()
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)
        checkmark_num = ""
        start_count()
        for i in range(int(rep/2)):
            checkmark_num += "✔"
            checkmark.config(text=checkmark_num)
    '''*arg count-1 sẽ đưa vào function'''
    '''Khi gọi countdown thì phải gọi phía dưới tomato canvas nếu ko lúc đó chưa tồn tại tomato để config'''


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = tkinter.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
timer_label.grid(column=2, row=1)

tomato = tkinter.Canvas(width=205, height=224, bg=YELLOW)
tomato_img = tkinter.PhotoImage(file="tomato.png")
tomato.create_image(101, 112, image=tomato_img)
timer_text = tomato.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
tomato.grid(column=2, row=2)


start_button = tkinter.Button(text="Start", font=(FONT_NAME, 10, "bold"), command=start_count)
start_button.grid(column=1, row=3)
reset_button = tkinter.Button(text="Reset", font=(FONT_NAME, 10, "bold"), command=reset)
reset_button.grid(column=3, row=3)

"""Dùng thư viện Pillow để chỉnh lại kích thước hình, đồng thời để ý dùng ImageTk.PhotoImage
 để đọc hình ảnh mới chứ ko dùng Tkinter như tomato"""


checkmark = tkinter.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 18, "bold"))
checkmark.grid(column=2, row=3)

'''có thể chỉnh âm lượng trong init(), vào đó xem'''
pygame.mixer.init()
ping_sound = pygame.mixer.Sound("news-ting-6832.wav")
ping2_sound = pygame.mixer.Sound("ping.wav")
click = pygame.mixer.Sound("mouse-click-153941.mp3")

"""mainloop nó thực ra là 1 vòng lặp liên tục refresh khung hình và liên tục lắng nghe input, nên nếu trước đó dùng 
Loop để countdown thì sẽ không thấy hiệu ứng countdown trên GUI vì mainloop tạm ngưng cho vòng Loop countdown"""
window.mainloop()
