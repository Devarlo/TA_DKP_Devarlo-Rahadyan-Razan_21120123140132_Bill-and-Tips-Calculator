import tkinter as tk
from tkinter import messagebox
from tkinter import *
import pygame
import os

#class billandtipscalculator
class BillandTipsCalculator:
    def __init__(self, root):
        #Inisialisasi Class BillandTipsCalculator dengan root window tkinter
        self.root = root
        self.root.title("Rumah makan Pakde babat")
        #Inisialisasi variabel buat nama dan nomer pelanggan
        self.customer_name = tk.StringVar()
        self.customer_number = tk.StringVar()
        #dictionary buat item menu dan harga
        self.items ={
            "Mie Goreng Jawa": 13000,
            "Nasi Goreng Babat": 16000,
            "Es Teh manis": 5000,
            "Es Jeruk": 8000,
        }

        self.orders ={}

        self.pajak_percentage = 10
        self.tip_percentage = tk.DoubleVar(value=10.0)

        #Bikin GUI
        self.create_gui()

    def create_gui(self):
        #buat customer detail
        details_frame = tk.LabelFrame(self.root, text="Customer Details")
        details_frame.pack(fill="x", padx=10, pady=10)
        name_label = tk.Label(details_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        number_label = tk.Label(details_frame, text="Number:")
        number_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        number_entry = tk.Entry(details_frame, textvariable=self.customer_number)
        number_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        number_entry.configure(validate="key")
        number_entry.configure(validatecommand=(number_entry.register(self.validate_number), "%P"))

        menu_frame = tk.LabelFrame(self.root, text="Menu")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        item_header = tk.Label(menu_frame, text="Items")
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        quantity_header = tk.Label(menu_frame, text="Quantity")
        quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        #buat tips
        details_frame = tk.LabelFrame(self.root, text="Tips ")
        details_frame.pack(fill="x", padx=10, pady=10)

        tip_label = tk.Label(details_frame, text="Tip (%):")
        tip_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tip_entry = tk.Entry(details_frame, textvariable=self.tip_percentage)
        tip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        tip_entry.configure(validate="key")
        tip_entry.configure(validatecommand=(tip_entry.register(self.validate_number), "%P"))

        #buat menu
        row = 1
       
        for item, price in self.items.items():
            item_var = tk.IntVar()
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            quantity_entry = tk.Entry(menu_frame, width=5)
            quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

            self.orders[item] = {"var": item_var, "quantity": quantity_entry}

            row += 1

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup)
        print_bill_button.pack(side="left", padx=5)

        clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection)
        clear_selection_button.pack(side="left", padx=5)

        self.sample_bill_text = tk.Text(self.root, height=10)
        self.sample_bill_text.pack(fill="x", padx=10, pady=10)

        # buat update sample bill
        for item, info in self.orders.items():
            info["quantity"].bind("<FocusOut>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<Return>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<KeyRelease>", lambda event, item=item: self.update_sample_bill(item))
            info["var"].trace("w", lambda *args, item=item: self.update_sample_bill(item))


    def show_bill_popup(self):
        # buat display bill

        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "Masukkan nama anda!")
            return

        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        if not selected_items:
            messagebox.showwarning("Warning", "Pilih salah satu menu yg tersedia!")
            return

        pajak_amount = (total_price * self.pajak_percentage) / 100
        tip_percentage = self.tip_percentage.get()
        tip_amount = (total_price * tip_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Number: {self.customer_number.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"pajak ({self.pajak_percentage}%): {self.convert_to_inr(pajak_amount)}\n"
        bill += f"Tip ({tip_percentage}%): {self.convert_to_inr(tip_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + pajak_amount + tip_amount)}"

        messagebox.showinfo("Bill", bill)

    # hapus item yg udh dipilih di gui
    def clear_selection(self):
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, tk.END)

    # Update bill display dari item yg dipilih
    def update_sample_bill(self, item):
        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        pajak_amount = (total_price * self.pajak_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Number: {self.customer_number.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"pajak ({self.pajak_percentage}%): {self.convert_to_inr(pajak_amount)}\n"
        bill += f"Total Without Tips: {self.convert_to_inr(total_price + pajak_amount)}"

        self.sample_bill_text.delete("1.0", tk.END)  
        self.sample_bill_text.insert(tk.END, bill)

    def validate_number(self, value):
        return value.isdigit() or value == ""

    @staticmethod
    def convert_to_inr(amount):
        return "Rp." + str(amount)  

root = tk.Tk()
#mempercantik bg GUI (//////)
my_bg = PhotoImage(file="C:/Users/ASUS/Pictures/chillbg.png")
my_label = Label(root, image=my_bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

pygame.init()
pygame.mixer.init()
music ="C:/Users/ASUS/Music/sharou.mp3"
if os.path.exists(music):
    try:
        pygame.mixer.music.load(music)
        # Loop Song
        pygame.mixer.music.play(-1)
    except pygame.error as e:
     messagebox.showwarning("Warning", f"Failed to load music file: {e}")
else:
    messagebox.showwarning("Warning", "Music file not found. Music will not play.")
BillandTips_system = BillandTipsCalculator(root)
root.mainloop()