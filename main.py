from threading import Thread
from bs4 import BeautifulSoup
from requests import get
from tkinter import *
from tkinter import ttk
import os
import re

import webbrowser

def main():
    def parse_price(priceText):
        return float(priceText.
                     replace(" ", "").
                     replace("zł", "").
                     replace(",", ".").
                     replace("donegocjacji", ""))

    def parse_page(number):
        textLabel.config(text=f"Ogarniam stronę: {number}")
        page = get(f"{URL}?page={number}")
        bs = BeautifulSoup(page.content, "html.parser")
        for offer in bs.find_all("div", class_="css-19ucd76"):
            try:
                footer = offer.find("p", class_="css-p6wsjo-Text eu5v0x0").get_text().strip()

                location = re.split('- |, ', footer)
                title = offer.find("h6", class_="css-v3vynn-Text eu5v0x0").get_text().strip()
                price = offer.find("p", class_="css-wpfvmn-Text eu5v0x0").get_text().strip()
                getURL = offer.find("a")['href']
                if "otodom" in getURL:
                    offerURL = getURL
                else:
                    offerURL = f"https://www.olx.pl{getURL}"

                tv.insert("", "end", values=(title, location[1], parse_price(price), offerURL))
            except Exception as e:
                print(offer)
                print(e)
        textLabel.config(text=f"Webscrapping zakończony.")
    # python main.py setup
    def webscrap(first: int, last: int):
        assert first <= last, "First argument must be less or equal second"

        for page in range(first, last + 1):
            parse_page(page)

    def execute_webscrapping():
        Thread(target=webscrap, args=(1, 3)).start()

    def select_item():
        selectedItems = tv.selection()
        if len(selectedItems) > 10:
            if messagebox.askokcancel("Dużo kart", f"Wybrałeś {len(selectedItems)} kart do otwarcia. Kontynuować?"):
                for item in selectedItems:
                    print(tv.item(item)["values"][3])
                    webbrowser.open_new_tab(tv.item(item)["values"][3])
        else:
            for item in selectedItems:
                print(tv.item(item)["values"][3])
                webbrowser.open_new_tab(tv.item(item)["values"][3])

    if os.path.exists("dane.db"):
        os.remove("dane.db")

    URL = "https://www.olx.pl/d/nieruchomosci/stancje-pokoje/krakow/"
    window = Tk()
    window.maxsize(1280, 640)
    window.minsize(1280, 640)

    buttonFrame = Frame(window, bd=5, padx=10, pady=10)


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
                    )
    button2 = Button(buttonFrame,
                     text="Open selected websites",
                     command=Thread(target=select_item).start(),
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


if __name__ == "__main__":
    main()
