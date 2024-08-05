import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
import csv

def shop_scr(name, username):
    from Singleplayer_start import start_match_singleplayer
    print(name)

    class ScrollBar:
        def __init__(self):
            shp = tk.Tk()
            shp.title("Shop")
            shp.geometry('600x800')
            shp.resizable(False, False)
            shp.configure(background='light grey')
            ph1 = tk.PhotoImage(file=r'images\home\quicket.png')
            shp.iconphoto(True, ph1)

            style = ttk.Style()
            style.configure('TNotebook.Tab', padding=[20, 10])

            def go_to_singleplayer():
                shp.destroy()
                start_match_singleplayer(name, username)

            def buy_player(player_name, player_price):
                
                print(f"Bought {player_name} for {player_price}")

            # Function to get player names and prices
            def get_names_price(img_no, ptype):
                file_path = ''
                if ptype == 'batsmen':
                    file_path = r'Data\batsmen_data.csv'
                elif ptype == 'bowlers':
                    file_path = r'Data\bowlers_data.csv'
                elif ptype == 'all_rounders':
                    file_path = r'Data\all_rounders_data.csv'
                elif ptype == 'wk_keepers':
                    file_path = r'Data\wk_keepers_data.csv'

                with open(file_path) as p_names:
                    names_reader = csv.reader(p_names, delimiter=',')
                    iterate_count = -1
                    for row in names_reader:
                        if iterate_count == img_no:
                            p_name = row[0]
                            p_price = row[4]
                            return [p_name, p_price]
                        iterate_count += 1

            tabControl = ttk.Notebook(shp)

            tab1 = ttk.Frame(tabControl) 
            tab2 = ttk.Frame(tabControl)
            tab3 = ttk.Frame(tabControl)
            tab4 = ttk.Frame(tabControl) 
            
            tabControl.add(tab1, text='Batsmen') 
            tabControl.add(tab2, text='Bowlers') 
            tabControl.add(tab3, text='All Rounders') 
            tabControl.add(tab4, text='WK Keepers') 
            tabControl.pack(expand=1, fill='both') 

            # Function to create a tab
            def create_tab(tab, path, ptype):
                canvas = Canvas(tab)
                canvas.pack(side=LEFT, fill=BOTH, expand=True)
                
                scrollbar = Scrollbar(tab, orient=VERTICAL, command=canvas.yview)
                scrollbar.pack(side=RIGHT, fill=Y)
                
                canvas.configure(yscrollcommand=scrollbar.set)
                canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                
                scr_frame = Frame(canvas)
                canvas.create_window((0, 0), window=scr_frame, anchor="nw")

                photo4 = tk.PhotoImage(file=r'images\singleplayer_start\home1.png')                
                btn3 = tk.Button(scr_frame, image=photo4, command=go_to_singleplayer, borderwidth=0, background='light grey')
                btn3.photo = photo4  # Keep a reference to avoid garbage collection
                btn3.grid(row=0, column=0, sticky=W, padx=10, pady=10)

                dir_list = os.listdir(path)
                print("Files and directories in '", path, "' :")
                print(dir_list)

                images = []
                buttons = []
                for player in dir_list:
                    img_path = os.path.join(path, f'{player}')
                    if os.path.exists(img_path):
                        img = Image.open(img_path)
                        img_resized = img.resize((150, 200))  # Resize images to 150x200
                        img_tk = ImageTk.PhotoImage(img_resized)
                        images.append(img_tk)

                img_no = 0

                for idx, img_tk in enumerate(images):
                    row = (idx // 3) + 1  # Start placing images from row 1 to avoid overlapping with the home button
                    col = idx % 3

                    frame = Frame(scr_frame)
                    frame.grid(row=row, column=col, padx=10, pady=10)

                    label = Label(frame, image=img_tk)
                    label.image = img_tk
                    label.pack()

                    name, price = get_names_price(img_no, ptype)
                    purchase_text = Label(frame, text=name, font=('Roboto Mono', 10, 'bold'))
                    purchase_text.pack()

                    price_text = Label(frame, text=price, font=('Roboto Mono', 10, 'bold'))
                    price_text.pack()

                    buy_photo = tk.PhotoImage(file=r'images\shop\buy.png')
                    buy_btn = Button(frame, image=buy_photo, style='A.TButton', command=lambda n=name, p=price: buy_player(n, p))
                    buy_btn.image = buy_photo  # Keep a reference to avoid garbage collection
                    buy_btn.pack()

                    buttons.append(buy_btn)

                    img_no += 1

            create_tab(tab1, r'images\shop\batsmen', 'batsmen')
            create_tab(tab2, r'images\shop\bowlers', 'bowlers')
            create_tab(tab3, r'images\shop\all rounders', 'all_rounders')
            create_tab(tab4, r'images\shop\wk keepers', 'wk_keepers')

            shp.mainloop()

    scr = ScrollBar()