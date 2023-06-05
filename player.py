import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import os
from tkinter import ttk
from mutagen.mp3 import MP3

root = Tk()
root.title("Shu Music Player")
root.geometry("485x700+290+0")
root.configure(background="#333333")
root.resizable(False, False)  # window won't be resizable
mixer.init()

def toggle_mute():
    if mixer.music.get_volume() == 0.0:
        # If music is already muted, unmute it
        mixer.music.set_volume(1.0)
        mute_button.config(text="Mute")
    else:
        # Mute the music
        mixer.music.set_volume(0.0)
        mute_button.config(text="Unmute")

def AddMusic():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                Playlist.insert(END, song)

def PlayMusic():
    Music_Name = Playlist.get(ACTIVE)
    print(Music_Name[0:-4])
    mixer.music.load(Playlist.get(ACTIVE))
    mixer.music.play()

def stop_music(event=None):
    mixer.music.stop()

def toggle_play_pause(event=None):
    if mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()

def play_next(event=None):
    current_index = Playlist.curselection()
    next_index = current_index[0] + 1
    if next_index < Playlist.size():
        Playlist.selection_clear(0, END)
        Playlist.selection_set(next_index)
        Playlist.activate(next_index)
        PlayMusic()

def play_previous(event=None):
    current_index = Playlist.curselection()
    previous_index = current_index[0] - 1
    if previous_index >= 0:
        Playlist.selection_clear(0, END)
        Playlist.selection_set(previous_index)
        Playlist.activate(previous_index)
        PlayMusic()

# icon
lower_frame = Frame(root, bg='white', width=485, height=180)
lower_frame.place(x=0, y=400)

image_icon = PhotoImage(file="logo.png")
root.iconphoto(False, image_icon)

frameCnt = 30
frames = [PhotoImage(file="aa1.gif", format='gif -index %i' % i) for i in range(frameCnt)]

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(40, update, ind)

label = Label(root)
label.place(x=0, y=0)
root.after(0, update, 0)

# button
ButtonPlay = PhotoImage(file="play.png")
Button(root, image=ButtonPlay, bg="white", bd=0, height=60, width=60, command=PlayMusic).place(x=215, y=487)

ButtonStop = PhotoImage(file="stop.png")
Button(root, image=ButtonStop, bg="white", bd=0, height=60, width=60, command=stop_music).place(x=130, y=487)

Buttonvolume = PhotoImage(file="volume.png")
Button(root, image=Buttonvolume, bg="#FFFFFF", bd=0, height=60, width=60, command=toggle_mute).place(x=20, y=487)

ButtonPause = PhotoImage(file="pause.png")
Button(root, image=ButtonPause, bg="white", bd=0, height=60, width=60, command=toggle_play_pause).place(x=300, y=487)
"""
ButtonNext = PhotoImage(file="next.png")
Button(root, image=ButtonNext, bg="white", bd=0, height=60, width=60, command=play_next).place(x=385, y=487)

ButtonPrevious = PhotoImage(file="previous.png")
Button(root, image=ButtonPrevious, bg="white", bd=0, height=60, width=60, command=play_previous).place(x=470, y=487)
"""
menu = PhotoImage(file="menu.png")
Label(root, image=menu).place(x=0, y=580, width=485, height=100)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=0, y=585, width=485, height=100)

Button(root, text="Browse Music", width=60, height=1, font=('calibri', 12, 'bold'), fg="Black", bg="lightblue",
       command=AddMusic).place(x=0, y=555)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="grey",
                   selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)

Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)

# Bind keyboard shortcuts
root.bind("<KeyPress-space>", toggle_play_pause)  # Bind spacebar to toggle play/pause
root.bind("<KeyPress-s>", stop_music)  # Press 's' to stop
root.bind("<KeyPress-n>", play_next)  # Press 'n' to play next
root.bind("<KeyPress-p>", play_previous)  # Press 'p' to play previous
root.bind("<KeyPress-m>",toggle_mute)
# Progress bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=484, mode='determinate')
progress_bar.place(x=0, y=461)

def update_progress():
    if mixer.music.get_busy():
        current_position = mixer.music.get_pos() / 1000  # Current position in seconds
        song_length = MP3(Playlist.get(ACTIVE)).info.length  # Song length in seconds
        progress = (current_position / song_length) * 100  # Calculate progress percentage
        progress_bar['value'] = progress
    else:
        progress_bar['value'] = 0

    # Schedule the next update
    root.after(1000, update_progress)

# Update progress bar
update_progress()

root.mainloop()
