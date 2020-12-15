"""
musicplayer module

Simple music player that requires pygame and tkinter.

Mutagen is also needed for dealing with some of the audio file data like song
length.

"""

import time
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk

import mutagen.mp3
import pygame

root = Tk()
root.title('MP3 Player')
root.configure(background="black")
#root.iconbitmap('file/path.ico')
root.geometry('500x420')

# Initialize Pygame Mixer
pygame.mixer.init()

# Song Dictionary for name in list as key and file path as value.
SONG_DICT = {}
global PLAYING_SONG
PLAYING_SONG = ''
global AUTO_PLAY
AUTO_PLAY = False
global STOPPED
STOPPED = False
global PAUSED
PAUSED = False

# Get Song Length Time Info
def song_time():
    # Stop this looping function if music has been stopped
    global AUTO_PLAY
    global STOPPED
    global PAUSED
    if STOPPED or PAUSED:
        return
    global PLAYING_SONG
    current_time = pygame.mixer.music.get_pos() / 1000
    # Convert to time format
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    # Load Song into Mutagen MP3 class
    song_mut = mutagen.mp3.MP3(PLAYING_SONG)
    # Get the song length
    song_length = song_mut.info.length
    # Convert song length time to Time Format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Elapsed Time: {converted_song_length} / {converted_song_length}  ')
        if AUTO_PLAY:
            next_song()
    elif PAUSED:
        pass
    elif int(my_slider.get()) == int(current_time):
        # Update Slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
        # update time every second while song is playing
        status_bar.after(1000, song_time)
    else:
        # Update Sliter To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # convert to time format
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Elapsed Time: {converted_current_time} / {converted_song_length}  ')

        # Move this thing along by one second
        next_time =  int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        # update time every second while song is playing
        status_bar.after(1000, song_time)

    # Update slider position on button release
    #my_slider.bind("<ButtonRelease-1>", my_slider.config(from_=0, to=pygame.mixer.music.get_pos() / 1000, value=current_time))


# Add Song Function
def add_song():
    path = filedialog.askopenfilename(initialdir='C:/Users/dkdan/Music/',
                                      title="Choose A Song",
                                      filetypes=(("mp3 Files", "*.mp3"), ))
    song=path.split('.')[0]
    song=song.split('/')[-1]
    song_list.insert(END, song)
    SONG_DICT[song] = path


# Add Many Songs Function
def add_many_songs():
    paths = filedialog.askopenfilenames(initialdir='C:/Users/dkdan/Music/',
                                      title="Choose A Song",
                                      filetypes=[("mp3 Files", "*.mp3"), 
                                                ("FLAC audio", "*.flac"),])
    # Loop through song list
    for path in paths:
        song=path.split('.')[0]
        song=song.split('/')[-1]
        song_list.insert(END, song)
        SONG_DICT[song] = path


# Delete a Song
def delete_song():
    song = song_list.get(ACTIVE)
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()
    try:
        del SONG_DICT[song]
    except KeyError:
        pass


# Delete all songs from the list
def delete_all_songs():
    stop()
    global SONG_DICT
    song_list.delete(0, END)
    pygame.mixer.music.stop()
    del SONG_DICT
    SONG_DICT = {}


def start_play(path):
    global PLAYING_SONG
    PLAYING_SONG = path
    # Load Song into Mutagen MP3 class for song frequency
    mp3_mut = mutagen.mp3.MP3(PLAYING_SONG)
    # Clear everything for start of new song
    # Clear the status bar
    status_bar.config(text='')
    # Reset Slider
    my_slider.config(value=0)
    # Load the song frequency so it plays at correct pace
    pygame.mixer.init(frequency=mp3_mut.info.sample_rate)
    # Helper function to take given path and play and start song_time loop
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops=0)

    # Call the play_time function
    song_time()


# Play Selected Song
def play():
    global STOPPED
    STOPPED = False
    global PAUSED
    PAUSED = False
    song = song_list.get(ACTIVE)
    path = SONG_DICT.get(song)
    start_play(path)


# Stop Playing Current Song
def stop():
    # Clear the status bar
    status_bar.config(text='')
    # Reset Slider
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    # Clear the list box
    song_list.selection_clear(ACTIVE)
    global STOPPED
    STOPPED = False
    global PAUSED
    PAUSED = False


# Play the Next Song in the playlist
def next_song():
    global STOPPED
    STOPPED = False
    global PAUSED
    PAUSED = False
    # Get the current song tuple number
    next_one = song_list.curselection()
    # If we are on last song, go to first song of list
    if (next_one[0]+1) == song_list.size():
        next_one = 0
    else:
        # Add one to the current song number
        next_one = next_one[0] + 1
    song = song_list.get(next_one)
    path = SONG_DICT.get(song)
    start_play(path)
    # Clear active bar in playlist
    song_list.selection_clear(0, END)
    # Highlight next song in playlist
    song_list.activate(next_one)
    # Set Active Bar to next song
    song_list.selection_set(next_one, last=None)


# Play the Previous Song in the playlist
def prev_song():
    global STOPPED
    STOPPED = False
    global PAUSED
    PAUSED = False
    # Get the current song tuple number
    prev_one = song_list.curselection()
    # If we are on the first song, go to the last song of the list
    if prev_one[0] == 0:
        prev_one = song_list.size() - 1
    else:
        # Add one to the current song number
        prev_one = prev_one[0] - 1
    song = song_list.get(prev_one)
    path = SONG_DICT.get(song)
    start_play(path)
    # Clear active bar in playlist
    song_list.selection_clear(0, END)
    # Highlight next song in playlist
    song_list.activate(prev_one)
    # Set Active Bar to next song
    song_list.selection_set(prev_one, last=None)


# Pause and Resume Music
def pause(is_paused):
    global PAUSED
    PAUSED = is_paused

    if PAUSED:
        pygame.mixer.music.unpause()
        PAUSED = False
        song_time()
    else:    
        pygame.mixer.music.pause()
        PAUSED = True


def toggle():
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    to toggle auto play
    '''
    global AUTO_PLAY
    if AUTO_PLAY == True:
        autoplay_btn.config(bg='red')
        AUTO_PLAY = False
    else:
        autoplay_btn.config(bg='green')
        AUTO_PLAY = True

autoplay_btn = Button(text="AUTOPLAY", width=12, command=toggle,
                        bg='red')
autoplay_btn.pack(pady=10)


# Create Slider Function
def slide(x):
    global PLAYING_SONG
    pygame.mixer.music.load(PLAYING_SONG)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Create Playlist Box
song_list = Listbox(root, activestyle=NONE, bg="black", fg="green", width=60,
                    selectbackground="gray", selectforeground="blue")
song_list.pack(pady=20)

# Define Player Control Button Images
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')

# Create Player Control Frames
controls_frame = Frame(root, bg="black")
controls_frame.pack()

# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0,
                     command=prev_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0,
                     command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0,
                     command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0,
                     command=lambda: pause(PAUSED))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0,
                     command=stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
# Add Many Songs
add_song_menu.add_command(label="Add Many Songs to Playlist",
                            command=add_many_songs)
# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist",
                            command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist",
                            command=delete_all_songs)


# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Create Music Position Slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0,
                    command=slide, length=300)
my_slider.pack(pady=30)


root.mainloop()
