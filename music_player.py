import io
import time
from pathlib import Path
from tkinter import *
from tkinter import filedialog

import cairosvg
import eyed3
import pygame
from PIL import Image, ImageTk
from mutagen.flac import FLAC
# from colorthief import ColorThief

root = Tk()
root.title("MusicPlayer")
root.geometry("700x350")
root.resizable(0, 0)
root["background"] = "#1b1b1b"

# frame
titleframe = Frame(root, bg="#1b1b1b")
titleframe.pack(pady=20, padx=(130, 0))

control = Frame(root, bg="#1b1b1b")
control.pack(pady=20)

song = ""


def add_song():
    global song
    # add song
    song = filedialog.askopenfilename(
        title="Songs",
        filetypes=(
            ("file mp3", "*.mp3"),
            ("file flac", "*.flac"),
        ),
    )

    # pick song image from metadata
    tempimage = ""
    if Path(song).suffix == ".mp3":

        audio_file = eyed3.load(song)
        # album_name = audio_file.tag.album
        # artist_name = audio_file.tag.artist

        for im in audio_file.tag.images:
            image_file = open("cover.jpg", "wb")

            image_file.write(im.image_data)
            image_file.close()

            tempimage = "cover.jpg"

    else:
        cover = FLAC(song).pictures
        for p in cover:
            if p.type == 3:  # front cover
                with open("cover.jpg", "wb") as f:
                    f.write(p.data)
        tempimage = "cover.jpg"

    photo = ImageTk.PhotoImage(Image.open(tempimage).resize((200, 200)))
    # color_thief = ColorThief("cover.jpg")
    # dominant_color = color_thief.get_color(quality=1)
    # rgb_to_hex = "#%00x%00x%00x" % dominant_color
    img_label = Label(control, image=photo, borderwidth=7)  # , bg=rgb_to_hex)
    img_label.image = photo
    img_label.grid(row=1, column=1, padx=(0, 55))

    path = Path(song)
    pathwt = path.name.replace(".mp3", "").replace(".flac", "")
    songname_label.config(
        text=pathwt, bg="#1b1b1b", fg="white", font=("Arial Rounded MT Bold", 16)
    )


# menu
menu = Menu(root)
root.config(menu=menu)

song_menu = Menu(root, tearoff=0)
menu.add_cascade(label="Songs", menu=song_menu)
song_menu.add_command(label="add song", command=add_song)


# song function
def playmusic():
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    stime()


def stopmusic():
    pygame.mixer.music.stop()


paused = False


def pausemusic(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False

    else:
        pygame.mixer.music.pause()
        paused = True


# status bar
def stime():
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))
    status_bar.config(text=converted_current_time)

    status_bar.after(1000, stime)


status_bar = Label(root, text="Time", bg="#1b1b1b", fg="white")
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# buttons images

image_data = cairosvg.svg2png(url="images/play.svg")
image = Image.open(io.BytesIO(image_data))

play_button_image = ImageTk.PhotoImage(image.resize((100, 100)))

image2_data = cairosvg.svg2png(url="images/pause.svg")
image2 = Image.open(io.BytesIO(image2_data))
pause_button_image = ImageTk.PhotoImage(image2.resize((100, 100)))

image3_data = cairosvg.svg2png(url="images/stop.svg")
image3 = Image.open(io.BytesIO(image3_data))
stop_button_image = ImageTk.PhotoImage(image3.resize((100, 100)))

play_button = Button(
    control,
    text="play",
    image=play_button_image,
    borderwidth=0,
    command=playmusic,
    font=("Arial Rounded MT Bold", 16),
    bg="#1b1b1b",
    fg="white",
)
pause_button = Button(
    control,
    text="pause",
    image=pause_button_image,
    borderwidth=0,
    command=lambda: pausemusic(paused),
    font=("Arial Rounded MT Bold", 16),
    bg="#1b1b1b",
    fg="white",
)
stop_button = Button(
    control,
    text="stop",
    image=stop_button_image,
    borderwidth=0,
    command=stopmusic,
    font=("Arial Rounded MT Bold", 16),
    bg="#1b1b1b",
    fg="white",
)

play_button.grid(row=1, column=2, padx=15)
pause_button.grid(row=1, column=3, padx=15)
stop_button.grid(row=1, column=4, padx=15)

songname_label = Label(titleframe, bg="#1b1b1b", fg="white")
songname_label.grid(row=0, column=6)

root.mainloop()
