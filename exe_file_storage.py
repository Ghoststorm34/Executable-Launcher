import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ExecutableLauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title and size of the main window
        self.title("Executable Launcher")
        self.geometry("800x600")

        # Apply dark mode style
        self.configure(bg='#2e2e2e')
        style = ttk.Style(self)
        self.tk_setPalette(background='#2e2e2e', foreground='white', activeBackground='#3e3e3e', activeForeground='white')

        # Create a dark Treeview style
        style.theme_use("clam")
        style.configure("Treeview", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
        style.map('Treeview', background=[('selected', '#4d4d4d')], foreground=[('selected', 'white')])

        # Create the menu bar
        self.create_menu_bar()

        # Create a search bar at the top
        self.create_search_bar()

        # Set up the treeview
        self.tree = ttk.Treeview(self, selectmode='browse', columns=("path",))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 5))

        # Add columns to treeview
        self.tree.heading("#0", text="Executables", anchor=tk.W)
        self.tree.heading("path", text="Path", anchor=tk.W)
        self.tree.column("path", stretch=True)

        # Set up context menu for treeview
        self.create_context_menu()

        # Load data from file
        self.data_file = "data.json"
        self.load_data()

        # Bind events
        self.bind_events()

        # Create the bottom button frame
        self.create_bottom_buttons()

    def bind_events(self):
        # Bind right-click to treeview
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Bind double-click to execute
        self.tree.bind("<Double-1>", self.execute_selected)

        # Bind drag and drop for moving items
        self.tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_release)

    def create_menu_bar(self):
        # Create the menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add Folder", command=self.add_folder)
        edit_menu.add_command(label="Add Executable", command=self.add_executable)
        edit_menu.add_command(label="Edit Selected", command=self.edit_item)
        edit_menu.add_command(label="Remove Selected", command=self.remove_item)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def create_search_bar(self):
        # Create a search bar frame at the top
        search_frame = tk.Frame(self, bg='#2e2e2e')
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Add search label and entry
        search_label = tk.Label(search_frame, text="Search:", bg='#2e2e2e', fg='white')
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, bg='#4d4d4d', fg='white', insertbackground='white')
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_items)

    def create_context_menu(self):
        # Right-click context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Add Folder", command=self.add_folder)
        self.context_menu.add_command(label="Add Executable", command=self.add_executable)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit", command=self.edit_item)
        self.context_menu.add_command(label="Remove", command=self.remove_item)

    def create_bottom_buttons(self):
        # Create a frame for bottom buttons
        button_frame = tk.Frame(self, bg='#2e2e2e')
        button_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

        # Add buttons to the bottom frame
        add_folder_btn = tk.Button(button_frame, text="Add Folder", command=self.add_folder, bg='#4d4d4d', fg='white')
        add_folder_btn.pack(side=tk.LEFT, padx=5)

        add_executable_btn = tk.Button(button_frame, text="Add Executable", command=self.add_executable, bg='#4d4d4d', fg='white')
        add_executable_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(button_frame, text="Edit Selected", command=self.edit_item, bg='#4d4d4d', fg='white')
        edit_btn.pack(side=tk.LEFT, padx=5)

        remove_btn = tk.Button(button_frame, text="Remove Selected", command=self.remove_item, bg='#4d4d4d', fg='white')
        remove_btn.pack(side=tk.LEFT, padx=5)

        sort_btn = tk.Button(button_frame, text="Sort", command=self.sort_items, bg='#4d4d4d', fg='white')
        sort_btn.pack(side=tk.LEFT, padx=5)

    def show_context_menu(self, event):
        # Display context menu on right-click
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            self.context_menu.post(event.x_root, event.y_root)

    def add_folder(self):
        # Placeholder function to add a folder
        print("Add Folder")
        self.save_data()  # Call save after making changes

    def add_executable(self):
        # Prompt the user for executable name and path
        name = "New Executable"  # Placeholder, replace with a dialog to input name
        path = "/path/to/example with spaces"  # Placeholder, replace with a dialog to input path
        parent = self.tree.selection()[0] if self.tree.selection() else ''

        # Add to treeview
        # Use a tuple with a single element to correctly insert paths with spaces
        self.tree.insert(parent, "end", text=name, values=(path,))
        print(f"Added Executable: {name} with path: {path}")
        self.save_data()  # Call save after making changes

    def edit_item(self):
        # Placeholder function to edit an item
        print("Edit Item")
        self.save_data()  # Call save after making changes

    def remove_item(self):
        # Placeholder function to remove an item
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            print("Item removed")
            self.save_data()  # Call save after making changes

    def execute_selected(self, event=None):
        # Placeholder function to execute the selected item
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        item_path = self.tree.item(selected_item, "values")[0]
        print(f"Executing {item_text} at {item_path}")

    def search_items(self, event=None):
        # Placeholder function for searching/filtering items in the treeview
        search_query = self.search_entry.get().lower()
        print(f"Searching for {search_query}")

    def sort_items(self):
        # Placeholder function to sort items in the treeview
        print("Sorting items")

    def on_drag_start(self, event):
        # Placeholder for drag start logic
        self.drag_data = {"item": self.tree.identify_row(event.y)}
        print("Drag Start")

    def on_drag_motion(self, event):
        # Placeholder for drag motion logic
        print("Dragging")

    def on_drag_release(self, event):
        # Placeholder for drag release logic
        print("Drop")

    def load_data(self):
        # Load data from JSON file
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                try:
                    data = json.load(file)
                    self.populate_treeview(data)
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Failed to load data.")
        else:
            self.initialize_default_data()

    def initialize_default_data(self):
        # Initialize default data if the file does not exist
        root_folder = self.tree.insert("", "end", text="Root Folder", open=True)
        self.tree.insert(root_folder, "end", text="Example Executable 🖥️", values=("/path/to/example with spaces",))

    def populate_treeview(self, data):
        # Populate the treeview with loaded data
        print("Populate treeview with loaded data")

    def save_data(self):
        # Save data to JSON file
        data = self.extract_treeview_data()
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)

    def extract_treeview_data(self):
        # Extract data from the treeview for saving
        print("Extract data from treeview for saving")
        return {}  # Return the extracted data structure

# Run the application
if __name__ == "__main__":
    app = ExecutableLauncherApp()
    app.mainloop()
