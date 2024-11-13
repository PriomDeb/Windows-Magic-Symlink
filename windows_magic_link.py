from tkinter import Tk, filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import subprocess
from tkinter import Toplevel, Label, Button

import sys
import os

if hasattr(sys, "_MEIPASS"):
    ui_folder_path = os.path.join(sys._MEIPASS, "UI")
else:
    ui_folder_path = os.path.join(os.getcwd(), "UI")


def show_custom_warning(command, error_message, error=False):
    # Create a new Toplevel window as a custom dialog
    warning_window = Toplevel()
    if error:
        title = "Error"
        image = f"{ui_folder_path}/error.png"
        font_color = "#FF0000"
        message = f"Error creating symlink: \n{error_message}"
    else:
        title = "Symlink Created"
        image = f"{ui_folder_path}/link_created.png"
        font_color = "#A6FF00"
        message = f"Symlink Created: \n{error_message}"
    warning_window.title(title)
    warning_window.iconbitmap(f"{ui_folder_path}/icon.ico")
    
    window_x = 500
    window_y = 300

    screen_width = warning_window.winfo_screenwidth()
    screen_height = warning_window.winfo_screenheight()

    centered_x = int(screen_width / 2 - window_x / 2)
    centered_y = int(screen_height / 2 - window_y / 2)

    window_string = f"{window_x}x{window_y}+{centered_x}+{centered_y}"

    # Constant Windows size
    warning_window.geometry(window_string)
    warning_window.minsize(window_x, window_y)
    warning_window.maxsize(window_x, window_y)
    
    warning_window.configure(bg="#171821")
    warning_window.grab_set()  # Makes the dialog modal
    
    message_ui = Image.open(image)
    message_ui = message_ui.resize((window_x, window_y))
    message_ui = ImageTk.PhotoImage(message_ui)
    warning_window.message_ui = message_ui 

    bg_canvas = Canvas(warning_window, width=window_x, height=window_y)
    bg_canvas.pack(fill=BOTH, expand=True)
    bg_canvas.create_image(0, 0, image=message_ui, anchor="nw")
    
    
    message_label = Label(
        warning_window,
        text=message,
        font=("Arial", 8),
        bg="#171821",
        fg=font_color,
        wraplength=350,
        justify="left",
    )
    message_label.pack(pady=10, padx=20)
    message_label.place(x = 79, y = 138, width=340, height=126)
    
    
    message_button_icon = Image.open(f"{ui_folder_path}/message_button.png")
    message_button_icon = message_button_icon.resize((72, 21))
    message_button_icon = ImageTk.PhotoImage(message_button_icon)
    warning_window.message_button_icon = message_button_icon
    message_button = Button(warning_window, 
                            image=warning_window.message_button_icon, 
                            compound="top", 
                            bg=font_color, 
                            border=0.0, 
                            borderwidth=0,
                            highlightthickness=0,
                            activebackground="#171821",
                            command=warning_window.destroy,
                            )
    message_button.pack(pady=20)
    message_button.place(x=214, y=271)


selected_folders = []
selected_symlink_folder = []

def on_drop():
    folder_path = filedialog.askdirectory()
    selected_folders.append(folder_path)
    
    target_folder.delete("1.0", END)
    folders = ""
    for i in selected_folders:
        folders += f"{i}, "
    
    folders = folders[:-2]
    target_folder.insert(INSERT, folders)

def on_drop_symlink_folder():
    folder_path = filedialog.askdirectory()
    selected_symlink_folder.append(folder_path)
    
    symlink_folder.delete("1.0", END)
    folders = ""
    for i in selected_symlink_folder:
        folders += f"{i}, "
    
    folders = folders[:-2]
    symlink_folder.insert(INSERT, folders)

def clear_folders():
    selected_folders.clear()
    selected_symlink_folder.clear()
    target_folder.delete("1.0", END)
    symlink_folder.delete("1.0", END)

def clear_selected_folder():
    selected_folders.clear()
    target_folder.delete("1.0", END)


def create_symlink(target=None, symlink=None):
    target = selected_folders
    symlink = selected_symlink_folder
    
    if len(symlink) == 0 or len(target) == 0:
        show_custom_warning(command="No folder selected.", error_message="Please select folders.", error=True)
        return
    
    temp = f'/{target[0].split("/")[-1]}'
    command = f'mklink "{symlink[0]}{temp}" "{target[0]}" /D'
    print(command)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        message = f"Executed command: {command} \n\n{result.stdout}"
        show_custom_warning(command=command, error_message=message)
        # print(f"Symlink created successfully: {result.stdout}")
    
    except subprocess.CalledProcessError as e:
        message = f"Executed command: {command} \n\nError creating symlink: {e.stderr}"
        show_custom_warning(command=command, error_message=message, error=True)
        # print("Error creating symlink:", e.stderr)


def windows_magic_link():
    global root, target_folder, symlink_folder
    root = Tk()
    version = "1.0"
    root.title(f"Windows Magic Link v{version}")
    root.iconbitmap(f"{ui_folder_path}/icon.ico")

    window_x = 400
    window_y = 630

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    centered_x = int(screen_width / 2 - window_x / 2)
    centered_y = int(screen_height / 2 - window_y / 2)

    window_string = f"{window_x}x{window_y}+{centered_x}+{centered_y}"

    # Constant Windows size
    root.geometry(window_string)
    root.minsize(window_x, window_y)
    root.maxsize(window_x, window_y)

    main_ui = Image.open(f"{ui_folder_path}/windows_magic_link.png")
    resize_main_ui = main_ui.resize((window_x, window_y))
    resized_main_ui = ImageTk.PhotoImage(resize_main_ui)

    bg_canvas = Canvas(root, width=window_x, height=window_y)
    bg_canvas.pack(fill=BOTH, expand=True)
    bg_canvas.create_image(0, 0, image=resized_main_ui, anchor="nw")
    
    
    
    instruction_label = Label(root, text="Create Symlinks", pady=10, font=("", 20),)
    instruction_label.pack()
    
    browse_x, browse_y, browse_w, browse_h = 50, 250, 232, 40
    target_folder = Text(root,
                         bg="#171821",
                         border=0,
                         highlightthickness=0,
                         font=("", 10),
                         foreground="white",
                         )
    target_folder.pack()
    target_folder.place(x=browse_x,
                      y=browse_y,
                      width=browse_w,
                      height=browse_h,
                      )
    
    symlink_folder = Text(root,
                          bg="#171821",
                          border=0,
                          highlightthickness=0,
                          font=("", 10),
                          foreground="white",
                          )
    symlink_folder.pack()
    symlink_folder.place(x=browse_x,
                      y=browse_y + 206,
                      width=browse_w,
                      height=browse_h,
                      )
    
    
    target_folder_browse_button_icon = Image.open(f"{ui_folder_path}/browse.png")
    target_folder_browse_button_icon = target_folder_browse_button_icon.resize((38,38))
    target_folder_browse_button_icon = ImageTk.PhotoImage(target_folder_browse_button_icon)
    target_folder_browse_button = Button(root, 
                                         image=target_folder_browse_button_icon, 
                                         compound="top", 
                                         bg="#171821", 
                                         border=0.0, 
                                         activebackground="#171821",
                                         command=on_drop,
                                         )
    target_folder_browse_button.pack(pady=20)
    target_folder_browse_button.place(x=286, y=248)
    
    
    target_folder_clear_icon = Image.open(f"{ui_folder_path}/clear.png")
    target_folder_clear_icon = target_folder_clear_icon.resize((38, 38))
    target_folder_clear_icon = ImageTk.PhotoImage(target_folder_clear_icon)
    target_folder_clear = Button(root, 
                                 image=target_folder_clear_icon, 
                                 compound="top", 
                                 bg="#171821", 
                                 border=0.0, 
                                 activebackground="#171821",
                                 command=clear_selected_folder,
                                 )
    target_folder_clear.pack(pady=20)
    target_folder_clear.place(x=286 + 46, y=246)
    
    
    symlink_folder_browse_button_icon = Image.open(f"{ui_folder_path}/link.png")
    symlink_folder_browse_button_icon = symlink_folder_browse_button_icon.resize((38, 38))
    symlink_folder_browse_button_icon = ImageTk.PhotoImage(symlink_folder_browse_button_icon)
    symlink_folder_browse_button = Button(root, 
                                         image=symlink_folder_browse_button_icon, 
                                         compound="top", 
                                         bg="#171821", 
                                         border=0.0, 
                                         activebackground="#171821",
                                         command=on_drop_symlink_folder,
                                         )
    symlink_folder_browse_button.pack(pady=20)
    symlink_folder_browse_button.place(x=286, y=450)
    
    
    clear_all_folder = Image.open(f"{ui_folder_path}/clear.png")
    clear_all_folder = clear_all_folder.resize((38, 38))
    clear_all_folder = ImageTk.PhotoImage(clear_all_folder)
    clear_all_folder_button = Button(root, 
                                     image=clear_all_folder, 
                                     compound="top", 
                                     bg="#171821", 
                                     border=0.0, 
                                     activebackground="#171821",
                                     command=clear_folders,
                                     )
    clear_all_folder_button.pack(pady=20)
    clear_all_folder_button.place(x=286 + 46, y=450)
    
    
    create_link_button_icon = Image.open(f"{ui_folder_path}/button.png")
    create_link_button_icon = create_link_button_icon.resize((156, 48))
    create_link_button_icon = ImageTk.PhotoImage(create_link_button_icon)
    create_link_button = Button(root, 
                                image=create_link_button_icon, 
                                compound="top", 
                                bg="#171821", 
                                border=0.0, 
                                activebackground="#171821",
                                command=create_symlink,
                                )
    create_link_button.pack(pady=20)
    create_link_button.place(x=120, y=538)
    
    
    urls = {
        "website": "http://priomdeb.com",
        "linkedin": "https://www.linkedin.com/in/priomdeb",
        "email": "mailto:priom@priomdeb.com"
        }
    
    
    website_icon = Image.open(f"{ui_folder_path}/website.png")
    website_icon = website_icon.resize((20, 20))
    website_icon = ImageTk.PhotoImage(website_icon)
    website_button = Button(root, 
                            image=website_icon, 
                            compound="top", 
                            bg="#171821", 
                            border=0.0, 
                            activebackground="#171821",
                            command=lambda: webbrowser.open_new(urls["website"]),
                            )
    website_button.pack(pady=20)
    website_button.place(x=6.5, y=597)
    
    
    linkedin_icon = Image.open(f"{ui_folder_path}/linkedin.png")
    linkedin_icon = linkedin_icon.resize((20, 20))
    linkedin_icon = ImageTk.PhotoImage(linkedin_icon)
    linkedin_button = Button(root, 
                                image=linkedin_icon, 
                                compound="top", 
                                bg="#171821", 
                                border=0.0, 
                                activebackground="#171821",
                                command=lambda: webbrowser.open_new(urls["linkedin"]),
                                )
    linkedin_button.pack(pady=20)
    linkedin_button.place(x=36, y=597)
    
    
    email_icon = Image.open(f"{ui_folder_path}/email.png")
    email_icon = email_icon.resize((20, 20))
    email_icon = ImageTk.PhotoImage(email_icon)
    email_button = Button(root, 
                          image=email_icon, 
                          compound="top", 
                          bg="#171821", 
                          border=0.0, 
                          activebackground="#171821",
                          command=lambda: webbrowser.open_new(urls["email"]),
                          )
    email_button.pack(pady=20)
    email_button.place(x=65, y=597)

    # Run App
    root.mainloop()

windows_magic_link()



# pyinstaller --onefile --uac-admin -w --add-data "UI;UI" --icon=UI/icon.ico windows_magic_link.py

