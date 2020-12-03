import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import serial
import sys
import time

try:
    ser = serial.Serial("/dev/ttyACM0",115200,timeout=1)
    # ser = serial.Serial("/dev/tty.usbmodem14103",115200,timeout=1)
    # ser = serial.Serial("/dev/ttys003",115200,timeout=1)
except:
    print("Couldn't open the serial port")
    # sys.exit(0)

window = tk.Tk()

x = tk.StringVar(window) # initial turn
f = tk.StringVar(window) # distance
y = tk.StringVar(window) # final turn

# to rename the title of the window
window.title("Teleop")
window.minsize(800,300)
window.geometry("800x600")
# pack is used to show the object in the window

# You will create two text labels namely 'username' and 'password' and and two input labels for them
tk.Label(window, text = "Controls", font=("", 24)).grid(row = 0, column = 0, sticky = '', pady = 10) #'username' is placed on position 00 (row - 0 and column - 0)
tk.Label(window, text = "Parameters", font=("", 24)).grid(row = 0, column = 2, sticky = '', pady = 10)

window.columnconfigure(0,weight=1)
window.columnconfigure(2,weight=4)
window.rowconfigure(0, weight = 0)
window.rowconfigure(1, weight = 4)
window.rowconfigure(3, weight = 4)

controls_frame = tk.Frame(window,name="controls_frame")
controls_frame.grid(row = 1, column = 0, sticky = 'NSEW')
wp_frame = tk.Frame(window,name="wp_frame")
wp_frame.grid(row = 3, column = 2, sticky = 'NSEW')
# params_frame = tk.Frame(window,name="params_frame")
# params_frame.grid(row = 1, column = 2, sticky = 'NSEW')

canvas = tk.Canvas(window,name="canvas")
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview, highlightcolor="snow2")
scrollable_frame = tk.Frame(canvas,width=800)
params_frame = tk.Frame(canvas,name="params_frame",width=537)
# scrollbar.pack(side="right", fill="y")
# params_frame.grid(row = 1, column = 2, sticky = 'NSEW')

# scrollable_frame = tk.Frame(canvas,bg="black")

temp_scroll = scrollbar.get()
scroll_len = temp_scroll[1]-temp_scroll[0]

canvas_frame = canvas.create_window((0, 0), window=params_frame, anchor="nw")

def configure_frame(e):
    global params_frame,canvas_frame
    # print(params_frame['width'])
    canvas_width = e.width
    # print("width " + str(canvas_width))
    # params_frame.config(width=canvas_width)
    canvas.itemconfig(canvas_frame, width = canvas_width)

def configure_canvas(e):
    global scroll_len
    canvas.configure(scrollregion=canvas.bbox("all"))
    temp_scroll = scrollbar.get()
    scroll_len = temp_scroll[1]-temp_scroll[0]
    # scrollbar.set(temp_scroll[0],temp_scroll[1])
    # canvas.yview_scroll(10, "units")
    # time.sleep(1)
    # canvas.yview_scroll(-10, "units")
    # print(prev_scroll)

params_frame.bind("<Configure>", configure_canvas)
canvas.bind("<Configure>", configure_frame)

canvas.configure(yscrollcommand=scrollbar.set)

def _on_mousewheel(event):
    global scroll_len
    curr_scroll = scrollbar.get()
    if scroll_len >= 1:
        return
    canvas.yview_scroll(-1*(event.delta), "units")
    print(curr_scroll)
    print(curr_scroll[1]-curr_scroll[0])
    # print(  (   max(min(1-scroll_len,curr_scroll[0]-event.delta),0) ,   max(min(1,curr_scroll[0]-event.delta),scroll_len) )   )
    scrollbar.set(max(min(1-scroll_len,curr_scroll[0]-event.delta),0), max(min(1,curr_scroll[0]-event.delta),scroll_len))

canvas.bind_all("<MouseWheel>", _on_mousewheel)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label "+str(i)).grid(row=i,sticky="EW")

canvas.grid(row = 1, column = 2, sticky = 'NSEW', pady = (0, 20))
# scrollable_frame.pack(expand = True) 
scrollbar.grid(row = 1, column = 3, sticky = 'NS', pady = (0, 20))

ttk.Separator(window, orient='vertical').grid(column=1, row=0, rowspan=2, sticky='NS')
ttk.Separator(window, orient='horizontal').grid(column=0, row=2, columnspan=4, sticky='NSEW')

w_frame = tk.Frame(controls_frame,name="w_frame")
w_frame.grid(row = 0, column = 1, sticky = 'S')

a_frame = tk.Frame(controls_frame,name="a_frame")
a_frame.grid(row = 1, column = 0, sticky = 'E')

s_frame = tk.Frame(controls_frame,name="s_frame")
s_frame.grid(row = 2, column = 1, sticky = 'N')

d_frame = tk.Frame(controls_frame,name="d_frame")
d_frame.grid(row = 1, column = 2, sticky = 'W')

q_frame = tk.Frame(controls_frame,name="q_frame",width=50,height=60)
q_frame.grid(row = 0, column = 0, sticky = 'SE', padx = (0,20), pady = (0,20))

e_frame = tk.Frame(controls_frame,name="e_frame",width=50,height=60)
e_frame.grid(row = 0, column = 2, sticky = 'SW', padx = (20,0), pady = (0,20))

# 'Entry' class is used to display the input-field for 'username' text label
tk.Label(w_frame,text="\u2191").grid(row = 0, column = 0)
btn_w = tk.Button(w_frame, text = "W", width = 1, height = 2, name = 'btn_w')
btn_w.grid(row = 1, column = 0)

tk.Label(a_frame,text="\u2190").grid(row = 0, column = 0)
btn_a = tk.Button(a_frame, text = "A", width = 1, height = 2, name = 'btn_a')
btn_a.grid(row = 0, column = 1)

tk.Label(s_frame,text="\u2193").grid(row = 1, column = 0)
btn_s = tk.Button(s_frame, text = "S", width = 1, height = 2, name = 'btn_s')
btn_s.grid(row = 0, column = 0)

tk.Label(d_frame,text="\u2192").grid(row = 0, column = 1)
btn_d = tk.Button(d_frame, text = "D", width = 1, height = 2, name = 'btn_d')
btn_d.grid(row = 0, column = 0)

tk.Label(q_frame,text="\u21b6",font=("Arial Unicode MS", 25)).place(relx=1,rely=1,anchor="se",y=-35,x=-10)
btn_q = tk.Button(q_frame, text = "Q", width = 1, height = 2, name = 'btn_q')
btn_q.place(relx=1,rely=1,anchor="se")

tk.Label(e_frame,text="\u21b7",font=("Arial Unicode MS", 25)).place(relx=0,rely=1,anchor="sw",y=-35,x=10)
btn_e = tk.Button(e_frame, text = "E", width = 1, height = 2, name = 'btn_e')
btn_e.place(relx=0,rely=1,anchor="sw")

e_frame.rowconfigure(0,weight=1)
e_frame.rowconfigure(1,weight=0)

movement_buttons = {'w': btn_w, 'a': btn_a, 's': btn_s, 'd': btn_d, 'q': btn_q, 'e': btn_e}

param_types = ["f","l","s","h","u","d","p"]

params = {
    "Walk": {
        "f": 0.8,
        "l": 0.15,
        "s": 0.06,
        "h": 0.15,
        "u": 0.03,
        "d": 0.03,
        "p": 0.15
    },
    "Trot": {
        "f": 0.8,
        "l": 0.15,
        "s": 0.06,
        "h": 0.15,
        "u": 0.03,
        "d": 0.03,
        "p": 0.5
    },
    "Pronk": {
        "f": 2,
        "l": 2,
        "s": 2,
        "h": 2,
        "u": 2,
        "d": 2,
        "p": 0.5
    },
    "Bound": {
        "f": 2,
        "l": 2,
        "s": 2,
        "h": 2,
        "u": 2,
        "d": 2,
        "p": 0.5
    },
}

controls_frame.columnconfigure(0,weight=1)
controls_frame.columnconfigure(1,weight=0)
controls_frame.columnconfigure(2,weight=1)
controls_frame.rowconfigure(0,weight=1)
controls_frame.rowconfigure(1,weight=0)
controls_frame.rowconfigure(2,weight=1)
# controls_frame.rowconfigure(3,weight=1)

GaitMode = tk.StringVar(window)
GaitMode.set("Walk")

tk.Label(params_frame, text="Gait").grid(row=0,column=0)
tk.OptionMenu(params_frame,GaitMode,"Walk","Trot","Pronk","Bound", "Waypoint").grid(row=0,column=1,sticky='EW',padx=(0,30),pady=(10,0))

tk.Label(params_frame, text="Frequency").grid(row=1,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=10,resolution=0.1,	
tickinterval=1, name="f").grid(row=1,column=1,sticky='EW',padx=(0,30))

tk.Label(params_frame, text="Stride Length").grid(row=2,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.2,resolution=0.01,	
tickinterval=0.05, name="l").grid(row=2,column=1,sticky='EW',padx=(0,30))

tk.Label(params_frame, text="Step Difference").grid(row=3,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.3,resolution=0.01,	
tickinterval=0.1, name="s").grid(row=3,column=1,sticky='EW',padx=(0,30))

tk.Label(params_frame, text="Stance Height").grid(row=4,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.2,resolution=0.01,	
tickinterval=0.05, name="h").grid(row=4,column=1,sticky='EW',padx=(0,30))

tk.Label(params_frame, text="Up Amplitude").grid(row=5,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.1,resolution=0.01,	
tickinterval=0.02, name="u").grid(row=5,column=1,sticky='EW',padx=(0,30))

tk.Label(params_frame, text="Down Amplitude").grid(row=6,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=0.1,resolution=0.01,	
tickinterval=0.02, name="d").grid(row=6,column=1,sticky='EW',padx=(0,30))

tk.Label(params_frame, text="Flight %").grid(row=7,column=0)
tk.Scale(params_frame,orient='horizontal',from_=0,to=1,resolution=0.05,	
tickinterval=0.2, name="p").grid(row=7,column=1,sticky='EW',padx=(0,30))

params_frame.columnconfigure(0,weight=1)
params_frame.columnconfigure(1,weight=10)
# params_frame.rowconfigure(0,weight=1)
# params_frame.rowconfigure(1,weight=1)
# params_frame.rowconfigure(2,weight=1)
# params_frame.rowconfigure(3,weight=1)
# params_frame.rowconfigure(4,weight=1)
# params_frame.rowconfigure(5,weight=1)
# params_frame.rowconfigure(6,weight=1)
# params_frame.rowconfigure(7,weight=1)

# waypoint frame
tk.Label(wp_frame, text="Initial turn in degrees").grid(row=1, column = 2, sticky = '', padx = 20)
read_x = tk.Entry(wp_frame, textvariable = x).grid(row=7, column = 2, sticky = '', padx = 20)

tk.Label(wp_frame, text="distance to move in meters").grid(row=1, column = 3, sticky = '', padx = 20)
read_d = tk.Entry(wp_frame, textvariable = f).grid(row=7, column = 3, sticky = '', padx = 20)

tk.Label(wp_frame, text="final turn in degrees").grid(row=1, column = 4, sticky = '', padx = 20)
read_y = tk.Entry(wp_frame, textvariable = y).grid(row=7, column = 4, sticky = '', padx = 20)

btn_sendwp = tk.Button(wp_frame, text = "Send Waypoint", width = 14, height = 2, name = 'btn_sendwp')
btn_sendwp.grid(row = 7, column = 5, sticky = 'W')

tk.Label(wp_frame, text="default values are all zero").grid(row=8,column=3)

def send_all_params():
    if GaitMode.get() == "Waypoint":
        return
    for (key,value) in params[GaitMode.get()].items():
        window.nametowidget("canvas.params_frame."+key).set(value)
        ser.write(str(key + ' ' + GaitMode.get()[0] + ' ' + str(value) + '\n').encode('utf-8'))
        if GaitMode.get() == "Trot":
            ser.write(str(key + ' Y ' + str(value) + '\n').encode('utf-8'))

send_all_params()

# 'Checkbutton' class is for creating a checkbutton which will take a 'columnspan' of width two (covers two columns)
# tk.Checkbutton(window, text = "Keep Me Logged In").grid(columnspan = 2) 

current_mode = []

def get_waypoint():
    _x = x.get()
    _f = f.get()
    _y = y.get()

    return _x, _f, _y

def button1_event(event=None,key=None,type_=None):
    if key:
        widget_name = "btn_" + key
        if type_ == "KeyPress":
            event_type =  "ButtonPress"
        elif type_ == "KeyRelease":
            event_type =  "ButtonRelease"
        elif type_ == "Multiple":
            event_type =  "ButtonPress"
            widget_name = key
    else:
        widget_name = str(event.widget).split(".")[-1]
        event_type = str(event.type)

    if event_type == "ButtonPress":
        if widget_name == "btn_sendwp" and GaitMode.get() == "Waypoint":
            print("SEND ", GaitMode.get(), "Forward")
            initial_turn, distance, final_turn = get_waypoint()
            print(initial_turn, distance, final_turn)
            ser.write(str('x' + ' ' + 'L' + initial_turn + ' ' + distance + ' ' + final_turn +'\n').encode('utf-8'))
            ser.write(str('L'+'\n').encode('utf-8'))
        if widget_name == "btn_w":
            current_mode.append(widget_name)
            print("SEND ", GaitMode.get(), "Forward")
            ser.write(b'r W 1\n')
            ser.write(str(GaitMode.get()[0]+'\n').encode('utf-8'))
        elif widget_name == "btn_a":
            current_mode.append(widget_name)
            # print(str('s Y -' + str(params["Trot"]["s"]) + '\r').encode('utf-8'))
            ser.write(str('s Y -' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            ser.write(b'Y\n')
            print("SEND Trot Left")
            # ser.write(b'\r')
        elif widget_name == "btn_s":
            current_mode.append(widget_name)
            print("SEND ", GaitMode.get(), "Backward")
            ser.write(b'r W -1\n')
            ser.write(str(GaitMode.get()[0]+'\n').encode('utf-8'))
        elif widget_name == "btn_d":
            current_mode.append(widget_name)
            # print(str('s Y ' + str(params["Trot"]["s"]) + '\r').encode('utf-8'))
            ser.write(str('s Y ' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            ser.write(b'Y\n')
            print("SEND Trot Right")
        elif widget_name == "btn_q":
            current_mode.append(widget_name)
            # print(str('s Y ' + str(params["Trot"]["s"]) + '\r').encode('utf-8'))
            # ser.write(str('s Y ' + str(params["Trot"]["s"]) + '\n').encode('utf-8'))
            # ser.write(b'Y\n')
            ser.write(b't W -1\n')
            ser.write(b'T\n')
            print("SEND Rotate Left")
        elif widget_name == "btn_e":
            current_mode.append(widget_name)
            # print(str('s Y ' + str(params["Trot"]["s"]) + '\r').encode('utf-8'))
            ser.write(b't W 1\n')
            ser.write(b'T\n')
            print("SEND Rotate Right")
    elif event_type == "ButtonRelease" and (widget_name == "btn_w" or widget_name == "btn_a" or widget_name == "btn_s" or widget_name == "btn_d" or widget_name == "btn_q" or widget_name == "btn_e"):
        # if type_ == "KeyRelease":
        current_mode.pop(current_mode.index(widget_name))
        if len(current_mode) > 0:
            button1_event(key=current_mode[-1],type_="Multiple")
            current_mode.pop()
        else:
            print("SEND Stop")
            ser.write(b'S\n')
    
    if event_type == "ButtonRelease":
        if widget_name in param_types:
            print("Setting ", widget_name, " to ", event.widget.get())
            params[GaitMode.get()][widget_name] = event.widget.get()
            ser.write(str(widget_name + ' ' + GaitMode.get()[0] + ' ' + str(event.widget.get()) + '\n').encode('utf-8'))
            if GaitMode.get() == "Trot":
                ser.write(str(widget_name + ' Y ' + str(event.widget.get()) + '\n').encode('utf-8'))
        elif widget_name == "!optionmenu":
            if GaitMode.get() == "Waypoint":
                print("Setting ", widget_name, " to ", GaitMode.get())
                print("parameters for waypoint are not changeable")
            else:
                print("Setting ", widget_name, " to ", GaitMode.get())
                print(params[GaitMode.get()])

was_pressed = {'w': False, 'a': False, 's': False, 'd': False, 'q': False, 'e': False}
            
def key_event(event):
    if event.char in was_pressed:
        if str(event.type) == "KeyPress" and not was_pressed[event.char]:
            was_pressed[event.char] = True
            movement_buttons[event.char].configure(state='active')
            button1_event(key=event.char,type_=str(event.type))
            # print(event.char, " ", event.type)
        elif str(event.type) == "KeyRelease":
            was_pressed[event.char] = False
            movement_buttons[event.char].configure(state='normal')
            button1_event(key=event.char,type_=str(event.type))
            # print(event.char, " ", event.type)

        

# btn_w.bind("<Button-1>",        event_w)
# btn_w.bind("<ButtonRelease-1>", event_w)

# btn_a.bind("<Button-1>",        event_a)
# btn_a.rbind("<ButtonRelease-1>", event_a)

# btn_s.bind("<Button-1>",        event_s)
# btn_s.bind("<ButtonRelease-1>", event_s)

# btn_d.bind("<Button-1>",        event_d)
# btn_d.bind("<ButtonRelease-1>", event_d)

def button_event(event):
    print(event)

# window.bind("<KeyPress>", button_event)
window.bind("<Button-1>", button1_event)
window.bind("<ButtonRelease-1>", button1_event)

window.bind("<KeyPress>", key_event)
window.bind("<KeyRelease>", key_event)

exitFlag = False

def on_exit():
    global exitFlag
    exitFlag = True
    print("Closing serial port")
    window.destroy()
    ser.close()

window.protocol("WM_DELETE_WINDOW",on_exit)
# window.mainloop()

inString = ""

while 1:
    # window.update()
    try:
        window.update()
        window.update_idletasks()
    except:
        sys.exit(0)

    if (not exitFlag and ser.in_waiting):
        c = ser.read()
        # print(inString)
        # print(chr(c))
        if (c == b'\n'):
            if ''.join(inString) == "!!!":
                print("Connected")
                time.sleep(2)
                send_all_params()
            inString = ""
        else:
            inString = inString + c.decode('utf-8')
