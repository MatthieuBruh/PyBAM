from tkinter import Tk, Label, Button, Frame

class ChooseCategory:
    """
    A simple initial window allowing the user to choose a category (Barreau or Notaire).
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("Choisissez une catégorie")
        self.choice = None

        # Center the window (1/3 screen size)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width // 3
        window_height = screen_height // 3
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

        # UI Elements
        Label(self.root, text="Veuillez choisir une catégorie :", font=("Arial", 14)).pack(pady=30)

        button_frame = Frame(self.root)
        button_frame.pack(pady=20)

        Button(button_frame, text="Barreau", width=15, font=("Arial", 12),
               command=lambda: self.select("./data/barreau_vaudois.json")).grid(row=0, column=0, padx=10)
        Button(button_frame, text="Notaire", width=15, font=("Arial", 12),
               command=lambda: self.select("./data/notaire_vaudois.json")).grid(row=0, column=1, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

    def select(self, filename):
        """Save the selected filename and close the window."""
        self.choice = filename
        self.root.destroy()

    def run(self):
        """Start the window's main loop."""
        self.root.mainloop()
        return self.choice