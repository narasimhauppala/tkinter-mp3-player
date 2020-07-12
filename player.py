from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Music Player")
root.iconbitmap('images/logo.ico')
root.geometry("500x400")

pygame.mixer.init()

song_length = 0


def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000

    # temp label
    # slider_label.config(
    # text=f'Slider: {int(slider_.get())} and Song Pos: {int(current_time)}')

    convert_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    current_song = song_box.curselection()
    # print(next_one)
    song = song_box.get(ACTIVE)
    song = f'C:/Users/SAINA/Downloads/{song}.mp3'
    # Song Length
    global song_length
    song_mut = MP3(song)
    song_length = song_mut.info.length
    convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(slider_.get()) == int(song_length):
        status_bar.config(text=f'{convert_song_length}   ')
    elif paused:
        pass
    elif int(slider_.get()) == int(current_time):
        # slider not moved
        # Slider Pos
        slider_position = int(song_length)
        slider_.config(to=slider_position, value=int(current_time))

    else:
        # slider moved
        # Slider Pos
        slider_position = int(song_length)
        slider_.config(to=slider_position, value=int(slider_.get()))

        convert_time = time.strftime(
            '%H:%M:%S', time.gmtime(int(slider_.get())))

        status_bar.config(text=f'{convert_time} || {convert_song_length}   ')
        next_time = int(slider_.get()) + 1
        slider_.config(value=next_time)

    #status_bar.config(text=f'{convert_time} || {convert_song_length}   ')
    slider_.config(value=int(current_time))

    # Update Time
    status_bar.after(1000, play_time)

# End Of play Time



def add_song():
    song = filedialog.askopenfilename(
        initialdir="audio/", title="Choose a Song", filetypes=(('mp3 Files', '*.mp3'),))
    song = song.replace("C:/gui/audio/", "")
    song = song.replace("C:/Users/SAINA/Downloads/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

# Play Audio


def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/SAINA/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Call Play_time
    play_time()

    # slider_position = int(song_length)
    # slider_.config(to=slider_position, value=0)

global stopped 
stopped = True


def stop():
    # Rest To Init
    status_bar.config(text="")
    slider_.config(value=0)
    # Stop from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text="")
    # stop var 
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


def add_many_songs():
    songs = filedialog.askopenfilenames(
        initialdir="audio/", title="Choose a Song", filetypes=(('mp3 Files', '*.mp3'),))
    # Loop over songs
    for song in songs:
        song = song.replace("C:/gui/audio/", "")
        song = song.replace("C:/Users/SAINA/Downloads/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)


def next_song():
    # Rest To Init
    status_bar.config(text="")
    slider_.config(value=0)
    next_one = song_box.curselection()
    # print(next_one)
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/Users/SAINA/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.select_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


def previous_song():
    # Rest To Init
    status_bar.config(text="")
    slider_.config(value=0)
    next_one = song_box.curselection()
    # print(next_one)
    next_one = next_one[0]-1
    song = song_box.get(next_one)
    song = f'C:/Users/SAINA/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.select_clear(0, END)
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
    # slider_label.config(text=f'{int(slider_.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/SAINA/Downloads/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider_.get()))


# Create PlayList
song_box = Listbox(root, bg="black", fg="green", width=60,
                   selectbackground="gray", selectforeground="white")
song_box.pack(pady=20)

# Create Player Controls
back_btn_img = PhotoImage(file="images/back50.png")
forward_btn_img = PhotoImage(file="images/forward50.png")
play_btn_img = PhotoImage(file="images/play50.png")
pause_btn_img = PhotoImage(file="images/pause50.png")
stop_btn_img = PhotoImage(file="images/stop50.png")

# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()


# Buttons
back_button = Button(controls_frame, image=back_btn_img,
                     borderwidth=0, command=previous_song)
forward_btn = Button(controls_frame, image=forward_btn_img,
                     borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img,
                  borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img,
                   borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img,
                  borderwidth=0, command=stop)


# Grid
back_button.grid(row=0, column=0, padx=10)
forward_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0, column=4, padx=10)


# Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Songs Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song", command=add_song)
# Add Many Songs
add_song_menu.add_command(label="Add many Song", command=add_many_songs)

# Delete Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Song", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a Song", command=delete_song)
remove_song_menu.add_command(
    label="Delete all Songs", command=delete_all_songs)

# Status bar

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor='se')
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# slider
slider_ = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL,
                    value=0, command=slide, length=360)
slider_.pack(pady=30)

# slider label
#slider_label = Label(root, text="0")
# slider_label.pack(pady=10)

root.mainloop()
