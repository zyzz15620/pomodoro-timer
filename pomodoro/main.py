# ---------------------------- CONSTANTS ------------------------------- #
import tkinter
import pygame
PINK = "#e2979c"
RED = "#d62839"
GREEN = "#4CAF50"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
rep = 0
timer = ''

# Button colors - using vibrant, high-contrast colors
BUTTON_GREEN = "#4CAF50"  # Vibrant green
BUTTON_RED = "#d62839"    # Vibrant red
BUTTON_DISABLED = "#757575"  # Dark gray for disabled state


# ---------------------------- TIMER RESET ------------------------------- # 
def reset():
    global rep
    click.play()
    start_button.config(state="normal", bg=BUTTON_GREEN)  # Use darker green
    window.after_cancel(timer)
    tomato.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark.config(text='')
    rep = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_count():
    global rep
    start_button.config(state="disabled", bg=BUTTON_DISABLED)  # Use darker gray
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
window.config(padx=40, pady=30, bg=YELLOW)
window.resizable(False, False)  # Fix window size

# Style configurations
button_style = {
    "width": 8,
    "height": 2,
    "font": (FONT_NAME, 12, "bold"),
    "borderwidth": 0,
    "relief": "raised",
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white",
    "highlightbackground": YELLOW,
    "highlightthickness": 0,
    "overrelief": "raised",
    "padx": 10,
    "pady": 5
}

# Main timer label
timer_label = tkinter.Label(
    text="Timer",
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 35, "bold")
)
timer_label.grid(column=1, row=0, pady=(0, 10))

# Tomato canvas with timer
tomato = tkinter.Canvas(
    width=250,
    height=250,
    bg=YELLOW,
    highlightthickness=0
)
tomato_img = tkinter.PhotoImage(file="tomato.png")
tomato.create_image(125, 125, image=tomato_img)
timer_text = tomato.create_text(
    125,
    140,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)
tomato.grid(column=1, row=1, pady=10)

# Button frame for better alignment
button_frame = tkinter.Frame(bg=YELLOW)
button_frame.grid(column=1, row=2, pady=10)

# Start button
start_button = tkinter.Button(
    button_frame,
    text="Start",
    command=start_count,
    bg=BUTTON_GREEN,
    activebackground=BUTTON_GREEN,
    **button_style
)
# Force button appearance
start_button.configure(background=BUTTON_GREEN)
start_button.configure(highlightbackground=BUTTON_GREEN)
start_button.configure(activebackground=BUTTON_GREEN)
start_button.grid(column=0, row=0, padx=5)

# Reset button
reset_button = tkinter.Button(
    button_frame,
    text="Reset",
    command=reset,
    bg=BUTTON_RED,
    activebackground=BUTTON_RED,
    **button_style
)
# Force button appearance
reset_button.configure(background=BUTTON_RED)
reset_button.configure(highlightbackground=BUTTON_RED)
reset_button.configure(activebackground=BUTTON_RED)
reset_button.grid(column=1, row=0, padx=5)

# Bind hover events to maintain colors
def on_enter(e, button, color):
    button.configure(background=color)
    button.configure(highlightbackground=color)

def on_leave(e, button, color):
    button.configure(background=color)
    button.configure(highlightbackground=color)

start_button.bind('<Enter>', lambda e: on_enter(e, start_button, BUTTON_GREEN))
start_button.bind('<Leave>', lambda e: on_leave(e, start_button, BUTTON_GREEN))
reset_button.bind('<Enter>', lambda e: on_enter(e, reset_button, BUTTON_RED))
reset_button.bind('<Leave>', lambda e: on_leave(e, reset_button, BUTTON_RED))

# Checkmark label
checkmark = tkinter.Label(
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 24, "bold")
)
checkmark.grid(column=1, row=3, pady=10)

# Update disabled state styling
start_button.config(disabledforeground="white")
start_button.config(state="normal")  # Ensure button starts enabled

'''có thể chỉnh âm lượng trong init(), vào đó xem'''
pygame.mixer.init()
ping_sound = pygame.mixer.Sound("news-ting-6832.wav")
ping2_sound = pygame.mixer.Sound("ping.wav")
click = pygame.mixer.Sound("mouse-click-153941.mp3")

"""mainloop nó thực ra là 1 vòng lặp liên tục refresh khung hình và liên tục lắng nghe input, nên nếu trước đó dùng 
Loop để countdown thì sẽ không thấy hiệu ứng countdown trên GUI vì mainloop tạm ngưng cho vòng Loop countdown"""
window.mainloop()
