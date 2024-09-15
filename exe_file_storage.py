import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import subprocess
import os

DATA_FILE = "tree_data.json"

class ExecutableLauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title and size of the main window
        self.title("Executable Launcher")
        self.geometry("1000x600")

        # Apply dark mode style
        self.configure(bg='#2e2e2e')
        style = ttk.Style(self)
        self.tk_setPalette(background='#2e2e2e', foreground='white', activeBackground='#3e3e3e', activeForeground='white')

        # Create a dark Treeview style
        style.theme_use("clam")
        style.configure("Treeview", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
        style.map('Treeview', background=[('selected', '#4d4d4d')], foreground=[('selected', 'white')])

        # Initialize variables for drag and drop
        self.dragging_item = None
        self.drag_label = None  # For the floating label

        # Create the menu bar
        self.create_menu_bar()

        # Create a search bar at the top
        self.create_search_bar()

        # Set up the treeview
        self.tree = ttk.Treeview(self, selectmode='browse', columns=("path",))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 5))

        # Initialize data structure to mimic the treeview
        self.tree_data = {}

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

        # Actions menu
        actions_menu = tk.Menu(menu_bar, tearoff=0)
        actions_menu.add_command(label="Execute", command=self.execute_selected)
        actions_menu.add_command(label="Sort", command=self.sort_items)
        menu_bar.add_cascade(label="Actions", menu=actions_menu)

        # Help menu (Placeholder for future use)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about_info)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def show_about_info(self):
        # Placeholder for showing information about the application
        messagebox.showinfo("About Executable Launcher", "Executable Launcher\nOrganize and run your executables.")


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
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Execute", command=self.execute_selected)
        self.context_menu.add_command(label="Sort", command=self.sort_items)

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
        
        # Add Execute button
        execute_btn = tk.Button(button_frame, text="Execute", command=self.execute_selected, bg='#4d4d4d', fg='white')
        execute_btn.pack(side=tk.LEFT, padx=5)

    def show_context_menu(self, event):
        # Display context menu on right-click
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            self.context_menu.post(event.x_root, event.y_root)

    def sort_treeview(self, parent=''):
        # Get the children of the current parent
        children = list(self.tree.get_children(parent))
        
        # Separate folders and executables
        folders = [item for item in children if not self.tree.item(item, 'values')]
        executables = [item for item in children if self.tree.item(item, 'values')]
        
        # Sort folders and executables alphabetically
        folders.sort(key=lambda x: self.tree.item(x, 'text').lower())
        executables.sort(key=lambda x: self.tree.item(x, 'text').lower())
        
        # Rearrange children in the treeview
        for index, item in enumerate(folders + executables):
            self.tree.move(item, parent, index)

    def add_folder(self):
        # Prompt the user for a folder name
        folder_name = simpledialog.askstring("Add Folder", "Enter folder name:")
        
        if folder_name:
            # Determine where to insert the new folder
            parent = self.tree.selection()[0] if self.tree.selection() else ''

            # If parent is an executable, get its parent folder
            if parent and self.tree.item(parent, 'values'):
                parent = self.tree.parent(parent)

            # Get path in data structure
            parent_path = self.get_data_path(parent)
            
            # Add the folder to the data structure
            current_level = self.get_current_level(self.tree_data, parent_path)
            current_level[folder_name] = {}

            # Add the folder to the treeview
            self.tree.insert(parent, "end", text=folder_name, open=True)

            # Sort items to reflect in the treeview
            self.sort_items()

            # Save the updated treeview to the data file
            self.save_data()

    def add_executable(self):
        # Prompt the user for the executable name
        exe_name = simpledialog.askstring("Add Executable", "Enter executable name:")
        if not exe_name:
            return  # If no name was provided, exit the function

        # Open a file picker dialog to select the executable path
        exe_path = filedialog.askopenfilename(
            title="Select Executable",
            filetypes=[("Executable files", "*.exe")],  # Restrict to .exe files
        )
        if not exe_path:
            return  # If no path was selected, exit the function

        # Prompt the user for an emoji
        exe_emoji = simpledialog.askstring("Add Executable", "Enter emoji for executable (optional):", initialvalue="📁")
        if not exe_emoji:
            exe_emoji = "📁"  # Use folder icon as default

        # Determine where to insert the new executable
        parent = self.tree.selection()[0] if self.tree.selection() else ''

        # If the selected item is an executable, add to its parent
        if parent and self.tree.item(parent, 'values'):
            parent = self.tree.parent(parent)

        # Get path in data structure
        parent_path = self.get_data_path(parent)

        # Add the executable to the data structure
        current_level = self.get_current_level(self.tree_data, parent_path)
        current_level[exe_name] = {"path": exe_path, "emoji": exe_emoji}

        # Add the executable to the treeview
        self.tree.insert(parent, "end", text=f"{exe_emoji} {exe_name}", values=(exe_path,))

        # Sort items to reflect in the treeview
        self.sort_items()

        # Save the updated treeview to the data file
        self.save_data()

    def get_data_path(self, item_id):
        # Helper to get the path in the data structure
        path = []
        while item_id:
            path.insert(0, self.tree.item(item_id, 'text'))
            item_id = self.tree.parent(item_id)
        return path

    def get_current_level(self, data_structure, path):
        # Traverse to the current level in the data structure
        current_level = data_structure
        for part in path:
            current_level = current_level[part]
        return current_level

    def edit_item(self):
        # Get the selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Edit Item", "No item selected.")
            return

        # Get the first selected item
        item_id = selected_item[0]

        # Get the current path in the data structure
        parent_path = self.get_data_path(self.tree.parent(item_id))
        current_name = self.tree.item(item_id, 'text').split(' ', 1)[-1]
        current_level = self.get_current_level(self.tree_data, parent_path)

        # Check if it's an executable (has values)
        item_values = self.tree.item(item_id, 'values')
        if item_values:
            # Executable - allow editing of name, path, and emoji
            current_emoji = self.tree.item(item_id, 'text').split(' ')[0]
            current_path = item_values[0]

            # Prompt for new name
            new_name = simpledialog.askstring("Edit Executable", "Enter new name:", initialvalue=current_name)
            if not new_name:
                return  # Exit if no name is provided

            # Prompt for new path
            new_path = filedialog.askopenfilename(
                title="Select Executable",
                filetypes=[("Executable files", "*.exe")],
                initialdir=os.path.dirname(current_path),
                initialfile=current_path
            )
            if not new_path:
                return  # Exit if no path is provided

            # Prompt for new emoji
            new_emoji = simpledialog.askstring("Edit Executable", "Enter new emoji (optional):", initialvalue=current_emoji)
            if not new_emoji:
                new_emoji = current_emoji  # Keep the current emoji if none is provided

            # Update the data structure
            del current_level[current_name]
            current_level[new_name] = {"path": new_path, "emoji": new_emoji}

            # Update the treeview with the new values
            self.tree.item(item_id, text=f"{new_emoji} {new_name}", values=(new_path,))
        
        else:
            # Folder - allow editing of the folder name
            # Prompt for new folder name
            new_name = simpledialog.askstring("Edit Folder", "Enter new folder name:", initialvalue=current_name)
            if not new_name:
                return  # Exit if no name is provided

            # Update the data structure
            current_level[new_name] = current_level.pop(current_name)

            # Update the treeview with the new folder name
            self.tree.item(item_id, text=new_name)

        # Sort items to reflect changes in the treeview
        self.sort_items()

        # Save the updated treeview to the data file
        self.save_data()


    def remove_item(self):
        # Get the selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Remove Item", "No item selected.")
            return

        # Get the first selected item
        item_id = selected_item[0]

        # Confirm deletion
        item_name = self.tree.item(item_id, 'text').split(' ', 1)[-1]
        confirm = messagebox.askyesno("Remove Item", f"Are you sure you want to remove '{item_name}'?")
        if not confirm:
            return  # If the user cancels, exit the function

        # Remove the item from the data structure
        parent_path = self.get_data_path(self.tree.parent(item_id))
        current_level = self.get_current_level(self.tree_data, parent_path)
        del current_level[item_name]

        # Remove the item from the treeview
        self.tree.delete(item_id)

        # Save the updated treeview to the data file
        self.save_data()


    def execute_selected(self, event=None):
        # Get the selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Execute Item", "No item selected.")
            return

        # Get the first selected item
        item_id = selected_item[0]

        # Check if it's an executable (has values)
        item_values = self.tree.item(item_id, 'values')
        if not item_values:
            # If the selected item is not an executable, show an error message
            messagebox.showerror("Execute Item", "Selected item is not an executable.")
            return

        # Get the path of the executable
        exe_path = item_values[0]

        # Try to execute the file
        try:
            # Use subprocess.Popen to execute the file
            subprocess.Popen(exe_path, shell=True)
        except Exception as e:
            # Show an error message if execution fails
            messagebox.showerror("Execution Error", f"Failed to execute: {exe_path}\nError: {e}")

    def rebuild_treeview(self, data, parent=''):
        # Separate folders and executables without sorting
        folders = {k: v for k, v in data.items() if isinstance(v, dict) and 'path' not in v}
        executables = {k: v for k, v in data.items() if isinstance(v, dict) and 'path' in v}

        # Insert folders first
        for folder_name, folder_content in folders.items():
            # Insert folder into the treeview
            item_id = self.tree.insert(parent, "end", text=folder_name, open=True)
            # Recursively rebuild the treeview for this folder's children
            self.rebuild_treeview(folder_content, item_id)

        # Insert executables after folders
        for exe_name, exe_content in executables.items():
            # Insert executable into the treeview
            exe_path = exe_content['path']
            exe_emoji = exe_content['emoji']
            self.tree.insert(parent, "end", text=f"{exe_emoji} {exe_name}", values=(exe_path,))


    def search_items(self, event=None):
        # Get the search query
        search_query = self.search_entry.get().strip().lower()
        
        # If the search query is empty, reset the treeview
        if not search_query:
            self.reset_treeview()
            return

        # Perform the search on the data structure
        filtered_data = self.search_in_data_structure(self.tree_data, search_query)

        # Clear and rebuild the treeview with the filtered data
        self.tree.delete(*self.tree.get_children())
        self.rebuild_treeview(filtered_data)

    def search_in_data_structure(self, data, query):
        filtered_data = {}

        for key, value in data.items():
            # Convert the key and path to lowercase for case-insensitive search
            key_lower = key.lower()

            if isinstance(value, dict):
                # Recursively search in folders
                result = self.search_in_data_structure(value, query)
                if result or query in key_lower:
                    # Include the folder if it or its children match the query
                    filtered_data[key] = result if result else value
            else:
                # Check if the executable name or path contains the query
                path_lower = value['path'].lower()
                if query in key_lower or query in path_lower:
                    filtered_data[key] = value

        return filtered_data

    def reset_treeview(self):
        # Reset the treeview to show the entire data structure
        self.tree.delete(*self.tree.get_children())
        self.rebuild_treeview(self.tree_data)

    def sort_items(self):
        # Sort the underlying data structure
        self.tree_data = self.sort_data_structure(self.tree_data)

        # Clear the treeview and repopulate it
        self.tree.delete(*self.tree.get_children())
        self.rebuild_treeview(self.tree_data)

        # Save the sorted treeview
        self.save_data()

    def sort_data_structure(self, data):
        # Sort folders and executables
        sorted_data = {}
        folders = {k: v for k, v in data.items() if isinstance(v, dict)}
        executables = {k: v for k, v in data.items() if not isinstance(v, dict)}

        # Sort folders and executables alphabetically
        for folder_name in sorted(folders):
            sorted_data[folder_name] = self.sort_data_structure(folders[folder_name])

        for exe_name in sorted(executables):
            sorted_data[exe_name] = executables[exe_name]

        return sorted_data

    def on_drag_start(self, event):
        try:
            # Identify the item being dragged
            item_id = self.tree.identify_row(event.y)
            if item_id:
                self.dragging_item = item_id
                # Create a floating label to follow the mouse cursor
                item_text = self.tree.item(item_id, 'text')
                self.drag_label = tk.Label(
                    self, 
                    text=item_text, 
                    relief='solid', 
                    bg='#333333',  # Dark background color
                    fg='white',    # White text color for contrast
                    font=('Arial', 10, 'bold'),  # Bold font for better readability
                    padx=5,        # Padding for a cleaner look
                    pady=2
                )
                # Place the label near the cursor
                self.drag_label.place(x=event.x_root, y=event.y_root)
        except AttributeError:
            # Swallow the AttributeError and do nothing
            pass


    def on_drag_motion(self, event):
        # Highlight the potential drop target and move the floating label
        if self.dragging_item and self.drag_label:
            target_item = self.tree.identify_row(event.y)
            self.tree.selection_set(target_item)
            
            # Move the floating label to follow the mouse cursor
            self.drag_label.place(x=event.x_root + 10, y=event.y_root + 10)  # Offset for better visibility

    def on_drag_release(self, event):
        if self.dragging_item:
            # Hide or destroy the floating label
            if self.drag_label:
                self.drag_label.destroy()
                self.drag_label = None
            
            # Identify the drop target
            target_item = self.tree.identify_row(event.y)

            # If target_item is not valid or is the same as dragging_item, return without making changes
            if not target_item or target_item == self.dragging_item:
                self.dragging_item = None
                return

            # Get the parent of the target item
            target_parent = self.tree.parent(target_item)
            
            # Prevent dropping into an executable
            if self.tree.item(target_item, 'values') and self.tree.item(target_parent, 'values'):
                self.dragging_item = None
                messagebox.showerror("Invalid Drop", "Cannot drop into an executable.")
                return

            # Move the item in the data structure
            item_name = self.tree.item(self.dragging_item, 'text').split(' ', 1)[-1]
            dragging_path = self.get_data_path(self.dragging_item)
            dragging_parent = self.get_current_level(self.tree_data, dragging_path[:-1])
            item_data = dragging_parent.pop(item_name)

            # If the drop target is an executable, place the dragged item above it
            if self.tree.item(target_item, 'values'):
                # Get the level for the parent
                target_path = self.get_data_path(target_parent)
                target_level = self.get_current_level(self.tree_data, target_path)
                
                # Insert the item above the target item in the parent
                new_target_data = {}
                for key, value in target_level.items():
                    if key == self.tree.item(target_item, 'text').split(' ', 1)[-1]:
                        # Place the dragged item before the target item
                        new_target_data[item_name] = item_data
                    # Insert the original items
                    new_target_data[key] = value

                # Replace the parent level with the new order
                target_level.clear()
                target_level.update(new_target_data)

                # Move the dragged item in the treeview
                self.tree.move(self.dragging_item, target_parent, self.tree.index(target_item))
            else:
                # If not dropping on an executable, add to the new parent normally
                target_path = self.get_data_path(target_item)
                target_parent_level = self.get_current_level(self.tree_data, target_path)
                target_parent_level[item_name] = item_data
                
                # Move the dragged item in the treeview
                self.tree.move(self.dragging_item, target_item, 'end')

            # Clear the dragging state
            self.dragging_item = None

            # Save the updated treeview to the data file
            self.save_data()


    def load_data(self):
        try:
            # Load self.tree_data from a JSON file
            with open(DATA_FILE, 'r') as file:
                self.tree_data = json.load(file)
            
            # Clear the treeview and rebuild it using the loaded data
            self.tree.delete(*self.tree.get_children())
            self.rebuild_treeview(self.tree_data)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is malformed, initialize default data
            self.initialize_default_data()

    def initialize_default_data(self):
        # Initialize a default data structure
        self.tree_data = {
            "Root": {
            }
        }

        # Clear the current treeview and rebuild it using the default data
        self.tree.delete(*self.tree.get_children())
        self.rebuild_treeview(self.tree_data)

    def save_data(self):
        # Save self.tree_data to a JSON file
        with open(DATA_FILE, 'w') as file:
            json.dump(self.tree_data, file, indent=4)

# Run the application
if __name__ == "__main__":
    app = ExecutableLauncherApp()
    app.mainloop()
