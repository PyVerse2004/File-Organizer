import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from file_organizer import FileOrganizer


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("650x430")
        self.root.minsize(600, 400)

        self.organizer = FileOrganizer()
        self.selected_folder = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.file_count = tk.StringVar(value="Files processed: 0")

        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 10)
        )

    def create_widgets(self):

        # Main container
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill="both", expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text="File Organizer",
            style="Title.TLabel"
        )
        title.pack(pady=(10, 5))

        # Subtitle
        subtitle = ttk.Label(
            main_frame,
            text="Organize your files quickly and easily",
            style="Subtitle.TLabel"
        )
        subtitle.pack(pady=(0, 25))

        # Folder section
        folder_frame = ttk.LabelFrame(
            main_frame,
            text=" Select Folder ",
            padding=15
        )
        folder_frame.pack(fill="x", pady=10)

        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.selected_folder,
            state="readonly"
        )
        self.folder_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        browse_button = ttk.Button(
            folder_frame,
            text="Browse",
            command=self.browse_folder
        )
        browse_button.pack(side="right")

        # Operation section
        operation_frame = ttk.LabelFrame(
            main_frame,
            text=" Operation ",
            padding=20
        )
        operation_frame.pack(fill="x", pady=20)

        button_frame = ttk.Frame(operation_frame)
        button_frame.pack()

        move_button = ttk.Button(
            button_frame,
            text="Move Files",
            style="Action.TButton",
            command=self.move_files
        )
        move_button.pack(
            side="left",
            padx=10
        )

        copy_button = ttk.Button(
            button_frame,
            text="Copy Files",
            style="Action.TButton",
            command=self.copy_files
        )
        copy_button.pack(
            side="left",
            padx=10
        )

        # Status section
        status_frame = ttk.LabelFrame(
            main_frame,
            text=" Status ",
            padding=15
        )
        status_frame.pack(
            fill="x",
            pady=10
        )

        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_text,
            style="Status.TLabel"
        )
        status_label.pack(anchor="w")

        count_label = ttk.Label(
            status_frame,
            textvariable=self.file_count,
            style="Status.TLabel"
        )
        count_label.pack(
            anchor="w",
            pady=(5, 0)
        )

    def browse_folder(self):
        folder = filedialog.askdirectory(
            title="Select a folder"
        )

        if folder:
            self.selected_folder.set(folder)
            self.status_text.set("Folder selected")
            self.file_count.set("Files processed: 0")

    def validate_folder(self):
        folder = self.selected_folder.get()

        if not folder:
            messagebox.showwarning(
                "No Folder",
                "Please select a folder first."
            )
            return False

        return True

    def move_files(self):
        if not self.validate_folder():
            return

        try:
            folder = self.selected_folder.get()

            self.organizer.folder_path(folder)
            self.organizer.create_folders()

            count = self.organizer.move_file()

            self.status_text.set("Files moved successfully")
            self.file_count.set(
                f"Files processed: {count}"
            )

            messagebox.showinfo(
                "Success",
                f"{count} file(s) moved successfully."
            )

        except Exception as error:
            self.status_text.set("An error occurred")

            messagebox.showerror(
                "Error",
                f"Something went wrong:\n\n{error}"
            )

    def copy_files(self):
        if not self.validate_folder():
            return

        try:
            folder = self.selected_folder.get()

            self.organizer.folder_path(folder)
            self.organizer.create_folders()

            count = self.organizer.copy_file()

            self.status_text.set("Files copied successfully")
            self.file_count.set(
                f"Files processed: {count}"
            )

            messagebox.showinfo(
                "Success",
                f"{count} file(s) copied successfully."
            )

        except Exception as error:
            self.status_text.set("An error occurred")

            messagebox.showerror(
                "Error",
                f"Something went wrong:\n\n{error}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()