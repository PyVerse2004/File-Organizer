import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

from file_organizer import FileOrganizer


class FileOrganizerGUI:

    def __init__(self, root):
        self.root = root

        self.root.title("File Organizer")
        self.root.geometry("650x500")
        self.root.minsize(600, 450)

        self.organizer = FileOrganizer()

        self.selected_folder = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.file_count = tk.StringVar(value="Files processed: 0")
        self.progress_text = tk.StringVar(value="0%")

        self.setup_style()
        self.create_widgets()

    # -------------------------
    # Style
    # -------------------------

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

    # -------------------------
    # GUI
    # -------------------------

    def create_widgets(self):

        main_frame = ttk.Frame(
            self.root,
            padding=30
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

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

        subtitle.pack(
            pady=(0, 25)
        )

        # -------------------------
        # Folder
        # -------------------------

        folder_frame = ttk.LabelFrame(
            main_frame,
            text=" Select Folder ",
            padding=15
        )

        folder_frame.pack(
            fill="x",
            pady=10
        )

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

        self.browse_button = ttk.Button(
            folder_frame,
            text="Browse",
            command=self.browse_folder
        )

        self.browse_button.pack(
            side="right"
        )

        # -------------------------
        # Operation
        # -------------------------

        operation_frame = ttk.LabelFrame(
            main_frame,
            text=" Operation ",
            padding=20
        )

        operation_frame.pack(
            fill="x",
            pady=20
        )

        button_frame = ttk.Frame(
            operation_frame
        )

        button_frame.pack()

        self.move_button = ttk.Button(
            button_frame,
            text="Move Files",
            style="Action.TButton",
            command=self.move_files
        )

        self.move_button.pack(
            side="left",
            padx=10
        )

        self.copy_button = ttk.Button(
            button_frame,
            text="Copy Files",
            style="Action.TButton",
            command=self.copy_files
        )

        self.copy_button.pack(
            side="left",
            padx=10
        )

        # -------------------------
        # Progress
        # -------------------------

        progress_frame = ttk.LabelFrame(
            main_frame,
            text=" Progress ",
            padding=15
        )

        progress_frame.pack(
            fill="x",
            pady=10
        )

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate"
        )

        self.progress_bar.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.progress_label = ttk.Label(
            progress_frame,
            textvariable=self.progress_text,
            width=5
        )

        self.progress_label.pack(
            side="right"
        )

        # -------------------------
        # Status
        # -------------------------

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

        status_label.pack(
            anchor="w"
        )

        count_label = ttk.Label(
            status_frame,
            textvariable=self.file_count,
            style="Status.TLabel"
        )

        count_label.pack(
            anchor="w",
            pady=(5, 0)
        )

    # -------------------------
    # Browse
    # -------------------------

    def browse_folder(self):

        folder = filedialog.askdirectory(
            title="Select a folder"
        )

        if folder:

            self.selected_folder.set(folder)

            self.status_text.set(
                "Folder selected"
            )

            self.file_count.set(
                "Files processed: 0"
            )

            self.progress_bar["value"] = 0
            self.progress_text.set("0%")

    # -------------------------
    # Validation
    # -------------------------

    def validate_folder(self):

        folder = self.selected_folder.get()

        if not folder:

            messagebox.showwarning(
                "No Folder",
                "Please select a folder first."
            )

            return False

        return True

    # -------------------------
    # Move
    # -------------------------

    def move_files(self):

        if not self.validate_folder():
            return

        self.start_operation("move")

    # -------------------------
    # Copy
    # -------------------------

    def copy_files(self):

        if not self.validate_folder():
            return

        self.start_operation("copy")

    # -------------------------
    # Start operation
    # -------------------------

    def start_operation(self, operation):

        self.set_buttons_state("disabled")

        self.progress_bar["value"] = 0
        self.progress_text.set("0%")

        self.status_text.set(
            f"{operation.capitalize()}ing files..."
        )

        thread = threading.Thread(
            target=self.run_operation,
            args=(operation,),
            daemon=True
        )

        thread.start()

    # -------------------------
    # Run operation
    # -------------------------

    def run_operation(self, operation):

        try:

            folder = self.selected_folder.get()

            self.organizer.folder_path(folder)
            self.organizer.create_folders()

            if operation == "move":

                count = self.organizer.move_file(
                    self.update_progress
                )

            else:

                count = self.organizer.copy_file(
                    self.update_progress
                )

            self.root.after(
                0,
                self.operation_finished,
                operation,
                count
            )

        except Exception as error:

            self.root.after(
                0,
                self.operation_error,
                error
            )

    # -------------------------
    # Progress callback
    # -------------------------

    def update_progress(self, current, total):

        if total == 0:
            percentage = 100
        else:
            percentage = int(
                (current / total) * 100
            )

        self.root.after(
            0,
            self.update_progress_ui,
            percentage,
            current,
            total
        )

    # -------------------------
    # Update progress UI
    # -------------------------

    def update_progress_ui(
        self,
        percentage,
        current,
        total
    ):

        self.progress_bar["value"] = percentage

        self.progress_text.set(
            f"{percentage}%"
        )

        self.file_count.set(
            f"Files processed: {current}/{total}"
        )

    # -------------------------
    # Finished
    # -------------------------

    def operation_finished(
        self,
        operation,
        count
    ):

        self.progress_bar["value"] = 100
        self.progress_text.set("100%")

        self.status_text.set(
            f"Files {operation}ed successfully"
        )

        self.file_count.set(
            f"Files processed: {count}"
        )

        self.set_buttons_state("normal")

        messagebox.showinfo(
            "Success",
            f"{count} file(s) {operation}ed successfully."
        )

    # -------------------------
    # Error
    # -------------------------

    def operation_error(self, error):

        self.status_text.set(
            "An error occurred"
        )

        self.set_buttons_state("normal")

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{error}"
        )

    # -------------------------
    # Button state
    # -------------------------

    def set_buttons_state(self, state):

        self.move_button["state"] = state
        self.copy_button["state"] = state
        self.browse_button["state"] = state


if __name__ == "__main__":

    root = tk.Tk()

    app = FileOrganizerGUI(root)

    root.mainloop()