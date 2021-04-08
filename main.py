import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
# from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt

import sqlite3

from PIL import ImageTk, Image

import pandas as pd
import statistics
import csv

# own file
import today
import my_clock

style.use("bmh")  # style for the matplotlib graph  --- this style contain a default grid.

list_curr = ['EUR', 'USD', 'AED', 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EGP', 'GBP', 'HRK',
             'HUF', 'INR', 'JPY', 'KRW', 'MDL', 'MXN', 'NOK', 'NZD', 'PLN', 'RSD', 'RUB', 'SEK', 'THB', 'TRY',
             'UAH', 'XDR', 'ZAR']  # 31

dict_curr = {
    'EUR': 0, 'USD': 1, 'AED': 2, 'AUD': 3, 'BGN': 4, 'BRL': 5, 'CAD': 6, 'CHF': 7, 'CNY': 8, 'CZK': 9,
    'DKK': 10, 'EGP': 11, 'GBP': 12, 'HRK': 13, 'HUF': 14, 'INR': 15, 'JPY': 16, 'KRW': 17, 'MDL': 18,
    'MXN': 19, 'NOK': 20, 'NZD': 21, 'PLN': 22, 'RSD': 23, 'RUB': 24, 'SEK': 25, 'THB': 26, 'TRY': 27,
    'UAH': 28, 'XDR': 29, 'ZAR': 30
}

"""
Bellow i created variables that contain the file from which we will show the values
    - that will help for building the show_2020() and show_all_currencies() functions
    - to choose a period to show = show values from a .csv  file (file that contain the currencies from the period ) 

OBS: period variable is the text of a label that will be grid on first row, from page 
        ( to show the period that is on the screen )
OBS2: * period_to_show = from which file we take data for building the graphs
      * period = the text that will be show in top of the pages as Label (to show us what period are we using)
      * current_page = is used to remember what class(page) are we running    
"""
period_to_show = 'currencies(csv)\\currencies2021.csv'
period = '2021'
current_page = None
database_user_logged = 'user database'
e_mail_user_logged = ''


def get_avgs_list(given_csv_file):
    """
    :param given_csv_file: is the file (period) from which we take values
    :return: a list with all averages, for each currency, on the given period
    """

    with open(given_csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        list_val_curr = []
        avgs_list_to_return = []

        for curr in list_curr:
            for line in csv_reader:
                list_val_curr.append(float(line[curr]))

            avg = statistics.mean(list_val_curr)
            avgs_list_to_return.append(round(avg, 4))

            csv_file.seek(0)
            csv_reader = csv.DictReader(csv_file)
            list_val_curr = []

    return avgs_list_to_return


def convert():
    """
    Here i created a fast converter
        -> create the 'tab' from 0 : - first create the root
                                     - then put 2 frames and a canvas
                                     - canvas is used as a background (have same color with frame 2)
                                     - frame2 contain the main of window ('Exchange from' + 'Exchange in'
                                                                          + 'Amount' + 'Result')
                                     - frame1 contain the 'TVA Calculator'
    """

    def convert_money():
        current_currency = clicked_curr.get()
        given_value = entry_amount.get()

        changed_value = float(given_value) / float(today.currency[current_currency])
        round_value = round(changed_value, 4)

        # Creating a label with the Result (convert value --> float)
        changed_value_label = tk.Label(frame2, font=13, text='',
                                       bg='#263D42', fg='#D4D4BF')
        changed_value_label.grid(row=8, column=1)

        changed_value_label['text'] = str(round_value) + ' ' + clicked_curr.get()

        tva_value = (19 / 100) * round_value
        tva_val_label = tk.Label(frame1, text=str(tva_value), font=('Calibri', 15), bg='grey')
        tva_val_label.grid(row=2, column=1)

        final_value = tva_value + round_value
        tva_final_result = tk.Label(frame1, text=str(round(final_value, 4)) + ' ' + current_currency,
                                    font=('Calibri', 15), bg='grey')
        tva_final_result.grid(row=3, column=1)

    # Getting the currency date :
    date = today.current_date

    window = tk.Tk()
    window.title('Fast Converter')
    window.geometry("465x600+70+60")
    window.resizable(0, 0)

    canvas_root = tk.Canvas(window, height=600, width=465, bg='#263D42')
    canvas_root.pack()

    frame1 = tk.Frame(window, bg='grey')
    frame1.place(relwidth=0.9, relheight=0.3, relx=0.05, rely=0.67)

    frame2 = tk.Frame(window, bg='#263D42')
    frame2.place(relwidth=0.92, relheight=0.629, relx=0.04, rely=0.02)

    # Options currencies are saved in today.py
    options = today.list_currencies_of_countries

    title = tk.Label(frame2, text="     ! Make the exchange now ! \n "
                                  "Using the BNR course from " + date + ' ', bg='#CBCE18', fg='white',
                     font=('Courier', 14, 'bold'), relief=tk.RAISED, borderwidth=3)

    title.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

    label_wild = tk.Label(frame2, text='', fg='#263D42', bg='#263D42')
    label_wild.grid(row=1, column=0, columnspan=2)

    label1 = tk.Label(frame2, text='Exchange from ', font=('Calibri', 15), bg='#263D42', fg='#D4D4BF')
    label1.grid(row=2, column=0)

    ron_label = tk.Label(frame2, text='RON', font=('Calibri', 13), bg='#263D42', fg='#D4D4BF')
    ron_label.grid(row=2, column=1)

    label2 = tk.Label(frame2, text='Exchange in ', font=('Calibri', 15), bg='#263D42', fg='#D4D4BF')
    label2.grid(row=3, column=0)

    # Creating a Option Menu with all currencies:
    clicked_curr = tk.StringVar()
    clicked_curr.set(options[0])  # todo: nothing happen at options[0] !? - weird ..   see why !!
    currencies_menu = ttk.OptionMenu(frame2, clicked_curr, *options)
    currencies_menu.grid(row=3, column=1)

    label3 = tk.Label(frame2, text='Amount ', font=('Calibri', 15), bg='#263D42', fg='#D4D4BF')
    label3.grid(row=4, column=0)

    entry_amount = ttk.Entry(frame2, font=('Calibri', 15))
    entry_amount.grid(row=4, column=1)

    label_wild = tk.Label(frame2, text='', fg='#263D42', bg='#263D42')
    label_wild.grid(row=5, column=0, columnspan=2)

    calc_button = ttk.Button(frame2, text="Calculate", command=convert_money)
    calc_button.grid(row=6, column=0, columnspan=2, ipadx=180, ipady=5)

    label_wild = tk.Label(frame2, text='', fg='#263D42', bg='#263D42')
    label_wild.grid(row=7, column=0, columnspan=2)

    result_label = tk.Label(frame2, text='RESULT : ', font=15, bg='#263D42', fg='#D4D4BF')
    result_label.grid(row=8, column=0)

    label_wild = tk.Label(frame2, text='', fg='#263D42', bg='#263D42')
    label_wild.grid(row=9, column=0, columnspan=2)

    # Creating a TVA calculator :
    label_tva_title = tk.Label(frame1, text='           TVA Calculator           ', font=('Verdana', 20), bg='white')
    label_tva_title.grid(row=0, column=0, columnspan=2)

    label_wild = tk.Label(frame1, text='', fg='grey', bg='grey')
    label_wild.grid(row=1, column=0, columnspan=2)

    tva_val_wild = tk.Label(frame1, text='TVA(19%): ', font=('Calibri', 15), bg='grey')
    tva_val_wild.grid(row=2, column=0)
    tva_result_wild = tk.Label(frame1, text='Value After TVA: ', font=('Calibri', 15), bg='grey')
    tva_result_wild.grid(row=3, column=0)

    window.mainloop()


def pop_up_msg():
    messagebox.showinfo('Bad day for you..', 'Not supported yet !')


# Here is the body(root) of app :
class ExchangeCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # is a good practice to put *args and **kwargs --> for the future of app

        tk.Tk.title(self, "RoExchange")
        # tk.Tk.iconbitmap(self, default='eur.ico')   # todo : need a '.ico' icon ! -> is a must
        # on the root(tk.Tk) we must have a parent frame:
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand='True')

        container.grid_rowconfigure(0, weight=1)  # set the row and col to 1  , because i want to show the text
        container.grid_columnconfigure(0, weight=1)  # in center of screen

        # create a func to show all currencies from 2021
        def show_2021():
            global period_to_show, period
            period_to_show = 'currencies(csv)\\currencies2021.csv'
            period = '2021'

            """
            EuroPage and DollarPage are separated classes from the others. 
                So to change the period must be done separated.
            Steps: - destroy the frame
                   - recreate the frame 
            When we recreate the frame, it will be created with the new period_to_show 
            """
            if current_page == EuroPage:
                self.frames[EuroPage].grid_forget()
                self.frames[EuroPage].destroy()
                self.frames[EuroPage].__init__(container, self)
                self.show_frame(EuroPage)
            elif current_page == DollarPage:
                self.frames[DollarPage].grid_forget()
                self.frames[DollarPage].destroy()
                self.frames[DollarPage].__init__(container, self)
                self.show_frame(DollarPage)

        # create a func to show all currencies from 2020
        def show_2020():
            global period_to_show, period
            period_to_show = 'currencies(csv)\\currencies2020.csv'
            period = '2020-full year'

            """
            EuroPage and DollarPage are separated classes from the others. 
                So to change the period must be done separated.
            Steps: - destroy the frame
                   - recreate the frame 
            When we recreate the frame, it will be created with the new period_to_show 
            """
            if current_page == EuroPage:
                self.frames[EuroPage].grid_forget()
                self.frames[EuroPage].destroy()
                self.frames[EuroPage].__init__(container, self)
                self.show_frame(EuroPage)
            elif current_page == DollarPage:
                self.frames[DollarPage].grid_forget()
                self.frames[DollarPage].destroy()
                self.frames[DollarPage].__init__(container, self)
                self.show_frame(DollarPage)

        # create a func to show all currencies from 2019
        def show_2019():
            global period_to_show, period
            period_to_show = 'currencies(csv)\\currencies2019.csv'
            period = '2019-full year'

            """
            EuroPage and DollarPage are separated classes from the others. 
                So to change the period must be done separated.
            Steps: - destroy the frame
                   - recreate the frame 
            When we recreate the frame, it will be created with the new period_to_show 
            """
            if current_page == EuroPage:
                self.frames[EuroPage].grid_forget()
                self.frames[EuroPage].destroy()
                self.frames[EuroPage].__init__(container, self)
                self.show_frame(EuroPage)
            elif current_page == DollarPage:
                self.frames[DollarPage].grid_forget()
                self.frames[DollarPage].destroy()
                self.frames[DollarPage].__init__(container, self)
                self.show_frame(DollarPage)

        # create a func to show all currencies from 2018
        def show_2018():
            global period_to_show, period
            period_to_show = 'currencies(csv)\\currencies2018.csv'
            period = '2018-full year'

            """
            EuroPage and DollarPage are separated classes from the others. 
                So to change the period must be done separated.
            Steps: - destroy the frame
                   - recreate the frame 
            When we recreate the frame, it will be created with the new period_to_show 
            """
            if current_page == EuroPage:
                self.frames[EuroPage].grid_forget()
                self.frames[EuroPage].destroy()
                self.frames[EuroPage].__init__(container, self)
                self.show_frame(EuroPage)
            elif current_page == DollarPage:
                self.frames[DollarPage].grid_forget()
                self.frames[DollarPage].destroy()
                self.frames[DollarPage].__init__(container, self)
                self.show_frame(DollarPage)

        def set_graph_dimensions():
            def save_dim(left, bottom, right, top, wspace, hspace):
                if left == '' or bottom == '' or right == '' or top == '' or wspace == '' or hspace == '':
                    messagebox.showerror('ERROR', 'The values must be between 0 and 1 !')
                elif float(left) > 1 or float(bottom) > 1 or float(right) > 1 or float(top) > 1 \
                        or float(wspace) > 1 or float(hspace) > 1:
                    messagebox.showerror('ERROR', 'The values must be between 0 and 1 !')
                elif float(left) < 0 or float(bottom) < 0 or float(right) < 0 or float(top) < 0 \
                        or float(wspace) < 0 or float(hspace) < 0:
                    messagebox.showerror('ERROR', 'The values must be between 0 and 1 !')
                else:
                    plt.subplots_adjust(left=float(left), bottom=float(bottom), right=float(right), top=float(top),
                                        wspace=float(wspace), hspace=float(hspace))

            root = tk.Tk()
            root.title('Set graph dimensions')
            root.configure(bg='#4A85FF')
            root.geometry('250x320')
            root.resizable(0, 0)

            styl_save = ttk.Style()
            styl_save.theme_use('default')
            styl_save.configure('Save.TButton', font=('College', 15, 'bold'), background='#F9EA3D',
                                foreground='#353102')
            styl_save.map('Save.TButton', background=[('active', '#D1C219')])

            left_label = tk.Label(root, text='left', font='Impact 24', bg='#4A85FF')
            left_entry = ttk.Entry(root, font='College 15', width=12)
            bottom_label = tk.Label(root, text='bottom', font='Impact 24', bg='#4A85FF')
            bottom_entry = ttk.Entry(root, font='College 15', width=12)
            right_label = tk.Label(root, text='right', font='Impact 24', bg='#4A85FF')
            right_entry = ttk.Entry(root, font='College 15', width=12)
            top_label = tk.Label(root, text='top', font='Impact 24', bg='#4A85FF')
            top_entry = ttk.Entry(root, font='College 15', width=12)
            wspace_label = tk.Label(root, text='wspace', font='Impact 24', bg='#4A85FF')
            wspace_entry = ttk.Entry(root, font='College 15', width=12)
            hspace_label = tk.Label(root, text='hspace', font='Impact 24', bg='#4A85FF')
            hspace_entry = ttk.Entry(root, font='College 15', width=12)

            left_label.grid(row=0, column=0)
            left_entry.grid(row=0, column=1)
            bottom_label.grid(row=1, column=0)
            bottom_entry.grid(row=1, column=1)
            right_label.grid(row=2, column=0)
            right_entry.grid(row=2, column=1)
            top_label.grid(row=3, column=0)
            top_entry.grid(row=3, column=1)
            wspace_label.grid(row=4, column=0)
            wspace_entry.grid(row=4, column=1)
            hspace_label.grid(row=5, column=0)
            hspace_entry.grid(row=5, column=1)

            save_btn = tk.Button(root, text='Save Dimensions', bg='#F9EA3D', fg='black', activebackground='#F27B04'
                                 , font='College 13 bold',
                                 command=lambda: save_dim(left_entry.get(), bottom_entry.get(),
                                                          right_entry.get(), top_entry.get(), wspace_entry.get(),
                                                          hspace_entry.get()))
            save_btn.grid(row=6, column=0, columnspan=2, pady=7, ipadx=36, padx=3)

            root.mainloop()

        # Here i am creating a menubar(the toolbar) to project
        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Set the _graph size', command=set_graph_dimensions)
        filemenu.add_command(label='Settings..', command=pop_up_msg)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        # Add the converter window on bar (show direct the converter, without any submenus)
        menubar.add_command(label='Converter', command=convert)

        # Account window:
        menubar.add_command(label='_Account', command=lambda: self.show_frame(Account))

        # go to home page :
        menubar.add_command(label='Home', command=lambda: self.show_frame(StartPage))

        # Add a option menu from which you can change the period to show:
        period_menu = tk.Menu(menubar, tearoff=0)
        period_menu.add_command(label='2021', command=lambda: show_2021())
        period_menu.add_command(label='2020', command=lambda: show_2020())
        period_menu.add_command(label='2019', command=lambda: show_2019())
        period_menu.add_command(label='2018', command=lambda: show_2018())
        menubar.add_cascade(label='Choose period to show', menu=period_menu)

        tk.Tk.config(self, menu=menubar)

        global period_to_show
        self.frames = {}  # here i am creating a dict that will contains all pages (frames)

        for FRAME in (StartPage, DollarPage, UserExchangesPage, OtherPages, EuroPage, LoginPage, Account):
            frame = FRAME(container, self)  # Creating the pages (frames) 1 by 1 . Pages are classes !
            self.frames[FRAME] = frame  # adding to dict

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]  # take the page from dict and  add it in front with tkraise()
        if cont == Account:
            frame.grid(row=0, column=0, sticky='nw', padx=5)
            frame.tkraise()
        else:
            frame.grid(row=0, column=0, sticky='nsew')
            frame.tkraise()

        """
        creating a variable that remember which page are we using  
        I used this way to built the show_2020()...etc  functions:
            - check if we are using the EuroPage or DollarPage , then reload the page with the new period 
            - is not used for the other graphs, because those pages are redrawn at every clicked of button
        """
        global current_page
        current_page = cont


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='white')

        # Create the buttons style :
        styl_start_pg_btns = ttk.Style()
        styl_start_pg_btns.theme_use('default')
        styl_start_pg_btns.configure('Start_btn.TButton', font=('OSAKA', 20, 'bold'),
                                     background='white', foreground='black', borderwidth=0)
        styl_start_pg_btns.map('Start_btn.TButton', background=[('active', '#E5E5E5')])

        # here is the title of the page
        label_title_page = tk.Label(self, text="START PAGE", fg="#2C3E50",
                                    bg="white", font="Impact 20")
        label_title_page.pack(pady=10, padx=10)

        canvas_width = self.winfo_screenwidth()

        canvas_bg_img = tk.Canvas(self, height=300, width=canvas_width, borderwidth=0, relief=tk.RAISED)
        canvas_bg_img.pack(side=tk.BOTTOM)
        usd_img = Image.open('images\\runner.jpg')
        canvas_bg_img.image = ImageTk.PhotoImage(usd_img.resize((canvas_width, 300), Image.ANTIALIAS))
        canvas_bg_img.create_image(0, 0, image=canvas_bg_img.image, anchor='nw')

        white_frame = tk.Frame(self, bg='white')
        white_frame.place(relwidth=1, relheight=0.01, rely=0.61, relx=0)

        # Make same space between label with title and buttons(2 spaces)
        label_for_space_horizontal = tk.Label(self, text='', bg='white')
        label_for_space_horizontal.pack()
        label_for_space_horizontal = tk.Label(self, text='', bg='white')
        label_for_space_horizontal.pack()

        usd_button = ttk.Button(self, text="See DOLLAR Page-Status", command=lambda: controller.show_frame(DollarPage),
                                style='Start_btn.TButton')
        usd_button.place(x=35, y=200)
        eur_button = ttk.Button(self, text="See EURO Page-Status", command=lambda: controller.show_frame(EuroPage),
                                style='Start_btn.TButton')
        eur_button.place(x=35, y=250)
        other_button = ttk.Button(self, text='See Other Graphs ... ', command=lambda: controller.show_frame(OtherPages),
                                  style='Start_btn.TButton')

        other_button.place(x=35, y=300)

        bucharest_label = tk.Label(self, text='BUCHAREST', font='IMPACT 20 ', bg='white', fg='black')
        bucharest_label.place(x=1200, y=80)

        # Create the clock
        canvas_clock = my_clock.Clock(self, 0, 300, 300, 'images\\clock.jpg')
        canvas_clock.place(x=1120, y=120)

        # Create the shadow for the clock:
        canvas_shadow = tk.Canvas(self, height=20, width=300, borderwidth=0, highlightthickness=0, relief=tk.RAISED)
        canvas_shadow.place(x=1120, y=470)
        shadow_img = Image.open('images\\clock_shadow.jpg')
        canvas_shadow.image = ImageTk.PhotoImage(shadow_img.resize((300, 20), Image.ANTIALIAS))
        canvas_shadow.create_image(0, 0, image=canvas_shadow.image, anchor='nw')


class EuroPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_title_page = tk.Label(self, text="Euro Page", fg="#7FFFD4",
                                    bg="#4B0082", font="Impact 20",
                                    width=300, border=3, relief=tk.SUNKEN)
        label_title_page.pack(pady=10, padx=10)

        # show the period running:
        # it's a string variable
        # it' s change when we chose other period to show
        # it's used to show us what period are we seeing on the graph
        global period
        label_show_period = tk.Label(self, text='   ' + period + '   ', font="Helvetica 20 bold italic",
                                     border=3, relief=tk.GROOVE)
        label_show_period.place(x=90, y=56)

        # Here i created the canvas with the representative flag for currency:

        canvas_eur_img = tk.Canvas(self, height=44, width=74, borderwidth=0, highlightthickness=0, relief=tk.RAISED)
        canvas_eur_img.place(x=9, y=53)
        eur_img = Image.open('images\\eur.jpg')
        canvas_eur_img.image = ImageTk.PhotoImage(eur_img.resize((74, 44), Image.ANTIALIAS))
        canvas_eur_img.create_image(0, 0, image=canvas_eur_img.image, anchor='nw')

        usd_button = tk.Button(self, text="See Dollar Page-Status", command=lambda: controller.show_frame(DollarPage),
                               bg='#B0E0E6', fg='#8B0000', activebackground='yellow',
                               highlightcolor='#A52A2A', relief='raised', font='OSAKA 14 bold italic', width=20)
        usd_button.pack()

        fig = plt.figure()
        ax1 = plt.subplot2grid((7, 5), (0, 0), rowspan=4, colspan=5)
        ax2 = plt.subplot2grid((7, 5), (5, 0), rowspan=2, colspan=5)

        # this is the .csv file from which will take the values
        # it's a global variable because it can be change to take other .csv file
        #    -> take other .csv file = change the period !!
        global period_to_show

        data = pd.read_csv(period_to_show)
        date = data['date']
        date_day = pd.to_datetime(date)  # converting string to date
        val = data['EUR']
        avg_eur = statistics.mean(val)

        euro_current_value = today.currency['EUR']  # it's a string currency['EUR'] !!!

        e_title = 'Euro Status \n Last Exchange value : ' + euro_current_value + ' RON' + ' | ' + \
                  str(round(today.eur_diff, 4))

        # Create a font for ylabel and xlabel on graph
        font = FontProperties()
        font.set_family('serif')
        font.set_name('Times New Roman')
        font.set_style('italic')
        font.set_size('15')

        ax1.clear()
        ax1.plot(date_day, val, '#23696e', marker='o')
        labels_ax1 = ax1.get_xticklabels()
        plt.setp(labels_ax1, rotation=30, horizontalalignment='right')
        ax1.set_title(e_title)
        ax1.text(avg_eur, date_day[0], 'avg')  # todo: add text on graph
        ax1.axhline(avg_eur, 0.048, color='#AEB6BF', ls='--')
        ax1.fill_between(date_day, avg_eur, val, fc='#ABEBC6')
        ax1.set_ylabel('Currency Exchange [RON]', labelpad=20, fontproperties=font)

        avgs_list = get_avgs_list(period_to_show)

        barlist = ax2.bar(list_curr, avgs_list)
        labels = ax2.get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')

        ax2.set_ylabel('Average  on \n period ', font=font, labelpad=25)

        barlist[dict_curr['EUR']].set_color('r')

        ax2.tick_params(axis='x', colors='#F39C12')  # give a color for x axis (for currencies)

        plt.subplots_adjust(left=0.07, bottom=0.071, right=0.988, top=0.902, wspace=0.2, hspace=0.2)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class DollarPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create a frame that contain the canvas with graph (frame will be show with grid() and canvas with pack())
        eur_frame_graph = tk.Frame(self)

        label_title_page = tk.Label(self, text="Dollar Page", fg="#7FFFD4",
                                    bg="#4B0082", font="Impact 20",
                                    width=300, border=3, relief=tk.SUNKEN)
        label_title_page.pack(pady=10, padx=10)

        # show the period running:
        # it's a string variable
        # it' s change when we chose other period to show
        # it's used to show us what period are we seeing on the graph
        global period
        label_show_period = tk.Label(self, text='   ' + period + '   ', font="Helvetica 20 bold italic",
                                     border=3, relief=tk.GROOVE)
        label_show_period.place(x=90, y=55)

        # Here i created the canvas with the representative flag for currency:

        canvas_usd_img = tk.Canvas(self, height=43, width=74, borderwidth=0, highlightthickness=0, relief=tk.RAISED)
        canvas_usd_img.place(x=9, y=53)
        usd_img = Image.open('images\\usd.jpg')
        canvas_usd_img.image = ImageTk.PhotoImage(usd_img.resize((74, 43), Image.ANTIALIAS))
        canvas_usd_img.create_image(0, 0, image=canvas_usd_img.image, anchor='nw')

        eur_btn = tk.Button(self, text="See Euro Page-Status", command=lambda: controller.show_frame(EuroPage),
                            bg='#B0E0E6', fg='#8B0000', activebackground='yellow',
                            highlightcolor='#A52A2A', relief='raised', font='OSAKA 14 bold italic', width=20)
        eur_btn.pack()

        fig = plt.figure()
        ax1 = plt.subplot2grid((7, 5), (0, 0), rowspan=4, colspan=5)
        ax2 = plt.subplot2grid((7, 5), (5, 0), rowspan=2, colspan=5)

        # this is the .csv file from which will take the values
        # it's a global variable because it can be change to take other .csv file
        #    -> take other .csv file = change the period !!
        global period_to_show

        data = pd.read_csv(period_to_show)
        date = data['date']
        date_day = pd.to_datetime(date)  # converting string to date
        val = data['USD']
        avg_usd = statistics.mean(val)

        dollar_current_value = today.currency['USD']  # it's a string currency['USD'] !!!

        d_title = 'Dollar Status \n Last Exchange vale : ' + dollar_current_value + ' RON' + ' | ' + \
                  str(round(today.usd_diff, 4))

        # Create a font for ylabel and xlabel on graph
        font = FontProperties()
        font.set_family('serif')
        font.set_name('Times New Roman')
        font.set_style('italic')
        font.set_size('15')

        ax1.clear()
        ax1.plot(date_day, val, '#FFBF00', marker='o')
        labels_ax1 = ax1.get_xticklabels()
        plt.setp(labels_ax1, rotation=30, horizontalalignment='right')
        ax1.set_title(d_title)
        # ax.set_text(avg_usd, date_day[1], 'avg')  # todo: add text on graph
        ax1.axhline(avg_usd, 0.048, color='#AEB6BF', ls='--')
        ax1.fill_between(date_day, avg_usd, val, fc='#CA5D5D')
        ax1.set_ylabel('Currency Exchange [RON]', labelpad=20, fontproperties=font)

        avgs_list = get_avgs_list(period_to_show)

        barlist = ax2.bar(list_curr, avgs_list)
        labels_ax2 = ax2.get_xticklabels()
        plt.setp(labels_ax2, rotation=45, horizontalalignment='right')
        ax2.set_ylabel('Average  on \n period ', font=font, labelpad=25)
        barlist[dict_curr['USD']].set_color('r')

        ax2.tick_params(axis='x', colors='#F39C12')  # give a color for x axis (for currencies)

        plt.subplots_adjust(left=0.07, bottom=0.071, right=0.988, top=0.902, wspace=0.2, hspace=0.2)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class OtherPages(tk.Frame):
    """
    This class is a frame which will contain a canvas that have the graph for the every currency
    (without EUR and USD)
    OtherPages class has the __init__ func that create the list of buttons with currencies, and contain the canvas with
    the graph of currency.
    The graph is created by the OnePage class
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        container_o = tk.Frame(self)
        container_o.pack(side='top', fill='both', expand='True')

        # container_o is set to have only 3 rows (that will expand the graph on all page)
        container_o.rowconfigure(3, weight=2)

        self.frames = {}  # here i am creating a dict that will contains all pages (frames)

        def show_pages(currency):
            frame = OnePage(container_o, currency)  # Creating the pages (frames) 1 by 1 . Pages are classes !
            self.frames[OnePage] = frame  # adding to dict
            frame.grid(row=2, column=0, sticky='nsew', columnspan=20, rowspan=2)

        # Create a style for currencies buttons:
        styl_3 = ttk.Style()
        styl_3.theme_use('default')
        styl_3.configure('B3.TButton', font=('Freshman', 10), background='#E7E5D1', foreground='#0647C5')
        styl_3.map('B3.TButton', background=[('active', '#B9E8F5')])

        # Create a style for left/right buttons:
        styl_4 = ttk.Style()
        styl_4.theme_use('default')
        styl_4.configure('B4.TButton', font=('Freshman', 10, 'bold'), background='#E9967A', foreground='#353102')
        styl_4.map('B4.TButton', background=[('active', '#CD5C5C')])

        # Create a style for left/right buttons when are disabled !!:
        styl_5 = ttk.Style()
        styl_5.theme_use('default')
        styl_5.configure('Disabled.TButton', font=('College', 10, 'bold'), background='#C8C7C4', foreground='#353102')
        styl_5.map('Disabled.TButton', background=[('active', '#8F8E87')])

        # Here i created the buttons:
        aed_btn = ttk.Button(container_o, text='AED', command=lambda: show_pages('AED'), style='B3.TButton')
        aud_btn = ttk.Button(container_o, text='AUD', command=lambda: show_pages('AUD'), style='B3.TButton')
        bgn_btn = ttk.Button(container_o, text='BGN', command=lambda: show_pages('BGN'), style='B3.TButton')
        cad_btn = ttk.Button(container_o, text='CAD', command=lambda: show_pages('CAD'), style='B3.TButton')
        chf_btn = ttk.Button(container_o, text='CHF', command=lambda: show_pages('CHF'), style='B3.TButton')
        cny_btn = ttk.Button(container_o, text='CNY', command=lambda: show_pages('CNY'), style='B3.TButton')
        czk_btn = ttk.Button(container_o, text='CZK', command=lambda: show_pages('CZK'), style='B3.TButton')
        dnk_btn = ttk.Button(container_o, text='DKK', command=lambda: show_pages('DKK'), style='B3.TButton')
        egp_btn = ttk.Button(container_o, text='EGP', command=lambda: show_pages('EGP'), style='B3.TButton')
        gbp_btn = ttk.Button(container_o, text='GBP', command=lambda: show_pages('GBP'), style='B3.TButton')
        hrk_btn = ttk.Button(container_o, text='HRK', command=lambda: show_pages('HRK'), style='B3.TButton')
        huf_btn = ttk.Button(container_o, text='HUF', command=lambda: show_pages('HUF'), style='B3.TButton')
        inr_btn = ttk.Button(container_o, text='INR', command=lambda: show_pages('INR'), style='B3.TButton')
        jpy_btn = ttk.Button(container_o, text='JPY', command=lambda: show_pages('JPY'), style='B3.TButton')
        krw_btn = ttk.Button(container_o, text='KRW', command=lambda: show_pages('KRW'), style='B3.TButton')
        mdl_btn = ttk.Button(container_o, text='MDL', command=lambda: show_pages('MDL'), style='B3.TButton')
        mxn_btn = ttk.Button(container_o, text='MXN', command=lambda: show_pages('MXN'), style='B3.TButton')
        nok_btn = ttk.Button(container_o, text='NOK', command=lambda: show_pages('NOK'), style='B3.TButton')
        nzd_btn = ttk.Button(container_o, text='NZD', command=lambda: show_pages('NZD'), style='B3.TButton')
        pln_btn = ttk.Button(container_o, text='PLN', command=lambda: show_pages('PLN'), style='B3.TButton')
        rsd_btn = ttk.Button(container_o, text='RSD', command=lambda: show_pages('RSD'), style='B3.TButton')
        rub_btn = ttk.Button(container_o, text='RUB', command=lambda: show_pages('RUB'), style='B3.TButton')
        sek_btn = ttk.Button(container_o, text='SEK', command=lambda: show_pages('SEK'), style='B3.TButton')
        thb_btn = ttk.Button(container_o, text='THB', command=lambda: show_pages('THB'), style='B3.TButton')
        try_btn = ttk.Button(container_o, text='TRY', command=lambda: show_pages('TRY'), style='B3.TButton')
        uah_btn = ttk.Button(container_o, text='UAH', command=lambda: show_pages('UAH'), style='B3.TButton')
        xau_btn = ttk.Button(container_o, text='XAU', command=lambda: show_pages('XAU'), style='B3.TButton')
        xdr_btn = ttk.Button(container_o, text='XDR', command=lambda: show_pages('XDR'), style='B3.TButton')
        zar_btn = ttk.Button(container_o, text='ZAR', command=lambda: show_pages('ZAR'), style='B3.TButton')
        left_btn = ttk.Button(container_o, text='<', command=lambda: move_left(1), style='B4.TButton', width=12)
        right_btn = ttk.Button(container_o, text='>', state=tk.DISABLED, style='Disabled.TButton', width=12)

        # build a list with all buttons
        buttons_list = [aed_btn, aud_btn, bgn_btn, cad_btn, chf_btn, cny_btn, czk_btn, dnk_btn,
                        egp_btn, gbp_btn, hrk_btn, huf_btn, inr_btn, jpy_btn, krw_btn, mdl_btn,
                        mxn_btn, nok_btn, nzd_btn, pln_btn, rsd_btn, rub_btn, sek_btn, thb_btn,
                        try_btn, uah_btn, xau_btn, xdr_btn, zar_btn]

        def init_grid_buttons():
            """
            init grid = grid_forget()
              -> to change the position of a button, first it must be forget from grid
              then put back in his new position (in grid)
            """
            aed_btn.grid_forget()
            aud_btn.grid_forget()
            bgn_btn.grid_forget()
            cad_btn.grid_forget()
            chf_btn.grid_forget()
            cny_btn.grid_forget()
            czk_btn.grid_forget()
            dnk_btn.grid_forget()
            egp_btn.grid_forget()
            gbp_btn.grid_forget()
            hrk_btn.grid_forget()
            huf_btn.grid_forget()
            inr_btn.grid_forget()
            jpy_btn.grid_forget()
            krw_btn.grid_forget()
            mdl_btn.grid_forget()
            mxn_btn.grid_forget()
            nok_btn.grid_forget()

        def init_buttons_poz():
            """
            Place the buttons in their first/initial positions (in grid)
             -> initial position = first 18 buttons in first 18 columns of grid

             obs: change the position of a button means:
                  -> first put/show the buttons in grid(their first position),
                    after apply grid_forget()
                    after put(show) the buttons in their new positions of grid
            """
            row = 0
            left_btn.grid(row=row, column=0, padx=3)
            right_btn.grid(row=row, column=19, padx=3)
            for i in range(1, 19):
                buttons_list[i - 1].grid(row=row, column=i, pady=5)

        def move_left(num):
            """
            ~ Move the buttons to left with 1 position at every click of left button(' < ') ~

            The simplest way to move the buttons to left is having a list with all buttons, and declare a parameter
            that will remember how many position to move.
            First this param ('num') is equal to 1, that means when we press for the first time the '<' button,
            all buttons will change their position with 1 to left (the column value from grid will decrement with 1) .
            When the button will be on first column, after pressing '<' (left button) it won't be show anymore,
            because before redraw buttons on their new position, they will be deleted from grid by init_grid_buttons()
            At every click of the left button('<') the column value for every button will decrement with 1, AND
                the 'num' value will be incremented with 1 at every click
            When we arrive at the last button ('ZAR') the left btn will be DISABLED and the right btn will be ABLE
                -> when that is happen the 'num' will take it's max value (num = 11 )

            :param num: move elem. from list with 'num' positions at left
            """
            row = 0
            global left_btn, right_btn

            init_grid_buttons()

            for i in range(num, num + 19):
                buttons_list[i - 1].grid(row=row, column=abs(i - num), pady=5)

            if num + 19 > 29:
                left_btn = ttk.Button(container_o, text='<', state=tk.DISABLED, style='Disabled.TButton', width=12)
            else:
                left_btn = ttk.Button(container_o, text='<', command=lambda: move_left(num + 1),
                                      style='B4.TButton', width=12)
            left_btn.grid(row=row, column=0)

            right_btn = ttk.Button(container_o, text='>', command=lambda: move_right(num - 1),
                                   style='B4.TButton', width=12)
            right_btn.grid(row=row, column=19)

        def move_right(num):
            """
               ~ Move the buttons to right with 1 position at every click of right button(' > ') ~

                It' s similar with move_left(), but here num is initial 11, and will decrement with 1
                at every clicked of right_btn

               :param num: move elem. from list with 'num' positions at right
               """
            row = 0
            global left_btn, right_btn
            init_grid_buttons()  # here i delete the old buttons from grid (free the grid)

            for i in range(num, num + 20):
                buttons_list[i - 1].grid(row=row, column=abs(i - num), pady=5)

            if num < 1:
                right_btn = ttk.Button(container_o, text='>', state=tk.DISABLED,
                                       style='Disabled.TButton', width=12)
            else:
                right_btn = ttk.Button(container_o, text='>', command=lambda: move_right(num - 1),
                                       style='B4.TButton', width=12)
            right_btn.grid(row=row, column=19)

            left_btn = ttk.Button(container_o, text='<', command=lambda: move_left(num + 1),
                                  style='B4.TButton', width=12)
            left_btn.grid(row=row, column=0)

        # show the initial list of buttons (first 18 buttons):
        init_buttons_poz()


class OnePage(tk.Frame):
    """
    The OnePage class create the graph for every currency.
    Needs the parent(where to show the canvas with graph) and the currency (to know which graph to build)
    -> to build a graph = draw graph using the values from a X currency from the .csv file and the dates (also from
                                                                                                    the same .csv file)

    """

    def __init__(self, parent, currency):
        tk.Frame.__init__(self, parent)

        # show the period running:
        # it's a string variable
        # it' s change when we chose other period to show
        # it's used to show us what period are we seeing on the graph
        global period
        label_show_period = tk.Label(self, text='   ' + period + '   ', font="Helvetica 20 bold italic",
                                     border=3, relief=tk.GROOVE)
        label_show_period.place(x=5, y=5)

        # Title for page:
        label_title = tk.Label(self, text='   Other  Graphs   ', fg="#2C3E50"
                               , font="Impact 20")
        label_title.pack(pady=5)

        fig = plt.figure()
        ax1 = plt.subplot2grid((7, 5), (0, 0), rowspan=4, colspan=5)
        ax2 = plt.subplot2grid((7, 5), (5, 0), rowspan=2, colspan=5)

        current_value = today.currency[currency]

        currency_title = currency + ' Status \n Last Exchange value : ' + current_value + ' RON'

        # this is the .csv file from which will take the values
        # it's a global variable because it can be change to take other .csv file
        #    -> take other .csv file = change the period !!
        global period_to_show

        data = pd.read_csv(period_to_show)
        date = data['date']
        date_day = pd.to_datetime(date)  # converting string to date
        val = data[currency]
        avg_curr = statistics.mean(val)

        # Create a font for ylabel and xlabel on graph
        font = FontProperties()
        font.set_family('serif')
        font.set_name('Times New Roman')
        font.set_style('italic')
        font.set_size('15')

        ax1.clear()
        ax1.plot(date_day, val, marker='o')
        ax1.set_title(currency_title)
        ax1.fill_between(date_day, avg_curr, val, fc='#D6EAF8')
        ax1.axhline(avg_curr, 0.048, color='#AEB6BF', ls='--')
        ax1.set_ylabel('Currency Exchange [RON]', labelpad=20, fontproperties=font)
        labels_ax1 = ax1.get_xticklabels()
        plt.setp(labels_ax1, rotation=30, horizontalalignment='right')

        avgs_list = get_avgs_list(period_to_show)

        barlist = ax2.bar(list_curr, avgs_list)
        labels_ax2 = ax2.get_xticklabels()
        plt.setp(labels_ax2, rotation=45, horizontalalignment='right')
        ax2.set_ylabel('Average  on \n period ', font=font, labelpad=25)
        barlist[dict_curr[currency]].set_color('r')

        plt.subplots_adjust(left=0.07, bottom=0.071, right=0.988, top=0.902, wspace=0.2, hspace=0.2)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='white')

        # Credit for BNR (it' s a must, i take currencies from their free ste :))
        label_text_credit_bnr = tk.Label(self,
                                         text='© all currencies are from National Bank of Romania site where you can '
                                              'find all ofthem, for free, check their site: '
                                              'https://www.bnr.ro/Cursul-de-schimb-524.aspx    ',
                                         bg='white', fg='#9F6F5C', font='Belligerent 8')
        label_text_credit_bnr.pack(side=tk.BOTTOM, anchor='se')

        def create_account():
            def add_user_in_database():

                if len(phone_entry.get()) != 10:
                    messagebox.showerror("ERROR", 'The Phone number must have 10 characters !')
                else:
                    # create a databases or connect to one
                    with sqlite3.connect('user_account.db') as db:
                        # create cursor
                        cursor = db.cursor()

                        cursor.execute("SELECT MAX(user_id) + 1 FROM users")
                        last_user_id = cursor.fetchone()[0]
                        db.commit()

                        # select all data from table
                        cursor.execute(
                            "INSERT INTO users VALUES (:u_id, :f_name_box, :l_name_box, :mail_box, :phone_box)",
                            {
                                'u_id': last_user_id,
                                'f_name_box': f_name_entry.get(),
                                'l_name_box': l_name_entry.get(),
                                'mail_box': e_mail_create_entry.get(),
                                'phone_box': phone_entry.get()
                            })

                        db.commit()

                    # Clear the boxes
                    f_name_entry.delete(0, tk.END)
                    l_name_entry.delete(0, tk.END)
                    e_mail_create_entry.delete(0, tk.END)
                    phone_entry.delete(0, tk.END)

            window = tk.Tk()
            window.title("Add")
            window.geometry("200x300")
            window.resizable(0, 0)

            # declare elem:
            title_label = tk.Label(window, text="Add an account ")
            f_name_label = tk.Label(window, text="First Name")
            f_name_entry = ttk.Entry(window)
            l_name_label = tk.Label(window, text='Last Name')
            l_name_entry = ttk.Entry(window)
            e_mail_create_label = tk.Label(window, text='E-mail')
            e_mail_create_entry = ttk.Entry(window)
            phone_label = tk.Label(window, text='Phone')
            phone_entry = ttk.Entry(window)
            password_label = tk.Label(window, text='Password')
            password_entry = ttk.Entry(window)

            # grid elem:
            title_label.grid(row=0, column=0, columnspan=2)
            f_name_label.grid(row=1, column=0)
            f_name_entry.grid(row=1, column=1)
            l_name_label.grid(row=2, column=0)
            l_name_entry.grid(row=2, column=1)
            e_mail_create_label.grid(row=3, column=0)
            e_mail_create_entry.grid(row=3, column=1)
            phone_label.grid(row=4, column=0)
            phone_entry.grid(row=4, column=1)
            password_label.grid(row=5, column=0)
            password_entry.grid(row=5, column=1)

            # Create and grid the buttons
            add_user_btn = ttk.Button(window, text='Create Account', command=add_user_in_database)
            add_user_btn.grid(row=6, column=0, columnspan=2)

            window.mainloop()

        def check_sign_in(e_mail, password):

            global database_user_logged, e_mail_user_logged
            e_mail_user_logged = e_mail

            with sqlite3.connect('user_account.db') as db:
                cursor = db.cursor()
                cursor.execute("Select e_mail, user_password, first_name, last_name from Users")
                records = cursor.fetchall()
                db.commit()

            check = 0

            for record in records:
                if e_mail == str(record[0]) and password == str(record[1]):
                    database_user_logged = str(record[2]) + ' ' + str(record[3])
                    App.frames[Account].__init__(parent, self)
                    check = 1
                    break
                else:
                    check = 0

            if e_mail == '' or password == '' or check == 0:
                messagebox.showerror('Error to connect', 'Wrong Username or Password')
            else:
                App.frames[UserExchangesPage].__init__(parent, controller)
                controller.show_frame(StartPage)

        # Title for page:
        label_title = tk.Label(self, text='   Login Page  ', fg="#0B2783"
                               , font="Impact 22", bg='#FEFEFE')
        label_title.pack(pady=5)
        label_title = tk.Label(self, text='-   Please login to start   -', fg="#6495ED"
                               , font="College 19 italic", bg='#FEFEFE')
        label_title.pack(pady=5)

        # Here i created the canvas with the representative blurry background for login window:

        canvas_width = self.winfo_screenwidth()
        canvas_height = self.winfo_screenheight()

        canvas_bg_img = tk.Canvas(self, height=277, width=472, borderwidth=0, highlightthickness=0, relief=tk.RAISED)
        canvas_bg_img.place(x=canvas_width / 2 - 236, y=canvas_height / 2 - 201)
        usd_img = Image.open('images\\blurr.jpg')
        canvas_bg_img.image = ImageTk.PhotoImage(usd_img.resize((472, 277), Image.ANTIALIAS))
        canvas_bg_img.create_image(0, 0, image=canvas_bg_img.image, anchor='nw')

        # Create a a canvas with white color as background for login menu:
        white_canvas = tk.Frame(self, bg='white')
        white_canvas.place(x=canvas_width / 2 - 235, y=canvas_height / 2 - 200)

        """
        row=0 -> empty row
        row=1 -> E-mail (label + entry)
        row=2 -> Password: (label + entry)
        row=3 -> Sign_in button
        row=4 -> Create_account button

       ### tables from database : 
        CREATE TABLE  Users (
                user_id integer PRIMARY KEY,
                first_name text,
                last_name text,
                e_mail text,
                phone text
                user_password text)

        CREATE TABLE  bank_cards (
                    card_id integer PRIMARY KEY,
                    user_id integer,
                    card_number text,
                    expiration_date text,
                    full_name text,
                    cvv_code integer)
        """

        # declare elements:
        empty_row = tk.Label(white_canvas, text='                   ', bg='white', bd=0)
        empty_row2 = tk.Label(white_canvas, text='    ', bg='white', width=5, bd=0)
        empty_col1 = tk.Label(white_canvas, bg='white', fg='white', bd=0)
        empty_col2 = tk.Label(white_canvas, bg='white', fg='white', bd=0)
        e_mail_login_label = tk.Label(white_canvas, text='E-mail:', bg='white',
                                      font="Helvetica 17 bold italic", bd=0)
        e_mail_login_entry = ttk.Entry(white_canvas, width=25, font="Tahoma 17 italic")
        password_login_label = tk.Label(white_canvas, text=' Password:', bg='white',
                                        font="Helvetica 15 bold italic", bd=0)
        password_login_entry = ttk.Entry(white_canvas, show='*', width=25, font="Tahoma 17 italic")
        styl_1 = ttk.Style()
        styl_1.theme_use('default')
        styl_1.configure('B1.TButton', font=('College', 18, 'bold'), background='#3457F5', foreground='white')
        styl_1.map('B1.TButton', background=[('active', '#1840F7')])

        styl_2 = ttk.Style()
        styl_2.theme_use('default')
        styl_2.configure('B2.TButton', font=('College', 15, 'bold'), background='#F9EA3D', foreground='#353102')
        styl_2.map('B2.TButton', background=[('active', '#F4E322')])

        styl_forgot_pass = ttk.Style()
        styl_forgot_pass.theme_use('default')
        styl_forgot_pass.configure('B_forgot_pass.TButton', font=('Nottingham', 10, 'italic'), background='white',
                                   foreground='blue', borderwidth=0)
        styl_forgot_pass.map('B_forgot_pass.TButton', background=[('active', '#E6F7F7')], borderwidth=[('active', '0')])

        sign_in_btn = ttk.Button(white_canvas, text='Sign in', style="B1.TButton",
                                 command=lambda: check_sign_in(e_mail_login_entry.get(), password_login_entry.get()))

        create_account_btn = ttk.Button(white_canvas, text='Create an Account',
                                        command=create_account, style="B2.TButton")

        line_label = tk.Label(white_canvas, text='------------------------------------------------------------------',
                              fg='gray', bg='white', width=50)

        forgot_password_btn = ttk.Button(white_canvas, text="  Forgot password  ?  ", style="B_forgot_pass.TButton",
                                         command=pop_up_msg)

        # init positions for elements on grid:
        empty_row.grid(row=0, column=1, columnspan=3, ipadx=200)
        empty_col1.grid(row=0, column=0, rowspan=7)
        empty_col2.grid(row=0, column=3, rowspan=7)
        e_mail_login_label.grid(row=1, column=1)
        e_mail_login_entry.grid(row=1, column=2, ipady=5)
        password_login_label.grid(row=2, column=1)
        password_login_entry.grid(row=2, column=2, ipady=5)
        sign_in_btn.grid(row=3, column=1, columnspan=3, ipady=5, pady=5, ipadx=155, padx=5)
        forgot_password_btn.grid(row=4, column=1, columnspan=3)
        line_label.grid(row=5, column=1, columnspan=3)
        create_account_btn.grid(row=6, column=0, columnspan=4, ipady=5, ipadx=30)
        empty_row2.grid(row=7, column=1, columnspan=3, ipadx=200)


class UserExchangesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def change_card():

            def cancel():
                right_title['text'] = 'Credit card'

                # Hide the unused elements:
                new_card_canvas.pack_forget()
                new_data_frame.place_forget()

                # Show the old elements:
                canvas_bg_img.pack()
                sw_card_btn.pack(side=tk.BOTTOM, ipadx=190, ipady=20)

            def save_data_card():

                if expiration_date_entry.get() == '' or new_full_name_entry.get() == '' \
                        or new_cvv_entry.get() == '' or new_card_number_entry.get() == '':
                    messagebox.showerror('Error ', 'Fill all the white spaces !')
                elif new_full_name_entry.get() == '' \
                        or len(new_cvv_entry.get()) != 3 or len(new_card_number_entry.get()) != 16:
                    messagebox.showerror('Error ', 'Wrong values :( !')
                elif len(expiration_date_entry.get()) < 3 or len(expiration_date_entry.get()) > 5 or \
                        str(expiration_date_entry.get()).count('/') == 0:
                    messagebox.showerror('Error ', 'Wrong expiration date  :( !')
                else:
                    right_title['text'] = 'Credit card'

                    # Hide the unused elements:
                    new_card_canvas.pack_forget()
                    new_data_frame.place_forget()

                    # Show the used elements:
                    new_card_number = new_card_number_entry.get()
                    new_card_number_formated = new_card_number[0:4] + ' ' + new_card_number[
                                                                            4:8] + ' ' + new_card_number[
                                                                                         8:12] + ' ' + new_card_number[
                                                                                                       12:16]
                    new_exp_date = expiration_date_entry.get()
                    new_full_name = new_full_name_entry.get()
                    new_cvv_code = new_cvv_entry.get()

                    num_card_label['text'] = new_card_number_formated
                    db_date_label['text'] = new_exp_date
                    db_name_label['text'] = new_full_name.upper()
                    cvv_number_label['text'] = new_cvv_code

                    canvas_bg_img.pack()
                    sw_card_btn.pack(side=tk.BOTTOM, ipadx=190, ipady=20)

            # Destroy the unused elements:
            canvas_bg_img.pack_forget()
            sw_card_btn.pack_forget()

            # Create the used elements:
            styl_save_card = ttk.Style()
            styl_save_card.theme_use('default')
            styl_save_card.configure('Save_Card.TButton', font=('Verdana', 20, 'bold'),
                                     background='#AC96E9', foreground='white')
            styl_save_card.map('Save_Card.TButton', background=[('active', '#5C38BE')])

            right_title['text'] = 'Change Card'
            new_card_canvas = tk.Canvas(banking_cards_frame, height=310, width=450, borderwidth=0,
                                        highlightthickness=0, relief=tk.RAISED)
            new_card_canvas.pack()
            new_card_img = Image.open('images\\card_face.jpg')
            new_card_canvas.image = ImageTk.PhotoImage(new_card_img.resize((445, 310), Image.ANTIALIAS))
            new_card_canvas.create_image(0, 0, image=new_card_canvas.image, anchor='nw')

            new_data_frame = tk.Frame(banking_cards_frame, bg='#9377E1')
            new_data_frame.place(relwidth=1, relheight=0.57, rely=0.495, relx=0.0)

            new_data_frame.rowconfigure(7, weight=1)

            subtitle_label = tk.Label(new_data_frame, text='write  the  card  details :',
                                      font='Pristina 21 bold italic',
                                      fg='#9377E1', bg='#CFCEBA', width=32)

            empty_row1_for_space = tk.Label(new_data_frame, text=' ', bg='#9377E1', fg='#9377E1', font='Verdana 25')
            empty_row2_for_space = tk.Label(new_data_frame, text=' ', bg='#9377E1', fg='#9377E1', font='Verdana 25')

            new_card_number_label = tk.Label(new_data_frame, text='Card number', font='Verdana 15 bold',
                                             fg='white', bg='#9377E1')
            new_card_number_entry = ttk.Entry(new_data_frame, width=25, font="Tahoma 15 italic")

            expiration_date_label = tk.Label(new_data_frame, text='Expiration date', font='Verdana 15 bold',
                                             fg='white', bg='#9377E1')
            expiration_date_entry = ttk.Entry(new_data_frame, width=25, font="Tahoma 15 italic")

            new_full_name_label = tk.Label(new_data_frame, text='Full name', font='Verdana 15 bold',
                                           fg='white', bg='#9377E1')
            new_full_name_entry = ttk.Entry(new_data_frame, width=25, font="Tahoma 15 italic")

            new_cvv_label = tk.Label(new_data_frame, text='CVV code', font='Verdana 15 bold',
                                     fg='white', bg='#9377E1')
            new_cvv_entry = ttk.Entry(new_data_frame, width=25, font="Tahoma 15 italic")

            subtitle_label.grid(row=0, column=0, columnspan=2)
            empty_row1_for_space.grid(row=1, column=1, columnspan=2)
            new_card_number_label.grid(row=2, column=0)
            new_card_number_entry.grid(row=2, column=1)
            expiration_date_label.grid(row=3, column=0)
            expiration_date_entry.grid(row=3, column=1)
            new_full_name_label.grid(row=4, column=0)
            new_full_name_entry.grid(row=4, column=1)
            new_cvv_label.grid(row=5, column=0)
            new_cvv_entry.grid(row=5, column=1)
            empty_row2_for_space.grid(row=6, column=1, columnspan=2)

            save_card_btn = ttk.Button(new_data_frame, text='Continue',
                                       style="Save_Card.TButton", command=save_data_card)
            save_card_btn.grid(row=7, column=0, ipadx=14, pady=10)
            cancel_btn = ttk.Button(new_data_frame, text='Cancel', style="Save_Card.TButton", command=cancel)
            cancel_btn.grid(row=7, column=1, ipadx=40, padx=0, pady=10)

        # Here i get the Credit Card values:

        if database_user_logged != 'user database':
            with sqlite3.connect('user_account.db') as db:
                cursor = db.cursor()

                cursor.execute("Select user_id FROM Users WHERE e_mail= " + "'" + e_mail_user_logged + "'")
                user_id_from_users = cursor.fetchone()[0]

                cursor.execute("""
                                         Select card_number, expiration_date, full_name, cvv_code 
                                         FROM bank_cards 
                                         WHERE user_id= """ + str(user_id_from_users))

                credit_card_values = cursor.fetchone()

                card_number = credit_card_values[0]
                card_number_formated = card_number[0:4] + ' ' + card_number[4:8] + ' ' + card_number[
                                                                                         8:12] + ' ' + card_number[
                                                                                                       12:16]
                exp_date = credit_card_values[1]
                full_name = credit_card_values[2]
                cvv_code = credit_card_values[3]

                db.commit()

        left_title = tk.Label(self, text='   Last Exchanges  ', fg="#2C3E50", font="Impact 20")
        exchanges_root_frame = tk.Frame(self, bg='white', border=3, relief=tk.RAISED)
        banking_cards_frame = tk.Frame(self, bg='#83D7F3', relief=tk.SUNKEN)
        right_title = tk.Label(banking_cards_frame, text='Credit card', fg='#34495E', bg='#CCCCFF', font="Impact 20")

        status_root = tk.Label(self, text='Status: ', fg='black', font='Rockwell 20 bold italic underline')
        status_root.place(x=1200, y=12)

        status_check = tk.Label(self, text='OFFLINE' if database_user_logged == 'user database' else 'ONLINE'
                                , fg='#EA140D' if database_user_logged == 'user database' else '#54F910'
                                , font='Rockwell 19 bold')
        status_check.place(x=1295, y=13)

        if status_check['text'] == 'OFFLINE':
            lock_canvas_black = tk.Canvas(self, height=200, width=200, borderwidth=0,
                                          highlightthickness=0, relief=tk.RAISED)
            lock_canvas_black.place(x=400, y=340)
            lock_img = Image.open('images\\lock.jpg')
            lock_canvas_black.image = ImageTk.PhotoImage(lock_img.resize((200, 220), Image.ANTIALIAS))
            lock_canvas_black.create_image(0, 0, image=lock_canvas_black.image, anchor='nw')

            lock_black_frame = tk.Frame(lock_canvas_black, bg='black')
            lock_black_frame.place(relwidth=0.5, relheight=0.4, rely=0.56, relx=0.27)
            text_lock = tk.Label(lock_black_frame, text='- Please -\n Login ', font='College 15', bg='black',
                                 fg='white')
            text_lock.pack()

        left_title.place(x=400, y=10)
        right_title.pack(side=tk.TOP, ipadx=190)
        exchanges_root_frame.place(relwidth=0.64, relheight=0.90, rely=0.08, relx=0.02)
        banking_cards_frame.place(relwidth=0.29, relheight=0.884, rely=0.09, relx=0.713)

        # Card image:
        canvas_bg_img = tk.Canvas(banking_cards_frame, height=608, width=485, borderwidth=0, highlightthickness=0,
                                  relief=tk.RAISED)
        canvas_bg_img.pack()
        card_img = Image.open('images\\card.jpg')
        canvas_bg_img.image = ImageTk.PhotoImage(card_img.resize((485, 608), Image.ANTIALIAS))
        canvas_bg_img.create_image(0, 0, image=canvas_bg_img.image, anchor='nw')

        # Here will be created the labels to be put on the credit card :
        num_card_label = tk.Label(banking_cards_frame, text='' if database_user_logged == 'user database'
        else card_number_formated, fg='#F6F9E5',
                                  bg='#919497', font=('College', 18))

        exp_fix_label = tk.Label(banking_cards_frame, text='EXP ', fg='#353434', bg='#919497', font=('Impact', 12))

        db_date_label = tk.Label(banking_cards_frame, text='' if database_user_logged == 'user database' else exp_date,
                                 fg='#F6F9E5', bg='#919497', font=('College', 14))

        db_name_label = tk.Label(banking_cards_frame, text='' if database_user_logged == 'user database'
        else full_name, fg='#F6F9E5', bg='#919497', font=('College', 15))

        cvv_number_label = tk.Label(banking_cards_frame, text='' if database_user_logged == 'user database'
        else cvv_code, fg='black', bg='white', font='Rockwell 17 italic')

        num_card_label.place(x=70, y=205, width=300)
        exp_fix_label.place(x=180, y=250)
        db_date_label.place(x=220, y=250)
        db_name_label.place(x=70, y=300)
        cvv_number_label.place(x=341, y=463)

        # Create buttons to change the actual credit card | to unpack | to pack:

        styl_sw_card = ttk.Style()
        styl_sw_card.theme_use('default')
        styl_sw_card.configure('Sw_card.TButton', font=('College', 18, 'bold italic'), background='#38B6E7',
                               foreground='white')
        styl_sw_card.map('Sw_card.TButton', background=[('active', '#1840F7')])

        styl_pack = ttk.Style()
        styl_pack.theme_use('default')
        styl_pack.configure('pack.TButton', font=('College', 12, 'bold'), background='#F2F7F7', foreground='black')
        styl_pack.map('pack.TButton', background=[('active', '#73B1AE')])

        sw_card_btn = ttk.Button(banking_cards_frame, text='Change credit card',
                                 style="Sw_card.TButton", command=change_card,
                                 state=tk.DISABLED if database_user_logged == 'user database' else tk.NORMAL)
        sw_card_btn.pack(side=tk.BOTTOM, ipadx=190, ipady=20)

        def do_pack():
            exchanges_root_frame.place_forget()
            banking_cards_frame.place_forget()
            pack_btn.place_forget()

            # The white table Columns must be grid_forget and after  grid again with a new ipdax (width):
            source_iban.grid_forget()
            exchange_from.grid_forget()
            exchange_in.grid_forget()
            new_value.grid_forget()
            date.grid_forget()
            time.grid_forget()

            source_iban.grid(row=0, column=1, pady=10, padx=5, ipadx=130)
            exchange_from.grid(row=0, column=2, pady=10, padx=5, ipadx=60)
            exchange_in.grid(row=0, column=3, pady=10, padx=5, ipadx=55)
            new_value.grid(row=0, column=4, pady=10, padx=5, ipadx=50)
            date.grid(row=0, column=5, pady=10, padx=5, ipadx=50)
            time.grid(row=0, column=6, pady=10, padx=5, ipadx=65)

            exchanges_root_frame.place(relwidth=0.94, relheight=0.90, rely=0.08, relx=0.02)
            unpack_btn.place(relwidth=0.018, relheight=0.884, rely=0.09, relx=0.98)

        def do_unpack():
            exchanges_root_frame.place_forget()
            banking_cards_frame.place_forget()
            unpack_btn.place_forget()

            # The white table Columns must be grid_forget and after  grid again with a new ipdax (width):
            source_iban.grid_forget()
            exchange_from.grid_forget()
            exchange_in.grid_forget()
            new_value.grid_forget()
            date.grid_forget()
            time.grid_forget()

            source_iban.grid(row=0, column=1, pady=10, padx=5, ipadx=80)
            exchange_from.grid(row=0, column=2, pady=10, padx=5, ipadx=20)
            exchange_in.grid(row=0, column=3, pady=10, padx=5, ipadx=20)
            new_value.grid(row=0, column=4, pady=10, padx=5, ipadx=20)
            date.grid(row=0, column=5, pady=10, padx=5, ipadx=20)
            time.grid(row=0, column=6, pady=10, padx=5, ipadx=20)

            exchanges_root_frame.place(relwidth=0.64, relheight=0.90, rely=0.08, relx=0.02)
            banking_cards_frame.place(relwidth=0.29, relheight=0.884, rely=0.09, relx=0.713)
            pack_btn.place(relwidth=0.018, relheight=0.884, rely=0.09, relx=0.694)

        pack_btn = ttk.Button(self, text='>', style="pack.TButton", command=do_pack)
        pack_btn.place(relwidth=0.018, relheight=0.884, rely=0.09, relx=0.694)

        unpack_btn = ttk.Button(self, text='<', style="pack.TButton", command=do_unpack)

        """ Create the scrollbar """
        bg_canvas = tk.Canvas(exchanges_root_frame, bg='white')
        bg_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(exchanges_root_frame, orient=tk.VERTICAL, command=bg_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        bg_canvas.configure(yscrollcommand=scrollbar.set)
        bg_canvas.bind('<Configure>', lambda e: bg_canvas.configure(scrollregion=bg_canvas.bbox("all")))

        # Create another FRAME inside the canvas:
        exchanges_frame = tk.Frame(bg_canvas, bg='white')
        # Add the new frame as window in canvas:
        bg_canvas.create_window((0, 0), window=exchanges_frame, anchor='nw')

        # Create the elements on the first row (title elements):
        count_label = tk.Label(exchanges_frame, text="No", fg='red', bg='white', font='Verdana 12 bold italic')
        source_iban = tk.Label(exchanges_frame, text="Source IBAN \n  [RON] ", fg='red', bg='white',
                               font='Verdana 12 bold italic')
        exchange_from = tk.Label(exchanges_frame, text="Amount \n  [RON] ", fg='red', bg='white',
                                 font='Verdana 12 bold italic')
        exchange_in = tk.Label(exchanges_frame, text="Exchange \n  in", fg='red', bg='white',
                               font='Verdana 12 bold italic')
        new_value = tk.Label(exchanges_frame, text="New \n  Amount", fg='red', bg='white',
                             font='Verdana 12 bold italic')
        date = tk.Label(exchanges_frame, text="Date", fg='red', bg='white', font='Verdana 12 bold italic')
        time = tk.Label(exchanges_frame, text="Time", fg='red', bg='white', font='Verdana 12 bold italic')

        count_label.grid(row=0, column=0, pady=10, padx=5)
        source_iban.grid(row=0, column=1, pady=10, padx=5, ipadx=80)
        exchange_from.grid(row=0, column=2, pady=10, padx=5, ipadx=20)
        exchange_in.grid(row=0, column=3, pady=10, padx=5, ipadx=20)
        new_value.grid(row=0, column=4, pady=10, padx=5, ipadx=20)
        date.grid(row=0, column=5, pady=10, padx=5, ipadx=20)
        time.grid(row=0, column=6, pady=10, padx=5, ipadx=20)

        for i in range(1, 101):
            label_no = tk.Label(exchanges_frame, text=str(i), fg='black', bg='white', font='Verdana 7 bold')
            label_no.grid(row=i, column=0)


class Account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def user_log_out():
            global database_user_logged
            database_user_logged = 'user database'
            App.show_frame(StartPage)
            App.frames[Account].__init__(parent, controller)
            App.frames[UserExchangesPage].__init__(parent, controller)

        self.configure(bg='#FFFFCE', borderwidth=1, relief=tk.RAISED)

        lab = tk.Label(self, text="                                               ", bg='#EBEEEE', fg='white', width=46)
        lab.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        top_left_frame = tk.Frame(self, bg='#FFFFCE', width=90, height=90)
        top_left_frame.grid(row=1, column=0, padx=0, pady=0)

        top_right_frame = tk.Frame(self, bg='#FFFFCE', width=90, height=90)
        top_right_frame.grid(row=1, column=1, padx=0, pady=0)

        canvas_profile_img = tk.Canvas(top_left_frame, bg='#FFFFCE', height=90, width=90,
                                       borderwidth=0, highlightthickness=0)
        canvas_profile_img.grid(row=2, column=0, padx=0, pady=2)

        # Here i create (prepare) the images for the buttons
        switch_account_image_open = Image.open("images\\switch_img.jpg")
        switch_account_image_resize = switch_account_image_open.resize((30, 20), Image.ANTIALIAS)
        switch_account_img = ImageTk.PhotoImage(switch_account_image_resize)

        settings_image_open = Image.open("images\\setting_img.jpg")
        settings_image_resize = settings_image_open.resize((30, 20), Image.ANTIALIAS)
        settings_img = ImageTk.PhotoImage(settings_image_resize)

        help_image_open = Image.open("images\\help_img.jpg")
        help_image_resize = help_image_open.resize((30, 20), Image.ANTIALIAS)
        help_img = ImageTk.PhotoImage(help_image_resize)

        feedback_image_open = Image.open("images\\feedback_img.jpg")
        feedback_image_resize = feedback_image_open.resize((30, 20), Image.ANTIALIAS)
        feedback_img = ImageTk.PhotoImage(feedback_image_resize)

        log_out_image_open = Image.open("images\\log_out_img.jpg")
        log_out_image_resize = log_out_image_open.resize((30, 20), Image.ANTIALIAS)
        log_out_img = ImageTk.PhotoImage(log_out_image_resize)

        # Create stiles for buttons:
        styl_6 = ttk.Style()
        styl_6.theme_use('default')
        styl_6.configure('B6.TButton', font=('College', 10, 'bold italic'), background='#FFFFCE', foreground='#49443F',
                         borderwidth=0)
        styl_6.map('B6.TButton', background=[('active', '#BDBDBD')])

        styl_7 = ttk.Style()
        styl_7.theme_use('default')
        styl_7.configure('B7.TButton', font=('College', 15, 'bold'), background='#FFFFCE', foreground='black',
                         borderwidth=0)
        styl_7.map('B7.TButton', background=[('active', '#BDBDBD')])

        global database_user_logged
        image = Image.open('images\\wh_me2.jpeg' if database_user_logged == 'Radu Tiperciuc'
                           else 'images\\unknow_user.jpg')
        canvas_profile_img.image = ImageTk.PhotoImage(image.resize((90, 90), Image.ANTIALIAS))
        canvas_profile_img.create_image(0, 0, image=canvas_profile_img.image, anchor='nw')

        username_label = tk.Label(top_right_frame, text=database_user_logged, bg='#FFFFCE', font=('Calibri', 20))
        see_exchanges_btn = ttk.Button(top_right_frame, text='See your last exchanges..', style='B6.TButton',
                                       command=lambda: App.show_frame(UserExchangesPage))

        # Here i grid the elements from the first frame (profile_frame):
        username_label.grid(column=1, row=0)
        see_exchanges_btn.grid(column=1, row=1)

        # Here i declared the elements for second frame:
        separate_line1 = tk.Label(self,
                                  text='----------------------------------------------------------------',
                                  bg='#FFFFCE')
        change_account_btn = ttk.Button(self, image=switch_account_img, text='Change Account', style='B7.TButton',
                                        width=32, compound="left", command=lambda: App.show_frame(LoginPage))
        settings_btn = ttk.Button(self, image=settings_img, text='_Settings', style='B7.TButton',
                                  width=32, compound="left")
        help_btn = ttk.Button(self, image=help_img, text='Help', style='B7.TButton',
                              width=32, compound="left")
        separate_line2 = tk.Label(self,
                                  text='----------------------------------------------------------------',
                                  bg='#FFFFCE')
        feedback_btn = ttk.Button(self, image=feedback_img, text='Send feedback ', style='B7.TButton',
                                  width=32, compound="left")

        log_out_btn = ttk.Button(self, image=log_out_img, text='Log out', style='B7.TButton',
                                 width=32, compound="left", command=user_log_out)

        # Here i pack the elements from second frame (buttons_frame):
        separate_line1.grid(row=3, column=0, columnspan=2)
        change_account_btn.grid(row=4, column=0, columnspan=2)
        settings_btn.grid(row=5, column=0, columnspan=2)
        help_btn.grid(row=6, column=0, columnspan=2)
        separate_line2.grid(row=7, column=0, columnspan=2)
        feedback_btn.grid(row=8, column=0, columnspan=2)
        log_out_btn.grid(row=9, column=0, columnspan=2, pady=2)


App = ExchangeCapp()
width = App.winfo_screenwidth()
height = App.winfo_screenheight()
# setting tkinter window size
App.geometry("%dx%d+0+0" % (width, height))
App.mainloop()

# Exchange the right moment
