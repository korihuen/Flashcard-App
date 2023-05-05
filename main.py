import json
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, font

class Flashcard:
    def __init__(self, front, back, review_date=None, interval=1, repetitions=0, easiness_factor=2.5):
        self.front = front
        self.back = back
        self.review_date = review_date
        self.interval = interval
        self.repetitions = repetitions
        self.easiness_factor = easiness_factor

    def to_dict(self):
        return {
            'front': self.front,
            'back': self.back,
            'review_date': self.review_date,
            'interval': self.interval,
            'repetitions': self.repetitions,
            'easiness_factor': self.easiness_factor
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['front'],
            data['back'],
            data['review_date'],
            data['interval'],
            data['repetitions'],
            data['easiness_factor']
        )

    def update_sm2(self, quality):
        if quality < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            self.easiness_factor = max(1.3, self.easiness_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            self.repetitions += 1

            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.easiness_factor)

        review_date = datetime.date.today() + datetime.timedelta(days=self.interval)
        self.review_date = review_date.isoformat()

class FlashcardApp:
    def __init__(self, flashcard_file='StudyBuddyApplication/flashcards.json'):
        self.flashcard_file = flashcard_file
        self.load_flashcards()

    def load_flashcards(self):
        try:
            with open(self.flashcard_file, 'r') as f:
                flashcard_data = json.load(f)
            self.flashcards = [Flashcard.from_dict(data) for data in flashcard_data]
        except FileNotFoundError:
            self.flashcards = []

    def save_flashcards(self):
        flashcard_data = [flashcard.to_dict() for flashcard in self.flashcards]
        with open(self.flashcard_file, 'w') as f:
            json.dump(flashcard_data, f)

    def add_flashcard(self, front, back):
        flashcard = Flashcard(front, back)
        self.flashcards.append(flashcard)

    def update_review_schedule(self, flashcard, quality):
        flashcard.update_sm2(quality)
        review_date = datetime.date.today() + datetime.timedelta(days=flashcard.interval)
        flashcard.review_date = review_date.isoformat()

    def get_flashcards_to_review(self):
        today = datetime.date.today().isoformat()
        return [flashcard for flashcard in self.flashcards if flashcard.review_date is None or flashcard.review_date <= today]

class FlashcardDeckWindow(tk.Toplevel):
    def __init__(self, app, master = None):
        super().__init__(master)
        self.app = app
        self.title("Flashcard Deck")
        self.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Flashcard", command=self.add_flashcard) 
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        self.review_frame = tk.Frame(self)
        self.review_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.front_label = tk.Label(self.review_frame, text="Front:")
        self.front_label.pack(side=tk.TOP)

        self.front_text = tk.Text(self.review_frame, wrap=tk.WORD, height=5, width=40)
        self.front_text.pack(side=tk.TOP, padx=5, pady=5)

        self.back_label = tk.Label(self.review_frame, text="Back:")
        self.back_label.pack(side=tk.TOP)

        self.back_text = tk.Text(self.review_frame, wrap=tk.WORD, height=5, width=40)
        self.back_text.pack(side=tk.TOP, padx=5, pady=5)

        self.buttons_frame = tk.Frame(self.review_frame)
        self.buttons_frame.pack(side=tk.TOP, pady=10)

        self.show_answer_button = tk.Button(self.buttons_frame, text="Show Answer", command=self.show_answer)
        self.show_answer_button.pack(side=tk.LEFT, padx=10)

        self.grade_frame = tk.Frame(self.buttons_frame)
        self.grade_frame.pack(side=tk.LEFT)

        self.grade_label = tk.Label(self.grade_frame, text="Grade (0-5):")
        self.grade_label.pack(side=tk.LEFT)

        self.grade_entry = tk.Entry(self.grade_frame, width=5)
        self.grade_entry.pack(side=tk.LEFT)

        self.grade_button = tk.Button(self.buttons_frame, text="Grade", command=self.grade)
        self.grade_button.pack(side=tk.LEFT, padx=10)


        self.next_flashcard()

    def add_flashcard(self):
        add_flashcard_dialog = tk.Toplevel(self)
        add_flashcard_dialog.title("Add Flashcard")

        front_label = tk.Label(add_flashcard_dialog, text="Front:")
        front_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        front_entry = tk.Entry(add_flashcard_dialog)
        front_entry.grid(row=0, column=1, padx=5, pady=5)

        back_label = tk.Label(add_flashcard_dialog, text="Back:")
        back_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        back_entry = tk.Entry(add_flashcard_dialog)
        back_entry.grid(row=1, column=1, padx=5, pady=5)

        submit_button = tk.Button(add_flashcard_dialog, text="Submit", command=lambda: self.submit_new_flashcard(add_flashcard_dialog, front_entry.get(), back_entry.get()))
        submit_button.grid(row=2, columnspan=2, pady=10)

    def submit_new_flashcard(self, dialog, front, back):
        self.app.add_flashcard(front, back)
        self.app.save_flashcards()
        dialog.destroy()

    def show_answer(self):
        self.back_text.config(state=tk.NORMAL)
        self.back_text.delete(1.0, tk.END)
        self.back_text.insert(tk.END, self.current_flashcard.back)
        self.back_text.config(state=tk.DISABLED)

    def grade(self):
        grade_str = self.grade_entry.get()
        if not grade_str.isdigit() or not (0 <= int(grade_str) <= 5):
            messagebox.showerror("Invalid Grade", "Please enter a valid grade between 0 and 5.")
            return

        grade = int(grade_str)
        self.app.update_review_schedule(self.current_flashcard, grade)
        self.app.save_flashcards()
        self.next_flashcard()

        self.grade_entry.delete(0, tk.END)
        self.back_text.config(state=tk.NORMAL)
        self.back_text.delete(1.0, tk.END)
        self.back_text.config(state=tk.DISABLED)

    def next_flashcard(self):
        flashcards_to_review = self.app.get_flashcards_to_review()
        if not flashcards_to_review:
            messagebox.showinfo("No Flashcards to Review", "There are no flashcards to review at this time.")
            return

        self.current_flashcard = flashcards_to_review[0]
        self.front_text.delete(1.0, tk.END)
        self.front_text.insert(tk.END, self.current_flashcard.front)
        self.back_text.delete(1.0, tk.END)
        self.back_text.config(state=tk.DISABLED)


class MainWindow(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Flashcard App")
        self.geometry("300x300")
        self.create_menu_screen()

    def create_menu_screen(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        new_deck_button = tk.Button(self.menu_frame, text="Create New Deck", command=self.create_new_deck)
        new_deck_button.pack(pady=10)

        browse_decks_button = tk.Button(self.menu_frame, text="Browse Decks", command=self.browse_decks)
        browse_decks_button.pack(pady=10)

    def create_new_deck(self):
        deck_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if deck_name:
            self.app.flashcard_file = deck_name
            self.app.flashcards = []
            self.app.save_flashcards()

    def browse_decks(self):
        deck_name = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if deck_name:
            self.app.flashcard_file = deck_name
            self.app.load_flashcards()
            self.open_new_window()

    def open_new_window(self):
        new_window = FlashcardDeckWindow(self.app, self)
        new_window.mainloop()

def main():
    app = FlashcardApp()
    gui = MainWindow(app)
    gui.mainloop()

if __name__ == "__main__":
    main()
