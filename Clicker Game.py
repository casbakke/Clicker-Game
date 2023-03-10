import tkinter as tk
import threading, os, json
from time import sleep

# constants
LIGHT_GRAY = "#e0e0e0"
GRAY = "#c7c7c7"
DARK_GRAY = "#969696"

# load config file
with open("config.json", "r") as f:
    config = json.load(f)

balance = config["balance"]
cash_per_second = config["cps"]
cash_per_click = config["cpc"]
click_counter = [0, 0, 0, 0, 0]
clicks_per_second = 0.0
running = True

# define & configure Tk object
window = tk.Tk()
window.title("Clicker Game")
window.geometry("480x720+50+50")
window.maxsize(480, 720)
window.minsize(480, 720)

# home screen
def homescreen():

    global balance, cash_per_second, clicks_per_second

    # updates all of the labels on screen
    def update_labels():
        global balance

        mps = cash_per_second + (cash_per_click * clicks_per_second)

        lbl_cash_per_click["text"] = f"Cash per click: ${cash_per_click}"
        lbl_cash_per_sec["text"] = f"${mps} per second"
        lbl_money["text"] = f"${balance}"

    # swaps the screen to show a different interface
    def shop_clicked():
        def back_clicked():
            tk.Button(
                frm_body,
                bg = GRAY,
                activebackground = GRAY,
                text = "Click Me",
                font = ("Arial", 42),
                command = clicker_clicked,
            ).grid(row = 0, column = 0, ipadx = 50, ipady = 60) # create a new clicker button
            btn_shop["text"] = "Shop"
            btn_shop["command"] = shop_clicked

        frm_body.winfo_children()[0].destroy() # hide the clicker button
        btn_shop["text"] = "Back"
        btn_shop["command"] = back_clicked

    # save the user's data and exit the program
    def quit(bal, cpc, cps):
        global running, t1
        running = False # stop the other thread
        sleep(1) # delay to ensure the other thread is not mid-iteration
        window.destroy()

        outfile = {
            "balance": bal,
            "cps": cps,
            "cpc": cpc
        }

        # store the current state of the important variables in a config file
        with open("config.json", "w") as f:
            json.dump(outfile, f)

    # runs when the clicker button is pressed by the user
    def clicker_clicked():
        global balance, click_counter
        balance += cash_per_click
        click_counter[0] += 1

        update_labels()


    # configure window
    window.columnconfigure(0, minsize = 480)
    window.rowconfigure(0, minsize = 140)
    window.rowconfigure(1, minsize = 480)
    window.rowconfigure(2, minsize = 100)

    # define frames
    frm_head = tk.Frame(bg = GRAY)
    frm_body = tk.Frame(bg = LIGHT_GRAY)
    frm_foot = tk.Frame(bg = GRAY)

    # configure frames
    frm_head.columnconfigure(0, minsize = 480)
    frm_body.rowconfigure(0, minsize = 140)
    frm_body.columnconfigure(0, minsize = 480)
    frm_body.rowconfigure(0, minsize = 480)
    frm_foot.columnconfigure(0, minsize = 480)
    frm_foot.rowconfigure(0, minsize = 100)
    
    # place frames
    frm_head.grid(row = 0, column = 0, sticky = "nesw")
    frm_body.grid(row = 1, column = 0, sticky = "nesw")
    frm_foot.grid(row = 2, column = 0, sticky = "nesw")

    # define widgets
    lbl_money = tk.Label(
        frm_head,
        text = f"${balance}",
        font = ("Arial", 36),
        bg = GRAY,
    )

    lbl_cash_per_sec = tk.Label(
        frm_head,
        text = f"${cash_per_second} per second",
        font = ("Arial", 20),
        bg = GRAY,
    )

    lbl_cash_per_click = tk.Label(
        frm_head,
        text = f"Cash per click: ${cash_per_click}",
        font = ("Arial", 20),
        bg = GRAY,
    )

    btn_clicker = tk.Button(
        frm_body,
        bg = GRAY,
        activebackground = GRAY,
        text = "Click Me",
        font = ("Arial", 42),
        command = clicker_clicked,
    )

    btn_shop = tk.Button(
        frm_foot,
        text = "Shop",
        font = ("Arial", 26),
        bg = LIGHT_GRAY,
        activebackground = LIGHT_GRAY,
        command = shop_clicked,
        width = 7,
    )

    btn_quit = tk.Button(
        frm_foot,
        text = "Quit",
        font = ("Arial", 18),
        bg = DARK_GRAY,
        activebackground = DARK_GRAY,
        command = lambda: quit(balance, cash_per_click, cash_per_second),
        width = 5,
    )

    # place widgets
    lbl_money.grid(row = 0, column = 0)
    lbl_cash_per_sec.grid(row = 1, column = 0)
    lbl_cash_per_click.grid(row = 2, column = 0)
    btn_clicker.grid(row = 0, column = 0, ipadx = 50, ipady = 60)
    btn_shop.grid(row = 0, column = 0)

    btn_quit.place(x = 375, y = 25, height = 50)

    # while loop that runs in the background on another thread
    def clock():
        global running
        while running:
            global balance, cash_per_second, click_counter, clicks_per_second
            sleep(1)

            balance += cash_per_second # add {cash_per_second} to the user's balance once every second, this is the passive income system

            # average out the clicks per second from the last 5 seconds
            sum = click_counter[0] + click_counter[1] + click_counter[2] + click_counter[3] + click_counter[4]
            clicks_per_second = round((float(sum) / 5.0), 1)

            # move each value through a rotating list
            click_counter[4] = click_counter[3]
            click_counter[3] = click_counter[2]
            click_counter[2] = click_counter[1]
            click_counter[1] = click_counter[0]
            click_counter[0] = 0

            update_labels()

    # use multithreading so that this can run in the background without interfering with mainloop
    global t1
    t1 = threading.Thread(target = clock)

### start of runtime ###

homescreen() # show the homescreen
global t1
t1.start() # start the clock thread
window.mainloop() # show the GUI window
SystemExit()