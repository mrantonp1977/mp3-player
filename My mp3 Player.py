from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from tkinter import ttk


root = Tk()
root.title("Mp3 Player")
root.geometry("1100x900",)
root.config(background="#FE527D")
icon = PhotoImage(file="play1.png")
root.iconphoto(True, icon)

name_label = Label(root, text="Papaioannou Antonis", font=("impact",20),fg="#C50AAC", bd=8, background="#1BDED0", relief=GROOVE, anchor=CENTER)
name_label.pack(side=TOP,fill=X, ipady=15)

name_label1 = Label(root, text="",fg="#C50AAC", bd=8, background="#1BDED0", relief=GROOVE, anchor=CENTER)
name_label1.pack(side=LEFT,fill=Y, ipady=15)

name_label2 = Label(root, text="",fg="#C50AAC", bd=8, background="#1BDED0", relief=GROOVE, anchor=CENTER)
name_label2.pack(side=RIGHT,fill=Y, ipady=15)







pygame.mixer.init()

current_song_name = ""



def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000

    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))


    current_song = song_box.curselection()

    song = song_box.get(ACTIVE)
    song = f'C:/Users/mrant/Music/My music/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f"Time Elapsed   {converted_song_length}  ",
                          background="#D8D905")

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))

        status_bar.config(text=f"Now Playing......     {current_song_name}       \nTime Elapsed......           {converted_current_time}   of   {converted_song_length}         ",
                          background="#1BDED0", font=("arial black", 13), foreground="#C207B1")

        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)


    status_bar.after(1000, play_time)


def add_song():

    song = filedialog.askopenfilename(initialdir="C:/Users/mrant/Music/My music/", title="Choose A Song", filetypes=(("mp3 files", ".mp3"), ))
    song = song.replace("C:/Users/mrant/Music/My music/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def add_many_songs():

    songs = filedialog.askopenfilenames(initialdir="C:/Users/mrant/Music/My music/", title="Choose A Song", filetypes=(("mp3 files", ".mp3"), ))
    for song in songs:
        song = song.replace("C:/Users/mrant/Music/My music/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)



def play():
    global stopped, current_song_name
    stopped = False
    song = song_box.get(ACTIVE)
    current_song_name = song
    song = f'C:/Users/mrant/Music/My music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    update_volume_slider()
    play_time()



global stopped
stopped = False
def stop():
    status_bar.config(text="")
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text="")

    global stopped
    stopped = True

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False

    else:
        pygame.mixer.music.pause()
        paused = True

def next_song():
    status_bar.config(text="")
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/Users/mrant/Music/My music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)

    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

def previous_song():
    status_bar.config(text="")
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'C:/Users/mrant/Music/My music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)

    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()


def slide(x):
    song = song_box.get(ACTIVE)
    song = f'C:/Users/mrant/Music/My music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

current_volume = 0.4



def volume(x):
    global current_volume
    current_volume = float(volume_slider.get())
    pygame.mixer.music.set_volume(current_volume)
    volume_label.config(text=f"Volume \n{int(current_volume * 100)}")

def update_volume_slider():
    volume_slider.set(current_volume)


# create a master frame
master_frame = Frame(root, background="#FE527D")
master_frame.pack(pady=20)

#create playlist box

song_box = Listbox(master_frame, bg="black", fg="#2BBA0B",font=("arial", 13), width=75, height=20, selectbackground="#F6E405", selectforeground="black")
song_box.grid(row=0, column=0)

#define player control button images

previous_btn_img = PhotoImage(file="previous1.png")
next_btn_img = PhotoImage(file="next1.png")
play_btn_img = PhotoImage(file="play1.png")
pause_btn_img = PhotoImage(file="pause1.png")
stop_btn_img = PhotoImage(file="stop1.png")



# create volume label frame
volume_frame = LabelFrame(master_frame, background="#FE527D")
volume_frame.grid(row=0, column=1, padx=20, pady=10)


volume_label = Label(volume_frame, text="Volume 100", foreground="#EEEB14", background="#FE527D", font=("impact", 13))
volume_label.pack(pady=20)


controls_frame = Frame(master_frame, background="#FE527D")
controls_frame.grid(row=2, column=0, pady=50)


#create player controls Buttons

previous_btn = Button(controls_frame, image=previous_btn_img, borderwidth=0, command=previous_song)
next_btn = Button(controls_frame, image=next_btn_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

previous_btn.grid(row=0, column=0, padx=30)
next_btn.grid(row=0, column=4, padx=30)
play_btn.grid(row=0, column=1, padx=30)
pause_btn.grid(row=0, column=2, padx=30)
stop_btn.grid(row=0, column=3, padx=30)


#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

open_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Open File", menu=open_menu)
open_menu.add_command(label="Add  Song ", command=add_song, font=("arial black", 10), foreground="#066495")
open_menu.add_command(label="Add Many Songs ", command=add_many_songs, font=("arial black", 10), foreground="#066495")
open_menu.add_command(label="Delete  Song  ", command=delete_song, font=("arial black", 10), foreground="#066495")
open_menu.add_command(label="Delete All Songs ", command=delete_all_songs, font=("arial black", 10), foreground="#066495")






status_bar = Label(root, text="", bd=8, background="#1BDED0", relief=GROOVE, anchor=CENTER)
status_bar.pack(fill=X, side=BOTTOM, ipady=20)





#create slider

my_slider = ttk.Scale(master_frame,from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=650)
my_slider.grid(row=1, column=0, pady=30)




# create volume slider

volume_slider = ttk.Scale(volume_frame,from_=1, to=0, orient=VERTICAL, value=0.4, command=volume, length=290)
volume_slider.pack(pady=8, padx=25)
update_volume_slider()



root.mainloop()


