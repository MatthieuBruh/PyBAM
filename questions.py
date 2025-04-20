from tkinter import Tk, messagebox, Label, Button, Frame, Menu, BOTH
import webbrowser
import json
from tree import display_tree

class QuestionnaireApp:
    """
    Main GUI class for navigating through the decision tree questionnaire.
    """

    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.history = []
        self.current_question = data["start"]
        self.widgets = {}
        self.button_width = 50

        self.setup_window()
        self.create_menu()
        self.build_layout()
        self.update_question()

    def setup_window(self):
        """Configure the main window size and position."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = (screen_width * 2) // 3
        height = (screen_height * 2) // 3
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.title("Questionnaire Barreau Vaudois")
        self.root.update_idletasks()

    def create_menu(self):
        """Creates the application menu."""
        menu_bar = Menu(self.root)

        # Changer de catégorie
        category_menu = Menu(menu_bar, tearoff=0)
        category_menu.add_command(label="Barreau", command=lambda: self.load_new_file("barreau_vaudois.json"))
        category_menu.add_command(label="Notaire", command=lambda: self.load_new_file("notaire_vaudois.json"))
        menu_bar.add_cascade(label="Changer de catégorie", menu=category_menu)

        # Arbre décisionnel
        tree_menu = Menu(menu_bar, tearoff=0)
        tree_menu.add_command(label="Afficher", command=self.show_tree)
        menu_bar.add_cascade(label="Arbre décisionnel", menu=tree_menu)

        # Autres options
        options_menu = Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Recommencer", command=self.restart)
        options_menu.add_command(label="Quitter", command=self.quit_app)
        menu_bar.add_cascade(label="Options", menu=options_menu)

        self.root.config(menu=menu_bar)

    def build_layout(self):
        """Initialize layout frames and labels."""
        self.root.grid_columnconfigure(0, weight=1, minsize=300)
        self.root.grid_columnconfigure(1, weight=2, minsize=500)
        self.root.grid_rowconfigure(0, weight=1)

        self.history_frame = (Frame(self.root))
        self.history_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.history_label = Label(self.history_frame, text="", anchor="w", justify="left", wraplength=240, bg="white")
        self.history_label.pack(padx=5, pady=5, fill=BOTH, expand=True)

        self.question_frame = Frame(self.root)
        self.question_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.question_label = Label(self.question_frame, text="", wraplength=500, justify="left", font="bold")
        self.question_label.pack(padx=5, pady=5)

    def load_new_file(self, filename):
        """Load a new JSON file and reset the questionnaire."""
        try:
            with open(f"data/{filename}", 'r', encoding="UTF-8") as f:
                self.data = json.load(f)
            self.current_question = self.data["start"]
            self.restart()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger {filename}.\n\n{e}")

    def show_tree(self):
        """Display the decision tree using PyVis."""
        display_tree(self.data)

    def restart(self):
        """Reset the questionnaire from the start."""
        self.history = []
        self.current_question = self.data["start"]
        self.history_label.config(text="")

        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()
        self.update_question()

    def quit_app(self):
        """Quit the application."""
        self.root.quit()

    def update_question(self):
        """Update the question and response options."""
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()

        node = self.data["nodes"][self.current_question]
        self.question_label.config(text=node["text"])

        if "link" in node:
            link_label = Label(self.question_frame, text="Lien vers article ou règlement", fg="blue", cursor="hand2", font=("Arial", 14, "underline"))
            link_label.pack(pady=5)
            link_label.bind("<Button-1>", lambda e, url=node["link"]: webbrowser.open_new(url))
            self.widgets["link"] = link_label

        for choice, next_key in node["choices"].items():
            next_node = self.data["nodes"][next_key]
            text = next_node["text"]

            if next_node["type"] == "result":
                result_label = Label(self.question_frame, text=text, fg="blue", wraplength=300, font=("Arial", 14, "italic"))
                result_label.pack(pady=5)
                self.widgets[choice] = result_label

                if "link" in next_node:
                    link = Label(self.question_frame, text="Lien vers le document officiel", fg="blue", cursor="hand2", font=("Arial", 14, "underline"))
                    link.pack(pady=5)
                    link.bind("<Button-1>", lambda e, url=next_node["link"]: webbrowser.open_new(url))
                    self.widgets[f"{choice}_link"] = link
            else:
                button = Button(self.question_frame, text=text, font=("Arial", 12), width=self.button_width, wraplength=300, command=lambda c=choice: self.handle_choice(c))
                button.pack(pady=5)
                self.widgets[choice] = button

    def handle_choice(self, choice):
        """Handle the user's answer and move to the next node."""
        node = self.data["nodes"][self.current_question]
        self.history.append((self.current_question, node["text"]))

        history_text = "\n\n".join([f"Q: {q[1]}" for q in self.history])
        self.history_label.config(text=history_text)

        next_key = node["choices"][choice]
        next_node = self.data["nodes"][next_key]

        if next_node["type"] == "result":
            self.history.append((next_key, next_node["text"], "Résultat"))
            final_text = "\n\n".join([f"- Question : {q[1]} -> {q[2]}" if len(q) > 2 else f"Q: {q[1]}" for q in self.history])
            self.history_label.config(text=final_text)
        else:
            self.current_question = next_key
            self.update_question()
