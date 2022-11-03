import tkinter as tk
from tkinter import ttk
import pytube
from pytube.cli import on_progress



def downloader():

    file_types = {"mp4":22 , "mp3":251}

    #get link
    link = url_entry.get()
    #get file format
    format = file_entry.get()

    yt = pytube.YouTube(link)
    stream = yt.streams.get_by_itag(file_types[format])
    stream.download()
    


root = tk.Tk()
root.title("YT Downloader")

root_width = 400
root_height = 400

#get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#find the center of the screen
center_x = int(screen_width/2 - root_width/2)
center_y = int(screen_height/2 - root_height/2)

#relocate root at the center of the screen
root.geometry(f"{root_width}x{root_height}+{center_x}+{center_y}")

#remove minimise and maximise capabilities from the window
root.resizable(False , False)


root.iconbitmap(r"C:\Users\Prabath H\Desktop\Deeshon\Python\project\pythontutorial-1-150x150.ico")

img = tk.PhotoImage(file = r"C:\Users\Prabath H\Desktop\Deeshon\Python\project\rsz_img.png")
image_label = ttk.Label(root , 
                            image = img,
                            text = "YouTube Video Downloader",
                            compound = "top"
    )
image_label.pack()





#store url
url = tk.StringVar()
file = tk.StringVar()

# download frame
download = ttk.Frame(root)
download.pack(padx=10, pady=10, fill='x', expand=True)
   

#url
url_lable = ttk.Label(download , text = "YouTube Video Link ")
url_lable.pack(expand = True)

url_entry = ttk.Entry(download , textvariable = "text")
url_entry.pack(fill = "x" , expand = True)
url_entry.focus()
  
#file
file_label = ttk.Label(download , text = "File Type(mp4/mp3) ")
file_label.pack()

file_entry = ttk.Entry(download , text = "text1")
file_entry.pack()  


#download button
download_button = ttk.Button(root , text = "Download" , command=downloader)
download_button.pack(ipadx=5 , ipady=5)



root.mainloop()