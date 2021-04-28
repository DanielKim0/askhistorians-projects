try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from tkcalendar import DateEntry
from submission_filter import Submission_Filter

class Page(tk.Frame):
    """Class used for basic pages, with labels and maybe buttons."""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.labels = []
        self.buttons = []
        self.calendars = []
        self.entries = []
        self.checks = []

    def add_label(self, text):
        label = tk.Label(self, text=text)
        label.pack(padx=10, pady=10)
        self.labels.append(label)
    
    def change_label(self, text, num=0):
        self.labels[num]["text"] = text

    def add_button(self, text, func):
        button = tk.Button(self, text=text, command=func)
        button.pack(padx=10, pady=10)
        self.buttons.append(button)

    def add_entry(self, text, show=False):
        label = tk.Label(self, text=text)
        label.pack(padx=10, pady=10)
        self.labels.append(label)

        if show:
            cal = tk.Entry(self, show="*")
        else:
            cal = tk.Entry(self)
        cal.pack(padx=10, pady=10)
        self.entries.append(cal)

    def add_calendar(self, text):
        label = tk.Label(self, text=text)
        label.pack(padx=10, pady=10)
        self.labels.append(label)

        cal = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)
        self.calendars.append(cal)

    def add_check(self, text):
        checkvar = tk.BooleanVar()
        check = tk.Checkbutton(self, text=text, var=checkvar)
        check.pack(padx=10, pady=10)
        self.checks.append([check, checkvar])

class FilterGUI(tk.Frame):
    """Class that sets up the GUI for the save fetcher and handles running functions on SaveFetcher."""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.filter = Submission_Filter()
        self.pages = self.page_setup()
        self.setup_gui()
        self.current_page = 0

    def page_setup(self):
        """Method that builds all of the pages used for this application."""

        pages = [Page(self), Page(self), Page(self)]
        pages[0].add_entry("Username")
        pages[0].add_entry("Password", True)
        pages[0].add_entry("2FA", True)
        pages[0].add_label("Input your credentials here.")
        pages[1].add_calendar("From Date")
        pages[1].add_calendar("To Date")
        pages[1].add_label("Input the from and to dates here.")
        pages[2].add_label("Press the button to begin.")
        pages[2].add_button("Begin!", self.filter_submissions)
        pages[2].add_check("Check to delete fetched posts.")
        pages[2].add_entry("Input the name of the results file. Leave blank for \"results\".")
        return pages

    def setup_gui(self):
        """Method that sets up the actual gui, including implementing the pages and other frames."""

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)

        buttonframe.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        for page in self.pages:
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.button = tk.Button(buttonframe, text="next page", command=self.next_page)
        self.button.pack(side="top", anchor="center", pady=50)
        self.pages[0].lift()

    def next_page(self):
        """Method that determines what to do when the next page button is clicked."""

        if self.current_page < len(self.pages):
            if self.current_page == 0:
                result, err = self.filter.reddit_signin(self.pages[0].entries[0].get(), self.pages[0].entries[1].get(), self.pages[0].entries[2].get())
            elif self.current_page == 1:
                result, err = self.filter.create_dates(self.pages[1].calendars[0].get_date(), self.pages[1].calendars[1].get_date())
            else: # self.current_page == 2
                result, err = True, None

            if result:
                if self.current_page == 2:
                    self.current_page = 1
                else:
                    self.current_page += 1
                self.button["text"] = "Next Page"

                self.pages[self.current_page].lift()
                if self.current_page == 2:
                    self.reset_final_page()
            else:
                self.pages[self.current_page].change_label(err, -1)

    def reset_final_page(self):
        """Method that resets the final page to prepare for multiple uses."""

        self.button["text"] = "Previous Page"
        self.pages[2].buttons[0].pack(padx=10, pady=10)
        self.pages[2].checks[0][0].pack(padx=10, pady=10)
        self.pages[2].labels[1].pack(padx=10, pady=10)
        self.pages[2].entries[0].pack(padx=10, pady=10)
        self.pages[2].change_label("Press the button to begin.", 0)

    def filter_submissions(self):
        """Wrapper method that calls the main functionality in self.filter."""

        self.pages[2].buttons[0].pack_forget()
        self.pages[2].checks[0][0].pack_forget()
        self.pages[2].labels[1].pack_forget()
        self.pages[2].entries[0].pack_forget()
        message = self.filter.filter_submissions(self.pages[2].entries[0].get(), self.pages[2].checks[0][1].get())
        self.pages[2].change_label(message, 0)

def main():
    """Main method that sets up the root frame and runs the program."""

    root = tk.Tk()
    main = FilterGUI(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x600")
    root.resizable(0, 0)
    root.mainloop()

if __name__ == "__main__":
    main()
