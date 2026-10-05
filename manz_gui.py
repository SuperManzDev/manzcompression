import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import manz_compressor # Imports our core logic
import os

class ManzGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Manz Compressor Tool")
        self.geometry("550x420") # Made window a bit taller
        self.minsize(500, 420)

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1) # Make column 1 (fields) expandable

        # --- 1. Mode Selection ---
        self.mode_var = tk.StringVar(value="compress")
        
        mode_frame = ttk.Frame(main_frame)
        ttk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            mode_frame, text="Compress", variable=self.mode_var, 
            value="compress", command=self.update_ui
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            mode_frame, text="Decompress", variable=self.mode_var, 
            value="decompress", command=self.update_ui
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            mode_frame, text="List Contents", variable=self.mode_var, 
            value="list", command=self.update_ui
        ).pack(side=tk.LEFT, padx=5)
        
        mode_frame.grid(row=0, column=0, columnspan=3, sticky="w", pady=5)

        # --- 2. Source Path ---
        self.source_label = ttk.Label(main_frame, text="Source:")
        self.source_label.grid(row=1, column=0, sticky="e", padx=5)
        
        self.source_path = tk.StringVar()
        source_field = ttk.Entry(main_frame, textvariable=self.source_path)
        source_field.grid(row=1, column=1, sticky="ew")
        
        self.source_btn = ttk.Button(main_frame, text="Browse...", command=self.browse_source)
        self.source_btn.grid(row=1, column=2, padx=5)

        # --- 3. Destination Path ---
        self.dest_label = ttk.Label(main_frame, text="Destination:")
        self.dest_label.grid(row=2, column=0, sticky="e", padx=5)
        
        self.dest_path = tk.StringVar()
        self.dest_field = ttk.Entry(main_frame, textvariable=self.dest_path)
        self.dest_field.grid(row=2, column=1, sticky="ew")
        
        self.dest_btn = ttk.Button(main_frame, text="Browse...", command=self.browse_dest)
        self.dest_btn.grid(row=2, column=2, padx=5)

        # --- 4. Compression Options ---
        self.compress_options_frame = ttk.LabelFrame(main_frame, text="Compression Options", padding=10)
        self.compress_options_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        self.compress_options_frame.columnconfigure(1, weight=1)

        # Method Dropdown
        ttk.Label(self.compress_options_frame, text="Method:").grid(row=0, column=0, sticky="e", padx=5)
        self.method_var = tk.StringVar(value="deflate")
        method_combo = ttk.Combobox(
            self.compress_options_frame, 
            textvariable=self.method_var, 
            values=manz_compressor.get_available_methods(), 
            state='readonly'
        )
        method_combo.grid(row=0, column=1, sticky="ew", padx=5)

        # Level Slider
        ttk.Label(self.compress_options_frame, text="Level (9=Max):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.comp_level = tk.DoubleVar(value=9)
        self.slider = ttk.Scale(
            self.compress_options_frame, from_=1, to=9, orient=tk.HORIZONTAL,
            variable=self.comp_level,
            command=lambda v: self.comp_level.set(round(float(v))) # Snap to integer
        )
        self.slider.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # --- 5. Action Button ---
        self.action_btn = ttk.Button(main_frame, text="Compress", command=self.run_action)
        self.action_btn.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)

        # --- 6. Footer (Branding & Status) ---
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10,0))
        
        self.status_var = tk.StringVar(value="Ready. Select mode and paths.")
        status_label = ttk.Label(footer_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        brand_label = ttk.Label(footer_frame, text="Made by Manz @manz.shh", font=("Arial", 8))
        brand_label.pack(side=tk.RIGHT, padx=5)
        
        self.update_ui() # Set initial UI state

    def update_ui(self):
        """Hides/shows widgets based on the selected mode."""
        mode = self.mode_var.get()
        if mode == "compress":
            self.source_label.config(text="Source (File/Dir):")
            self.dest_label.config(text="Destination (.manz):")
            self.action_btn.config(text="Compress")
            # Show destination path
            self.dest_label.grid()
            self.dest_field.grid()
            self.dest_btn.grid()
            # Show compression options
            self.compress_options_frame.grid()
        
        elif mode == "decompress":
            self.source_label.config(text="Source (.manz):")
            self.dest_label.config(text="Output Folder:")
            self.action_btn.config(text="Decompress")
            # Show destination path
            self.dest_label.grid()
            self.dest_field.grid()
            self.dest_btn.grid()
            # Hide compression options
            self.compress_options_frame.grid_remove()
            
        elif mode == "list":
            self.source_label.config(text="Source (.manz):")
            self.action_btn.config(text="List Contents")
            # Hide destination path
            self.dest_label.grid_remove()
            self.dest_field.grid_remove()
            self.dest_btn.grid_remove()
            # Hide compression options
            self.compress_options_frame.grid_remove()

    def browse_source(self):
        mode = self.mode_var.get()
        path = ""
        if mode == "compress":
            # This is how we handle "multiple files" - ask for a folder
            if messagebox.askyesno("Select Source", "Do you want to compress an entire FOLDER? (Select 'No' to pick a single file)."):
                path = filedialog.askdirectory(title="Select Source Folder")
            else:
                path = filedialog.askopenfilename(title="Select Source File")
            self.source_path.set(path)
        else: # Decompress or List
            path = filedialog.askopenfilename(
                title="Select .manz File",
                filetypes=[("Manz files", "*.manz"), ("Zip files", "*.zip"), ("All files", "*.*")]
            )
            self.source_path.set(path)

    def browse_dest(self):
        mode = self.mode_var.get()
        path = ""
        if mode == "compress":
            path = filedialog.asksaveasfilename(
                title="Save .manz File As",
                defaultextension=".manz",
                filetypes=[("Manz files", "*.manz")]
            )
        else: # Decompress
            path = filedialog.askdirectory(title="Select Output Folder")
        self.dest_path.set(path)

    def show_list_popup(self, contents):
        """Displays a new window with the list of files."""
        popup = tk.Toplevel(self)
        popup.title(f"Contents of {os.path.basename(self.source_path.get())}")
        popup.geometry("400x500")
        
        # Add a scrollable text area
        txt_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=60, height=25)
        txt_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        if contents:
            txt_area.insert(tk.INSERT, f"Found {len(contents)} items:\n\n")
            txt_area.insert(tk.INSERT, "\n".join(contents))
        else:
            txt_area.insert(tk.INSERT, "No contents found or file is empty.")
            
        txt_area.config(state=tk.DISABLED) # Make read-only
        
        close_btn = ttk.Button(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=10)
        
        popup.transient(self) # Keep popup on top
        popup.grab_set() # Modal
        self.wait_window(popup) # Wait until popup is closed

    def run_action(self):
        """Runs the action in a background thread to prevent GUI freeze."""
        source = self.source_path.get()
        dest = self.dest_path.get()
        mode = self.mode_var.get()

        if not source:
            messagebox.showerror("Error", "Source path is required.")
            return
        if mode != "list" and not dest:
            messagebox.showerror("Error", "Destination path is required.")
            return

        self.action_btn.config(state=tk.DISABLED)
        self.status_var.set("Working...")

        # Run in a separate thread
        threading.Thread(target=self.action_thread, args=(mode, source, dest), daemon=True).start()

    def action_thread(self, mode, source, dest):
        """The actual work that runs in the background."""
        try:
            if mode == "compress":
                level = int(self.comp_level.get())
                method = self.method_var.get()
                success = manz_compressor.compress(source, dest, level, method)
                if success:
                    self.status_var.set(f"Successfully compressed to {os.path.basename(dest)}")
                else:
                    self.status_var.set("Error during compression. Check console.")
            
            elif mode == "decompress":
                success = manz_compressor.decompress(source, dest)
                if success:
                    self.status_var.set(f"Successfully decompressed to {os.path.basename(dest)}")
                else:
                    self.status_var.set("Error during decompression. Check console.")
            
            elif mode == "list":
                contents = manz_compressor.list_contents(source)
                if contents:
                    self.status_var.set(f"Listed {len(contents)} items.")
                    # We must show the popup from the main thread
                    self.after(0, self.show_list_popup, contents) 
                else:
                    self.status_Tvar.set("Could not list contents. Check console.")

        except Exception as e:
            self.status_var.set(f"Error: {e}")
        
        finally:
            # Re-enable the button (must be done on the main thread)
            self.after(0, lambda: self.action_btn.config(state=tk.NORMAL))

if __name__ == "__main__":
    app = ManzGUI()
    app.mainloop()