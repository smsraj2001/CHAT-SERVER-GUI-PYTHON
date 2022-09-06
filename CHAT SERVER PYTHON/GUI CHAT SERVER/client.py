#import required modules
#from distutils.cmd import Command
from email import message
from re import I
import socket
from sqlite3 import connect
import threading
import tkinter as tk
from tkinter import Button, Label, scrolledtext
from tkinter import messagebox
from turtle import width
#from PIL import ImageTk,Image
from tkinter import filedialog
import time
import os
import os, shutil, sys
#from PIL import Image

#HOST = '192.168.50.82'
HOST = input("Enter the SERVER IP ADDRESS:-\n") # You should enter the same IP address as given in the server.py file.
PORT = int(input("Enter the port number for chat room its a FOUR-FIVE digit number:-\n"))
#PORT = 12000

DARK_GREY = '#121212'
MEDIUM_GREY = '#0000FF'
#'#804FB3'
#'#1F1b24'
ORI_DARK_GREY = "#1F1b24"
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica",17)
BUTTON_FONT = ('Helvetica', 15)
SMALL_FONT = ("Helvetica", 13)

#creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	

def add_message(message):
	message_box.config(state=tk.NORMAL)
	message_box.insert(tk.END, message + '\n')
	message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successsfullly connected to server")
        add_message("[SERVER] Successfully connected to the server")
		
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect server {HOST} {PORT}")



    username = username_textbox.get()
    if username != '':
	    client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username","Username cannot be empty")
        
		
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
	message = message_textbox.get()
	if message != "":
		#client.sendall(message.encode())
		client.sendall(message.encode("utf-8"))
		message_textbox.delete(0, len(message))
	else:
		messagebox.showerror("Empty message","Message cannot be empty")
		

def attach_message():
	file_name = input("File Name:")
	file_size = os.path.getsize(file_name)


	# Sending file_name and detail.
	client.send(file_name.encode())
	client.send(str(file_size).encode())

	# Opening file and sending data.
	with open(file_name, "rb") as file:
		c = 0
		# Starting the time capture.
		start_time = time.time()

		# Running loop while c != file_size.
		while c <= file_size:
			data = file.read(1024)
			if not (data):
				break
			client.send(data)
			#file.write(data)
			c += len(data)

		# Ending the time capture.
		end_time = time.time()	
	print("File Transfer Complete.Total time: ", end_time - start_time)




root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False) 

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)





top_frame = tk.Frame(root, width=600, height=100,bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row = 2,column=0,sticky=tk.NSEW)

bottom_up = tk.Frame(root, width=600, height=100, bg=MEDIUM_GREY)
bottom_up.grid(row = 3,column=0,sticky=tk.NSEW)


username_label = tk.Label(top_frame, text="Enter UserName: ",font=FONT,bg=DARK_GREY,fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE)
username_textbox.pack(side=tk.LEFT) 

my_btn = tk.Button(bottom_up, text="OpenFile -> .txt", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=attach_message)
my_btn.pack(side=tk.LEFT, padx=5)


username_button = tk.Button(top_frame, text="JOIN", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10) 

message_button =tk.Button(bottom_frame, text="📝⏫", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)





def listen_for_messages_from_server(client):

	while 1:
	
		message = client.recv(2048).decode()
		if message != '':
			username = message.split("~")[0]
			content = message.split('~')[1]
			
			add_message(f"[{username}] {content}")

			
		else:
			messagebox.showerror("Error","Message recieved from client is empty")


	
		



def main():
	root.mainloop()

		
if __name__ == "__main__":
	main()
 