from tkinter import *
from PIL import Image, ImageTk
import sys
import calculator


class Slider:
    def __init__(self, root):
        self.root = root
        self.root.title("Mart Land")
        root.attributes('-fullscreen', True)

        # Initialize theme colors
        self.bg_color = "dodgerblue4"
        self.btn_color = "deepskyblue"
        self.btn_hover_color = "firebrick2"
        self.text_color = "black"
        self.screen_bg_color = "white"

        # Load the images using PIL
        try:
            self.image1 = Image.open("a.jpg")
            self.image2 = Image.open("b.jpg")

            # Convert images to PhotoImage
            self.photo1 = ImageTk.PhotoImage(self.image1)
            self.photo2 = ImageTk.PhotoImage(self.image2)

            # Create labels with images
            self.lbl1 = Label(self.root, image=self.photo1, bd=0)
            self.lbl1.place(x=0, y=0, relwidth=1, relheight=1)
            self.lbl2 = Label(self.root, image=self.photo2, bd=0)
            self.lbl2.place(x=1000, y=0, relwidth=1, relheight=1)  # Start outside the visible window

            # Initial x position for lbl2
            self.x = 1000
            self.slider_function()

            # Display text on the screen
            self.text_label = Label(self.root, text="Welcome to Mart Land", font=("Arial", 24), bg=self.screen_bg_color, fg=self.text_color, relief="solid", borderwidth=2)
            self.text_label.place(relx=0.5, rely=0.01, anchor="n")

            # Button images
            self.img1 = ImageTk.PhotoImage(Image.open("open.png"))
            self.img2 = ImageTk.PhotoImage(Image.open("close.png"))

            # Button
            self.toggle_button = Button(self.root, command=self.toggle, image=self.img1)
            self.toggle_button.place(x=5, y=10)
        except Exception as e:
            print(f"Error loading images: {e}")

    def slider_function(self):
        self.x -= 1
        if self.x == 0:
            self.x = 1100
            temp = self.photo1
            self.photo1 = self.photo2
            self.photo2 = temp
            self.lbl1.config(image=self.photo1)
            self.lbl2.config(image=self.photo2)
        elif self.x < -1000:  # Reset to start from the right again
            self.x = 1000
        self.lbl2.place(x=self.x, y=0)
        self.lbl2.after(2, self.slider_function)  # Adjust the speed here

    def toggle(self):
        self.f1 = Frame(self.root, width=400, height=700, bg=self.bg_color)
        self.f1.place(x=0, y=0)

        button_style = {
            "font": ("Arial", 16),
            "bg": self.btn_color,
            "fg": self.text_color,
            "relief": "flat",
            "borderwidth": 0,
        }

        # Define frames with border color
        border_color = "black"
        border_width = 2

        self.cashmemo_frame = Frame(self.f1, bg=border_color, width=204, height=54)
        self.cashmemo_frame.place(relx=0.5, rely=0.2, anchor="center")
        self.cashmemo_button = Button(self.cashmemo_frame, text="Cashmemo", command=self.cashmemo_action, **button_style)
        self.cashmemo_button.place(x=border_width, y=border_width, width=200, height=50)
        self.cashmemo_button.bind("<Enter>", self.on_enter)
        self.cashmemo_button.bind("<Leave>", self.on_leave)

        self.products_frame = Frame(self.f1, bg=border_color, width=204, height=54)
        self.products_frame.place(relx=0.5, rely=0.35, anchor="center")
        self.products_button = Button(self.products_frame, text="Products", command=self.products_action, **button_style)
        self.products_button.place(x=border_width, y=border_width, width=200, height=50)
        self.products_button.bind("<Enter>", self.on_enter)
        self.products_button.bind("<Leave>", self.on_leave)

        self.bill_frame = Frame(self.f1, bg=border_color, width=204, height=54)
        self.bill_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.bill_button = Button(self.bill_frame, text="Bill", command=self.bill_action, **button_style)
        self.bill_button.place(x=border_width, y=border_width, width=200, height=50)
        self.bill_button.bind("<Enter>", self.on_enter)
        self.bill_button.bind("<Leave>", self.on_leave)

        self.quit_frame = Frame(self.f1, bg=border_color, width=204, height=54)
        self.quit_frame.place(relx=0.5, rely=0.65, anchor="center")
        self.quit_button = Button(self.quit_frame, text="Quit", command=self.quit_action, **button_style)
        self.quit_button.place(x=border_width, y=border_width, width=200, height=50)
        self.quit_button.bind("<Enter>", self.on_enter)
        self.quit_button.bind("<Leave>", self.on_leave)

        self.theme_frame = Frame(self.f1, bg=border_color, width=204, height=54)
        self.theme_frame.place(relx=0.5, rely=0.8, anchor="center")
        self.theme_button = Button(self.theme_frame, text="Change Theme", command=self.change_theme, **button_style)
        self.theme_button.place(x=border_width, y=border_width, width=200, height=50)
        self.theme_button.bind("<Enter>", self.on_enter)
        self.theme_button.bind("<Leave>", self.on_leave)

        close_button = Button(self.f1, image=self.img2, text="close", command=self.f1.destroy, relief="flat", borderwidth=0)
        close_button.place(x=5, y=5)

    def on_enter(self, event):
        event.widget.config(bg=self.btn_hover_color)

    def on_leave(self, event):
        event.widget.config(bg=self.btn_color)

    def cashmemo_action(self):
        import Cashmemo
        self.root.destroy()
        Cashmemo.Cashmemo()

    def products_action(self):
        import products
        self.root.destroy()
        products.manage_products()

    def bill_action(self):
        import bills
        self.root.destroy()  # Close the current window
        bills.Show_bills()

    def quit_action(self):
        sys.exit()  # Properly close the application

    def change_theme(self):
        if self.bg_color == "dodgerblue4":
            self.bg_color = "dimgray"
            self.btn_color = "firebrick2"
            self.btn_hover_color = "deepskyblue"
            self.text_color = "white"
            self.screen_bg_color = "black"
        else:
            self.bg_color = "dodgerblue4"
            self.btn_color = "deepskyblue"
            self.btn_hover_color = "firebrick2"
            self.text_color = "black"
            self.screen_bg_color = "white"
        self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.screen_bg_color)
        self.text_label.configure(bg=self.screen_bg_color, fg=self.text_color)
        if hasattr(self, 'f1') and self.f1.winfo_exists():
            self.f1.configure(bg=self.bg_color)
            for frame in self.f1.winfo_children():
                frame.configure(bg=self.bg_color)
                for button in frame.winfo_children():
                    button.configure(bg=self.btn_color, fg=self.text_color)

root = Tk()
obj = Slider(root)
root.mainloop()
#calculator()
