import tkinter as tk
import json
from category import ChooseCategory
from questions import QuestionnaireApp

# === APPLICATION ENTRY POINT ===
if __name__ == "__main__":
    # Open the category selection window
    selection_window = ChooseCategory()
    chosen_file = selection_window.run()

    if chosen_file:
        # Load the selected JSON data
        with open(f"{chosen_file}", 'r', encoding="UTF-8") as f:
            json_data = json.load(f)

        # Start the main questionnaire window
        main_app_window = tk.Tk()
        app = QuestionnaireApp(main_app_window, json_data)
        main_app_window.mainloop()
