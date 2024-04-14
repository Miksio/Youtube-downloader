import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube

def download_video():
    url = url_entry.get()
    format_choice = format_var.get()
    if not url.strip():
        messagebox.showerror("Błąd", "Proszę wpisać prawidłowy URL.")
        return
    
    try:
        yt = YouTube(url)
        if format_choice == 'mp3':
            media = yt.streams.get_audio_only()
            file_extension = '.mp3'
        elif format_choice == 'wav':
            media = yt.streams.get_audio_only()
            file_extension = '.wav'
        elif format_choice == 'mp4':
            media = yt.streams.get_highest_resolution()
            file_extension = '.mp4'
        else:
            messagebox.showerror("Błąd", "Proszę wybrać prawidłowy format.")
            return
        
        save_path = filedialog.askdirectory()
        if save_path:
            media.download(filename=media.title + file_extension, output_path=save_path)
            messagebox.showinfo("Sukces", "Pobieranie zakończone!")
        else:
            messagebox.showerror("Błąd", "Nie wybrano folderu.")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))

# Ustawienie głównego okna aplikacji
root = tk.Tk()
root.title("Downloader filmów z YouTube")

# Ustawienie etykiety
label = tk.Label(root, text="Wprowadź URL filmu z YouTube:")
label.pack(pady=10)

# Ustawienie pola tekstowego
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Ustawienie opcji formatu
format_var = tk.StringVar()
format_var.set("mp3")  # default value
format_label = tk.Label(root, text="Wybierz format:")
format_label.pack(pady=5)
formats = [('MP3', 'mp3'), ('WAV', 'wav'), ('MP4', 'mp4')]
for text, mode in formats:
    b = tk.Radiobutton(root, text=text, variable=format_var, value=mode)
    b.pack(anchor='w')

# Ustawienie przycisku do pobierania
download_button = tk.Button(root, text="Pobierz", command=download_video)
download_button.pack(pady=20)

# Uruchomienie aplikacji
root.mainloop()
