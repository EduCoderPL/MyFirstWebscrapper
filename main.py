import time
from threading import Thread
from bs4 import BeautifulSoup
from requests import get
from tkinter import *
from tkinter import ttk
import os
import re

import webbrowser


def main():

    def clear_table():
        tv.delete(*tv.get_children())


    isWebscrapRun = False

    def parse_price(priceText):
        if "Za darmo" in priceText:
            return priceText
        return float(priceText.
                     replace(" ", "").
                     replace("zł", "").
                     replace(",", ".").
                     replace("donegocjacji", ""))

    def parse_page(number):
        URL = websiteEntry.get()
        textLabel.config(text=f"Ogarniam stronę: {number}")
        page = get(f"{URL}?page={number}")
        bs = BeautifulSoup(page.content, "html.parser")
        for offer in bs.find_all("div", class_="css-19ucd76"):
            try:
                title = offer.find("h6", class_="css-v3vynn-Text eu5v0x0").get_text().strip()

                footer = offer.find("p", class_="css-p6wsjo-Text eu5v0x0").get_text().strip()
                location = re.split('- ', footer)

                price = offer.find("p", class_="css-wpfvmn-Text eu5v0x0").get_text().strip()
                getURL = offer.find("a")['href']

                offerURL = check_if_otodom(getURL)

                tv.insert("", "end", values=(title, location[0], parse_price(price), offerURL))
            except Exception as e:
                print(e)
        textLabel.config(text=f"Webscrapping finished.")

    def check_if_otodom(getURL):
        return getURL if "otodom" in getURL else f"https://www.olx.pl{getURL}"

    # python main.py setup
    def webscrap(first: int, last: int):
        assert first <= last, "First argument must be less or equal second"
        global isWebscrapRun
        isWebscrapRun = True
        button['state'] = DISABLED
        buttonText.set("Webscrapping in progress")
        clear_table()


        for page in range(first, last + 1):
            parse_page(page)

        isWebscrapRun = False
        button['state'] = NORMAL
        buttonText.set("Use Webscrapper")

    def execute_webscrapping():
        if not isWebscrapRun:
            Thread(target=webscrap, args=(1, 8), daemon=True).start()

    def select_item_threaded():
        Thread(target=select_item).start()

    def select_item():
        selectedItems = tv.selection()
        if len(selectedItems) > 10:
            if messagebox.askokcancel("Dużo kart", f"Wybrałeś {len(selectedItems)} kart do otwarcia. Kontynuować?"):
                open_URL_from_table(selectedItems)
        else:
            open_URL_from_table(selectedItems)

    def open_URL_from_table(selectedItems):
        for item in selectedItems:
            webbrowser.open_new_tab(tv.item(item)["values"][3])

    window = Tk()
    window.maxsize(1280, 800)
    window.minsize(1280, 800)

    buttonFrame = Frame(window, bd=5, padx=10, pady=10)
    buttonText = StringVar()
    buttonText.set("Use Webscrapper")
    button = Button(buttonFrame,
                    text="Use Webscrapper",
                    command=
                    execute_webscrapping,
                    font=("Comic Sans", 18),
                    fg="#00FF00",
                    bg="black",
                    activeforeground="#00DD00",
                    activebackground="#393939",  #
                    state=ACTIVE,  # ACTIVE, DISABLED - czy przycisk jest aktywny, czy nie
                    compound="top",
                    width=25,
                    textvariable=buttonText,
                    )
    button2 = Button(buttonFrame,
                     text="Open selected websites",
                     command=select_item_threaded,
                     font=("Comic Sans", 18),
                     fg="#00FF00",
                     bg="black",
                     activeforeground="#00DD00",
                     activebackground="#393939",  #
                     state=ACTIVE,  # ACTIVE, DISABLED - czy przycisk jest aktywny, czy nie
                     compound="top",
                     width=25,
                     )

    button.pack(side=LEFT)
    button2.pack(side=RIGHT)

    frame = Frame(window, padx=20, pady=20)

    tv = ttk.Treeview(frame, columns=(1, 2, 3, 4), show="headings", height=20)
    tv.pack()
    tv.heading(1, text="Tytuł ogłoszenia")
    tv.heading(2, text="Lokalizacja")
    tv.heading(3, text="Cena")
    tv.heading(4, text="url")

    textFrame = Frame(window, padx=10, pady=10, bd=5)
    textLabel = Label(textFrame, text="ELO", font=("Comic Sans", 18))
    textLabel.pack()

    websiteFrame = Frame(window, padx=10, pady=10, bd=5)
    websiteFrame.pack()
    websiteEntry = Entry(websiteFrame,
                         font=("Arial", 18),
                         width=50,
                         fg="#00FF00",
                         bg="black",
                         bd=5
                         )
    websiteEntry.insert(0, "https://www.olx.pl/d/muzyka-edukacja/materialy-jezykowe/")

    websiteEntry.pack()

    frame.pack()
    textFrame.pack()

    buttonFrame.pack()
    # listbox = Listbox(window,
    #                   bg = "#CCCCCC",
    #                   font=("Constantia", 12),
    #                   width=120,
    #                   height=30,
    #                   selectmode=MULTIPLE)
    # listbox.pack()
    from tkinter import messagebox

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()


    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()
    quit()

if __name__ == "__main__":
    main()



