from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root =Tk()
root.title('Musik Player')
#root.iconbitmap('C:/Users/Lenovo/Desktop/musik/images')
root.geometry("500x450")

play_btn_img = PhotoImage(file = 'images/play.png')
root.tk.call('wm', 'iconphoto', root._w, play_btn_img)

pause_btn_img = PhotoImage(file = 'images/pause.png')
root.tk.call('wm', 'iconphoto', root._w, pause_btn_img)

forward_btn_img = PhotoImage(file = 'images/forward.png')
root.tk.call('wm', 'iconphoto', root._w, forward_btn_img)

back_btn_img = PhotoImage(file = 'images/back.png')
root.tk.call('wm', 'iconphoto', root._w, back_btn_img)

stop_btn_img = PhotoImage(file = 'images/stop.png')
root.tk.call('wm', 'iconphoto', root._w, stop_btn_img)

# img = PhotoImage(file='your-icon')
#root.iconphoto(True, play_btn_img)

#initializing pygame mixer
pygame.mixer.init()

#Song length info
def play_time():
    
    #Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() /1000

    #convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    #currently playong song
    current_song = song_box.curselection()

    #Getting song title from playlist
    song = song_box.get(current_song)
    #adding info back to song
    song = f'C:/Users/Lenovo/Desktop/musik/audio/{song}'
        
    #Get song length with mutagen
    song_mut = MP3(song)

    global song_length #to use on slider function
    song_length = song_mut.info.length #this will give us length in seconds
    #convert into time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))


    #Output time to status bar
    status_bar.config(text = f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
    #status_bar.config(text = int(current_time))
    
    my_slider.config(value = int(current_time))


    #update time
    status_bar.after(1000, play_time)

#Slider Function
def slide(x):
    slider_label.config(text =f'{int(my_slider.get())} of {int(song_length)} ')

#Add song function
def add_song():
    song = filedialog.askopenfilename(initialdir= 'audio/', title = "choose the song", filetypes= (("mp3 Files", "*.mp3"), ))
    # Cutting out the directory info from song name
    song = song.replace("C:/Users/Lenovo/Desktop/musik/audio/", "")
    
    song_box.insert(END, song)

#Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir= 'audio/', title = "Choose the songs", filetypes= (("mp3 Files", "*.mp3"), ))

    #since there are many songs we cant use the insert(END) here so we use loop
    for song in songs:
        song = song.replace("C:/Users/Lenovo/Desktop/musik/audio/", "")
        
        song_box.insert(END, song)


#Removing a song
def delete_song():
    song_box.delete(ANCHOR) #delete currently selected song
    pygame.mixer.music.stop() #stop the deleted song



#Removing all songs
def delete_all_songs():
    song_box.delete(0,END) 
    pygame.mixer.music.stop() 


#play selected song

def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Lenovo/Desktop/musik/audio/{song}'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Calling the play_time function
    play_time()

    #Update slider to position
    slider_position = int(song_length)
    my_slider.config(to  = slider_position, value = 0) #value is given so that the slider starts from zero when a new song starts


#stop the current playing song
def stop():
    #pass
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE) #to unselect the stopped song

    #Clear the status bar
    status_bar.config(text ='')

def next_song():
    next_one = song_box.curselection() #returns a number in a tuple which indicates which song is currently playing
    #print(next_one)
    next_one = next_one[0] + 1
    #get the next song to play
    song = song_box.get(next_one)
    #adding directory info to song title for playing it
    song = f'C:/Users/Lenovo/Desktop/musik/audio/{song}'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0,END) #clearing the active bar from the current song
    song_box.activate(next_one) #passing it to next song, only shown by a underline
    song_box.selection_set(next_one, last = None) #It is a kind of a range function so last = None

def previous_song():
    next_one = song_box.curselection() #returns a number in a tuple which indicates which song is currently playing
    #print(next_one)
    next_one = next_one[0] - 1
    #get the next song to play
    song = song_box.get(next_one)
    #adding directory info to song title for playing it
    song = f'C:/Users/Lenovo/Desktop/musik/audio/{song}'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0,END) #clearing the active bar from the current song
    song_box.activate(next_one) #passing it to next song, only shown by a underline
    song_box.selection_set(next_one, last = None) #It is a kind of a range function so last = None

#Defining a global variable to know if the current song is paused or not
global paused
paused = False #false because initially the song is playing

#pausing and unpausing the current song
def pause(is_paused):
    global paused # changes in this value will also change the value of the upper variable as it is global variable
    paused = is_paused

    
    #Unause
    if(paused == True):
        pygame.mixer.music.unpause()
        paused = False
    else:
    #Pause
        pygame.mixer.music.pause()
        paused = True

#creating Playlist box
song_box = Listbox(root, bg = "black", fg = "green", width = 60, selectbackground= "grey", selectforeground="black")
song_box.pack(pady = 20)


#Player Control buttons
'''
play_btn_img = PhotoImage(file = 'images/play.png')
pause_btn_img = PhotoImage(file = 'images/pause.png')
forward_btn_img = PhotoImage(file = 'images/forward.png')
back_btn_img = PhotoImage(file = 'images/back.png')
stop_btn_img = PhotoImage(file = 'images/stop.png')
'''
#Player control frame
controls_frame = Frame(root)
controls_frame.pack()

#Player Control Buttons
back_button = Button(controls_frame, image = back_btn_img, borderwidth =0, command = previous_song)
forward_button = Button(controls_frame, image = forward_btn_img, borderwidth =0, command = next_song)
play_button = Button(controls_frame, image = play_btn_img , borderwidth =0, command= play)
pause_button = Button(controls_frame, image = pause_btn_img , borderwidth =0, command =lambda: pause(paused)) #to pass a variable into a button we have to use lambda function
stop_button =Button (controls_frame, image = stop_btn_img, borderwidth =0, command = stop)

back_button.grid(row = 0, column = 0, padx =10)
forward_button.grid(row = 0, column = 1,padx =10)
play_button.grid(row = 0, column = 2, padx =10)
pause_button.grid(row = 0, column = 3, padx =10)
stop_button.grid(row = 0, column = 4, padx =10)


# Creating Menu
my_menu = Menu(root)
root.config(menu = my_menu)


#Add songs menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Add Songs", menu = add_song_menu)
add_song_menu.add_command(label = "Add a song to your playlist", command = add_song)


#Add many songs
add_song_menu.add_command(label = "Add many songs to your playlist", command = add_many_songs)

#Deleting songs from the playlist
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Delete songs", menu = remove_song_menu)
remove_song_menu.add_command(label ="Remove this song", command = delete_song)

remove_song_menu.add_command(label = "Remove all songs", command = delete_all_songs)


#status bar
status_bar = Label(root, text ='', bd =1, relief = GROOVE, anchor = E)
status_bar.pack(fill =X, side = BOTTOM, ipady=2)


#Music Slider
my_slider = ttk.Scale(root, from_= 0, to = 100, orient =HORIZONTAL, value = 0, command = slide, length = 360)
my_slider.pack(pady = 20)

#Create Temp slider label
slider_label = Label(root, text ="0")
slider_label.pack(pady = 10)

root.mainloop()