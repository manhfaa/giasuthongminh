import asyncio
import playsound
import os
import speech_recognition as sr
from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import speech_recognition as sr
import pyaudio
import keyboard

recognizer = sr.Recognizer()
client = OpenAI(api_key="sk-J3vEsFqZXfrV6UtUPCVTYYgfTzUdAr7lrqmhAxO3xDkGOLyL",
                              base_url="https://api.chatanywhere.tech/v1")

def render_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Tôi là học sinh của bạn, bạn là gia sư của tôi. Bạn tên là Văn. Bạn chỉ có thể nói những thứ liên quan đến bài học. Với những câu hỏi trắc nghiệm thì bạn sẽ phải phân tích và gửi lại đáp án đúng nhất. Đối với câu hỏi tự luận, bạn phải phân tích bài và đưa ra các cách giải đúng và chính xác. Bạn có thể trả lời được mọi bài học, đối với những hình ảnh, bạn phải xác nhận được thông tin trong ảnh là gì và đưa ra được câu trả lời chính xác."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def SEND(event=None):
    data = entry.get()
    result = render_answer(data)
    text_area.config(state='normal')  # Enable the text area
    text_area.delete(1.0, tk.END)  # Clear the text area
    text_area.insert(tk.END, f" {result}\n")
    text_area.config(state='disabled')  # Disable the text area again
    entry.delete(0, tk.END)

def record_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=3)  # Set timeout to 4 seconds
        try:
            spoken_text = recognizer.recognize_google(audio, language="vi-VN")
            entry.insert(tk.END, spoken_text)
        except sr.UnknownValueError:
            print("Không thể hiểu được giọng nói của bạn. Vui lòng thử lại!")

def play_audio(text):
    tts = gtts.gTTS(text=text, lang='vi',)
    tts.save("output.mp3")
    playsound.playsound("output.mp3")
    os.remove("output.mp3")

def mic_button_clicked():
    record_audio()

def play_button_clicked():
    play_audio(text_area.get("1.0", tk.END))

def on_button_hover(event):
    event.widget.config(relief="ridge")

def on_button_leave(event):
    event.widget.config(relief="flat")

screen = tk.Tk()
screen.geometry("600x500")
screen.title("Ứng dụng Gia Sư Thông Minh")
screen.iconbitmap("icon.ico")

# Load ảnh
image = Image.open("giaovvien.png")
image = image.resize((100, 100))  # Chỉnh kích thước hình ảnh xuống 100x100
photo = ImageTk.PhotoImage(image)

# Hiển thị ảnh
image_label = tk.Label(screen, image=photo)
image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

entry_label = tk.Label(screen, text="Nhập dữ liệu:")
entry_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry = tk.Entry(screen, width=50)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Load ảnh nút
send_image = Image.open("SEND.png")
send_image = send_image.resize((100, 30))  # Chỉnh kích thước hình ảnh xuống 30x30
send_photo = ImageTk.PhotoImage(send_image)

mic_image = Image.open("MIC.png")
mic_image = mic_image.resize((100, 30))  # Chỉnh kích thước hình ảnh xuống 30x30
mic_photo = ImageTk.PhotoImage(mic_image)

play_image = Image.open("SOUND.png")
play_image = play_image.resize((100, 30))  # Chỉnh kích thước hình ảnh xuống 30x30
play_photo = ImageTk.PhotoImage(play_image)

button_frame = tk.Frame(screen)
button_frame.grid(row=1, column=2, padx=10, pady=10)

send_button = tk.Button(button_frame, image=send_photo, command=SEND)
send_button.image = send_photo
send_button.pack(side=tk.TOP, pady=5)
send_button.bind("<Enter>", on_button_hover)
send_button.bind("<Leave>", on_button_leave)

mic_button = tk.Button(button_frame, image=mic_photo, command=mic_button_clicked)
mic_button.image = mic_photo
mic_button.pack(side=tk.TOP, pady=5)
mic_button.bind("<Enter>", on_button_hover)
mic_button.bind("<Leave>", on_button_leave)

play_button = tk.Button(button_frame, image=play_photo, command=play_button_clicked)
play_button.image = play_photo
play_button.pack(side=tk.TOP, pady=5)
play_button.bind("<Enter>", on_button_hover)
play_button.bind("<Leave>", on_button_leave)

info_label = tk.Label(screen, text="", wraplength=400)
info_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")

text_area = scrolledtext.ScrolledText(screen, width=60, height=10)
text_area.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
text_area.config(state='normal')  # Enable the text area

screen.mainloop()