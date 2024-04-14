import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytube import YouTube

def show_progress(stream, chunk, bytes_remaining):
    # Aktualizacja paska postępu
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion
    progress_label.config(text=f"Pobrane {int(percentage_of_completion)} %")
    root.update_idletasks()

def download_video():
    url = url_entry.get()
    format_choice = format_var.get()
    if not url.strip():
        messagebox.showerror("Błąd", "Proszę wpisać prawidłowy URL.")
        return
    
    try:
        yt = YouTube(url, on_progress_callback=show_progress)
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
            progress_bar['value'] = 0  # Reset the progress bar after download
            progress_label.config(text="Pobrane 0%")  # Reset progress label
        else:
            messagebox.showerror("Błąd", "Nie wybrano folderu.")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))
        progress_bar['value'] = 0
        progress_label.config(text="Pobrane 0%")

# main application window
root = tk.Tk()
root.title("Downloader filmów z YouTube")

# label
label = tk.Label(root, text="Wprowadź URL filmu z YouTube:")
label.pack(pady=10)

#text field settings
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# format settings
format_var = tk.StringVar()
format_var.set("mp3")  # default value
format_label = tk.Label(root, text="Wybierz format:")
format_label.pack(pady=5)
formats = [('MP3', 'mp3'), ('WAV', 'wav'), ('MP4', 'mp4')]
for text, mode in formats:
    b = tk.Radiobutton(root, text=text, variable=format_var, value=mode)
    b.pack(anchor='w')

    # Set up a progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=20)
progress_label = tk.Label(root, text="Pobrane 0%")
progress_label.pack(pady=5)

# download button
download_button = tk.Button(root, text="Pobierz", command=download_video)
download_button.pack(pady=20)


root.mainloop()
