from tkinter import *
from PIL import ImageTk, Image
from win32api import GetSystemMetrics
import os
import rank
import webbrowser

def result_page(root,query):
    window = Toplevel(root)
    window.configure(background="white")
    window.title("Result")
    #window.geometry(str(GetSystemMetrics(0)) + 'x' + str(GetSystemMetrics(1)))
    window.attributes('-fullscreen', True)
    output,doc = rank.main(query)
    root.withdraw()
    link = [doc[i]["Link"] for i in output]
    print(link)
    frame = Frame(window, bg="white")
    frame.pack()
    for i in range(len(output)):
        url = link[i]
        Button(frame, text=output[i], height=10, width=45, bg = "white", font ="Helvetica 12 bold", command =  lambda url = url:  webbrowser.open_new(url)).grid(row = int(i/3), column = i%3)
    window.mainloop()

def query_page():
    root = Tk()
    root.configure(background = "white")
    root.attributes('-fullscreen', True)
    #root.geometry(str(GetSystemMetrics(0))+'x'+str(GetSystemMetrics(1)))
    frame = Frame(root)
    frame.pack(pady=50)
    frame2 = Frame(root, bg = "white")
    frame2.pack(pady=20)
    root.title("Search Store")
    img = ImageTk.PhotoImage(Image.open(r"C:\Users\User\Desktop\IR\Package\unnamed.png"))
    panel = Label(frame, image = img,bg = "white")
    panel.pack(side = "left", fill = "both", expand="yes")
    text =  Entry(frame2, bg="white", width=50,  font ="Helvetica 20 bold")
    text.pack(ipady=3, side="left")
    img2 = ImageTk.PhotoImage(Image.open(r"C:\Users\User\Desktop\IR\Package\search-icon.png").resize((50, 50), Image.ANTIALIAS))
    button = Button(frame2, image = img2, height=35, width=35, bg="white", command = lambda: result_page(root,text.get()))
    button.pack(side = "left", padx=10)
    root.bind("<Return>", lambda event : result_page(root,text.get()))
    root.mainloop()

if __name__ == '__main__':
    query_page()


