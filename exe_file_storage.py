import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import os
import subprocess
import json

# File to store the list of exe files and custom names
DATA_FILE = "exe_list.json"

class ExeLauncherApp:
    def __init__(self, root):
        self.root = root
        self.exe_list = {
        "executables": [
            {
                "name": "Test",
                "path": "C:/Test/Test.exe",
                "emoji": "🌟",
                "group": "Root"
            },
            {
                "name": "Kind Words",
                "path": "C:/Games/Kind Words.exe",
                "emoji": "🌟",
                "group": "Games"
            },
            {
                "name": "Rocket League",
                "path": "C:/Games/Rocket League.exe",
                "emoji": "🚀",
                "group": "Action"
            },
            {
                "name": "Doom Eternal",
                "path": "C:/Games/Doom Eternal.exe",
                "emoji": "🔫",
                "group": "Action"
            },
            {
                "name": "Stardew Valley",
                "path": "C:/Games/Stardew Valley.exe",
                "emoji": "🌾",
                "group": "Strategy"
            },
            {
                "name": "Civilization VI",
                "path": "C:/Games/Civilization VI.exe",
                "emoji": "🌍",
                "group": "Strategy"
            },
            {
                "name": "Skyrim Mod Organizer",
                "path": "C:/Mods/Skyrim Mod Organizer.exe",
                "emoji": "🗺️",
                "group": "Mod Lists"
            },
            {
                "name": "Fallout 4 Mod Manager",
                "path": "C:/Mods/Fallout 4 Mod Manager.exe",
                "emoji": "🔧",
                "group": "Mod Lists"
            }
        ],
        "groups": [
            {
                "name": "Games",
                "sub_groups": [
                    {"name": "Action", "sub_groups": []},
                    {"name": "Adventure", "sub_groups": []},
                    {"name": "Strategy", "sub_groups": []},
                ],
            },
            {
                "name": "Mod Lists",
                "sub_groups": []
            }
        ]
    }
        self.construct_ui()
   
    def construct_ui(self):
        self.root.title("Executable Launcher")
        self.root.geometry("1000x575")
        
        # Set dark mode colors
        self.bg_color = "#2e2e2e"  # Dark background
        self.fg_color = "#ffffff"  # White text
        self.highlight_color = "#4a4a4a"  # Slightly lighter background for widgets

        # Use the 'clam' theme
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure custom styles for widgets
        self.style.configure("Custom.Treeview",
                             background=self.bg_color,
                             foreground=self.fg_color,
                             fieldbackground=self.bg_color,
                             borderwidth=0)
        
        self.style.configure("Custom.TButton",
                             background=self.highlight_color,
                             foreground=self.fg_color,
                             borderwidth=1)
        
        self.style.map("Custom.TButton",
                       background=[('active', '#666666')],
                       foreground=[('active', '#ffffff')])

        # self.exe_list = {}
        self.load_exe_list()

        # Create treeview
        self.treeview = ttk.Treeview(self.root, columns=("path",), show="tree", style="Custom.Treeview")
        self.treeview.configure(style="Custom.Treeview")
        self.treeview.heading("#0", text="Name")
        self.treeview.heading("path", text="Path")
        self.treeview.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu: Focused on general app options
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Group Menu: Focused on group-related actions
        self.group_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Group", menu=self.group_menu)
        self.group_menu.add_command(label="Add Group", command=self.add_group)
        self.group_menu.add_command(label="Delete Group", command=self.delete_group)

        # EXE Menu: Focused on EXE management actions
        self.exe_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="EXE", menu=self.exe_menu)
        self.exe_menu.add_command(label="Add EXE", command=self.add_exe)
        self.exe_menu.add_command(label="Remove EXE", command=self.remove_exe)
        self.exe_menu.add_command(label="Edit EXE", command=self.edit_exe)
        self.exe_menu.add_command(label="Sort List", command=self.sort_list)

        # Execute Menu: Dedicated to executing EXE files
        self.execute_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Execute", menu=self.execute_menu)
        self.execute_menu.add_command(label="Execute Selected EXE", command=self.execute_exe)

        # Create frame for top buttons
        self.top_buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        self.top_buttons_frame.pack(pady=5, fill=tk.X)

        # Create frame for bottom buttons
        self.bottom_buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        self.bottom_buttons_frame.pack(pady=5, fill=tk.X)

        # Add buttons to bottom frame using grid layout
        self.bottom_buttons_frame.columnconfigure(0, weight=1)
        self.bottom_buttons_frame.columnconfigure(1, weight=1)
        self.bottom_buttons_frame.columnconfigure(2, weight=1)
        self.bottom_buttons_frame.columnconfigure(3, weight=1)

        self.remove_button = ttk.Button(self.bottom_buttons_frame, text="Remove EXE", command=self.remove_exe, style="Custom.TButton")
        self.remove_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(self.bottom_buttons_frame, text="Edit EXE", command=self.edit_exe, style="Custom.TButton")
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.sort_button = ttk.Button(self.bottom_buttons_frame, text="Sort List Alphabetically", command=self.sort_list, style="Custom.TButton")
        self.sort_button.grid(row=0, column=2, padx=5, pady=5)

        self.delete_group_button = ttk.Button(self.bottom_buttons_frame, text="Delete Group", command=self.delete_group, style="Custom.TButton")
        self.delete_group_button.grid(row=0, column=3, padx=5, pady=5)

        # Add buttons to top frame using grid layout with adjusted column placement
        self.top_buttons_frame.columnconfigure(0, weight=1)
        self.top_buttons_frame.columnconfigure(1, weight=1)
        self.top_buttons_frame.columnconfigure(2, weight=1)
        self.top_buttons_frame.columnconfigure(3, weight=1)
        self.top_buttons_frame.columnconfigure(4, weight=1)
        self.top_buttons_frame.columnconfigure(5, weight=1)
        self.top_buttons_frame.columnconfigure(6, weight=1)

        self.add_group_button = ttk.Button(self.top_buttons_frame, text="Add Group", command=self.add_group, style="Custom.TButton")
        self.add_group_button.grid(row=0, column=1, padx=5, pady=5)

        self.add_exe_button = ttk.Button(self.top_buttons_frame, text="Add EXE", command=self.add_exe, style="Custom.TButton")
        self.add_exe_button.grid(row=0, column=3, padx=5, pady=5)

        self.execute_exe_button = ttk.Button(self.top_buttons_frame, text="Execute EXE", command=self.execute_exe, style="Custom.TButton")
        self.execute_exe_button.grid(row=0, column=5, padx=5, pady=5)

        # Create a context menu with all options
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Add Group", command=self.add_group)
        self.context_menu.add_command(label="Add EXE", command=self.add_exe)
        self.context_menu.add_command(label="Remove EXE", command=self.remove_exe)
        self.context_menu.add_command(label="Edit EXE", command=self.edit_exe)
        self.context_menu.add_command(label="Sort List Alphabetically", command=self.sort_list)
        self.context_menu.add_command(label="Delete Group", command=self.delete_group)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Execute Selected EXE", command=self.execute_exe)

        # Bind context menu to right click on treeview
        self.treeview.bind("<Button-3>", self.show_context_menu)

        # Configure root window background color
        self.root.configure(bg=self.bg_color)

        self.update_treeview()

    def show_context_menu(self, event):
        """Display the context menu."""
        try:
            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def add_group(self):
        """Add a new group."""
        # Prompt the user for the new group name
        group_name = simpledialog.askstring("Input", "Enter a name for the new group:", parent=self.root)
        
        if group_name:
            if group_name == "Root":
                messagebox.showwarning("Invalid Name", "The group name 'Root' is not allowed.")
                return

            selected_item = self.treeview.selection()  # Check if any item is selected
            if not selected_item:
                # No item is selected, so add the group to the root level
                if any(group['name'] == group_name for group in self.exe_list['groups']):
                    messagebox.showwarning("Duplicate", "This group already exists.")
                else:
                    new_group = {"name": group_name, "sub_groups": []}
                    self.exe_list['groups'].append(new_group)
                    self.save_exe_list()
                    self.update_treeview()
            else:
                # An item is selected, so check if it's a group or an executable
                selected_item_id = selected_item[0]
                selected_item_text = self.treeview.item(selected_item_id, "text")
                
                # Check if the selected item is a group or executable
                if self.treeview.item(selected_item_id, "values"):
                    # Selected item is an executable
                    messagebox.showwarning("Invalid Selection", "You cannot add a group to an executable.")
                else:
                    # Selected item is a group
                    parent_group_name = selected_item_text
                    parent_group = self.find_group_by_name(self.exe_list['groups'], parent_group_name)
                    if parent_group:
                        if any(group['name'] == group_name for group in parent_group['sub_groups']):
                            messagebox.showwarning("Duplicate", "This group already exists.")
                        else:
                            parent_group['sub_groups'].append({"name": group_name, "sub_groups": []})
                            self.save_exe_list()
                            self.update_treeview()

    def find_group_by_name(self, groups, name):
        """Recursively find a group by name in the groups list."""
        for group in groups:
            if group['name'] == name:
                return group
            found = self.find_group_by_name(group['sub_groups'], name)
            if found:
                return found
        return None

    def add_exe(self):
        """Add an executable to the selected group with a custom name and emoji."""
        selected_item = self.treeview.selection()
        if selected_item:
            group_name = self.treeview.item(selected_item[0], "text")
            if group_name in self.exe_list:
                file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
                if file_path:
                    custom_name = simpledialog.askstring("Input", "Enter a custom name for this EXE:", parent=self.root)
                    if custom_name:
                        emoji = simpledialog.askstring("Input", "Enter a custom emoji for this EXE (optional):", parent=self.root)
                        if emoji is None or emoji.strip() == '':
                            emoji = '📁'
                        entry = {"path": file_path, "name": custom_name, "emoji": emoji if emoji else ""}
                        if entry not in self.exe_list[group_name]:
                            self.exe_list[group_name].append(entry)
                            self.save_exe_list()
                            self.update_treeview()
                        else:
                            messagebox.showwarning("Duplicate", "This EXE is already in the group.")
                    else:
                        messagebox.showwarning("Input Error", "Custom name cannot be empty.")
            else:
                messagebox.showwarning("Group Error", "The specified group does not exist.")
        else:
            messagebox.showwarning("Group Not Selected", "The chosen item was not a group.")

    def remove_exe(self):
        """Remove selected exe from the list."""
        selected_item = self.treeview.selection()
        if selected_item:
            try:
                selected_text = self.treeview.item(selected_item[0], "text")
                parent_item = self.treeview.parent(selected_item[0])
                if parent_item:
                    group_name = self.treeview.item(parent_item, "text")
                    exe_name = selected_text.split(" - ", 1)[0].strip()
                    exe_to_remove = next((exe for exe in self.exe_list[group_name] if exe["name"] in exe_name), None)
                    
                    if exe_to_remove:
                        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{exe_name}'?")
                        if confirm:
                            self.exe_list[group_name].remove(exe_to_remove)
                            self.save_exe_list()
                            self.update_treeview()
                    else:
                        messagebox.showwarning("Selection Error", "Selected item is not an executable.")
                else:
                    messagebox.showwarning("Selection Error", "Selected item is not an executable.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove executable: {e}")
    
    def execute_exe(self):
        """Execute the selected EXE file."""
        selected_item = self.treeview.selection()
        if selected_item:
            try:
                selected_text = self.treeview.item(selected_item[0], "text")
                parent_item = self.treeview.parent(selected_item[0])
                if parent_item:
                    group_name = self.treeview.item(parent_item, "text")
                    exe_name = selected_text.split(" - ", 1)[0].strip()
                    exe_to_run = next((exe for exe in self.exe_list[group_name] if exe["name"] in exe_name), None)
                    if exe_to_run:
                        subprocess.Popen(exe_to_run["path"], shell=True)
                    else:
                        messagebox.showwarning("Selection Error", "Selected item is not an executable.")
                else:
                    messagebox.showwarning("Selection Error", "Selected item is not an executable.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute executable: {e}")

    def edit_exe(self):
        """Edit the selected executable's name, path, and emoji."""
        selected_item = self.treeview.selection()
        if selected_item:
            try:
                selected_text = self.treeview.item(selected_item[0], "text")
                parent_item = self.treeview.parent(selected_item[0])
                if parent_item:
                    group_name = self.treeview.item(parent_item, "text")
                    exe_name = selected_text.split(" - ", 1)[0].strip()
                    exe_to_edit = next((exe for exe in self.exe_list[group_name] if exe["name"] in exe_name), None)
                    if exe_to_edit:
                        new_name = simpledialog.askstring("Input", "Enter a new name for this EXE:", initialvalue=exe_to_edit["name"], parent=self.root)
                        directory_path = os.path.dirname(exe_to_edit["path"])
                        new_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")], initialdir=directory_path, initialfile=exe_to_edit["path"])
                        new_emoji = simpledialog.askstring("Input", "Enter a new emoji for this EXE (optional):", initialvalue=exe_to_edit["emoji"], parent=self.root)
                        if new_name and new_path:
                            exe_to_edit["name"] = new_name
                            exe_to_edit["path"] = new_path
                            exe_to_edit["emoji"] = new_emoji if new_emoji else '📁'  # Default emoji if not provided
                            self.save_exe_list()
                            self.update_treeview()
                        else:
                            messagebox.showwarning("Input Error", "Values cannot be empty.")
                    else:
                        messagebox.showwarning("Selection Error", "Selected item is not an executable.")
                else:
                    messagebox.showwarning("Selection Error", "Selected item is not an executable.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit executable: {e}")

    def sort_list(self):
        """Sort groups and executables within each group alphabetically."""
        for group in self.exe_list:
            self.exe_list[group].sort(key=lambda x: x["name"].lower())
        sorted_groups = sorted(self.exe_list.keys(), key=lambda x: x.lower())
        self.exe_list = {group: self.exe_list[group] for group in sorted_groups}
        self.save_exe_list()
        self.update_treeview()

    def delete_group(self):
        """Delete the selected group."""
        selected_item = self.treeview.selection()
        if selected_item:
            try:
                selected_text = self.treeview.item(selected_item[0], "text")
                parent_item = self.treeview.parent(selected_item[0])
                if not parent_item:
                    # Confirm group deletion
                    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the group '{selected_text}' and all its executables?")
                    if confirm:
                        if selected_text in self.exe_list:
                            del self.exe_list[selected_text]
                            self.save_exe_list()
                            self.update_treeview()
                        else:
                            messagebox.showwarning("Deletion Error", "Selected group not found.")
                else:
                    messagebox.showwarning("Selection Error", "Selected item is not a group.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete group: {e}")

    def save_exe_list(self):
        """Save the list of exe files and custom names to a JSON file."""
        # with open(DATA_FILE, 'w') as f:
        #     json.dump(self.exe_list, f, indent=4)

    def load_exe_list(self):
        """Load the list of exe files and custom names from a JSON file."""
        # if os.path.exists(DATA_FILE):
        #     with open(DATA_FILE, 'r') as f:
        #         self.exe_list = json.load(f)
    
    def update_treeview(self):
        """Update the Treeview with the current exe list and custom names."""
        self.treeview.delete(*self.treeview.get_children())
        group_node_ids = {}

        def add_group(parent, group):
            group_node_ids[group['name']] = self.treeview.insert(parent, 'end', text=group['name'])
            for sub_group in group['sub_groups']:
                add_group(group_node_ids[group['name']], sub_group)

        # Add main groups
        for group in self.exe_list['groups']:
            add_group('', group)

        # Add executables under their respective groups, except "Root"
        for executable in self.exe_list['executables']:
            group = executable['group']
            if group != "Root" and group in group_node_ids:
                self.treeview.insert(group_node_ids[group], 'end', 
                                     text=f"{executable['emoji']} {executable['name']}",
                                     values=(executable['path']))

        # Add executables for the "Root" group last, as root level items
        for executable in self.exe_list['executables']:
            if executable['group'] == "Root":
                self.treeview.insert('', 'end', 
                                     text=f"{executable['emoji']} {executable['name']}",
                                     values=(executable['path']))


# Main code to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExeLauncherApp(root)
    root.mainloop()