import customtkinter as ctk
import random
import time
import threading
from PIL import Image, ImageDraw
import numpy as np
from typing import List, Tuple, Optional
import math
from sorting_algorithms import SortingAlgorithms
import os
from datetime import datetime

class SortingVisualizer:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Sorting Simulator - Educational Edition")
        self.window.geometry("1400x900")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.array = []
        self.array_size = ctk.IntVar(value=20)
        self.sorting_speed = ctk.IntVar(value=50)
        self.is_sorting = False
        self.current_algorithm = ctk.StringVar(value="Bubble Sort")
        self.step_by_step = ctk.BooleanVar(value=False)
        
        # Colors for visualization
        self.colors = {
            "normal": "#3b82f6",      # Blue
            "comparing": "#f59e0b",   # Yellow
            "swapping": "#ef4444",    # Red
            "sorted": "#10b981",      # Green
            "pivot": "#8b5cf6",       # Purple
            "min": "#ec4899",         # Pink
            "background": "#2b2b2b",  # Dark background
            "text": "#ffffff"         # White text
        }
        
        # Track array states for screenshots
        self.initial_array = None
        self.final_array = None
        
        # Initialize sorting algorithms
        self.sorting_algorithms = SortingAlgorithms(self.update_visualization)
        
        self.setup_ui()
        self.generate_random_array()
        
    def setup_ui(self):
        # Create main container with tabs
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create tabs (removed Learning Mode)
        self.tabview.add("Visualization")
        self.tabview.add("Comparison")
        
        # Setup each tab
        self.setup_visualization_tab()
        self.setup_comparison_tab()
        
    def setup_visualization_tab(self):
        """Setup the main visualization tab"""
        tab = self.tabview.tab("Visualization")
        
        # Create main container with better spacing
        self.main_container = ctk.CTkFrame(tab)
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Add title with better styling
        self.title_frame = ctk.CTkFrame(self.main_container)
        self.title_frame.pack(fill="x", pady=(0, 15))
        
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Sorting Simulator",
            font=("Arial", 32, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Create left and right panels
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(fill="both", expand=True)
        
        # Create left panel (70% width)
        self.left_panel = ctk.CTkFrame(self.content_frame)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Create right panel (30% width)
        self.right_panel = ctk.CTkFrame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", padx=(10, 0))
        
        # Move all existing visualization components to the left panel
        self.setup_canvas_frame()
        self.setup_controls_frame()
        self.setup_buttons_frame()
        self.setup_custom_array_frame()
        self.setup_legend_frame()
        
        # Move all existing info components to the right panel
        self.setup_stats_frame()
        self.setup_info_frame()
        
        # Add step-by-step toggle
        self.step_toggle = ctk.CTkSwitch(
            self.left_panel,
            text="Step-by-Step Mode",
            variable=self.step_by_step,
            command=self.toggle_step_by_step
        )
        self.step_toggle.pack(pady=5)
        
    def setup_canvas_frame(self):
        """Setup the canvas frame in the left panel"""
        self.canvas_frame = ctk.CTkFrame(self.left_panel)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add array state display
        self.array_state_frame = ctk.CTkFrame(self.canvas_frame)
        self.array_state_frame.pack(fill="x", padx=10, pady=5)
        
        self.initial_array_label = ctk.CTkLabel(
            self.array_state_frame,
            text="Initial Array: ",
            font=("Arial", 14, "bold")
        )
        self.initial_array_label.pack(side="left", padx=5)
        
        self.initial_array_value = ctk.CTkLabel(
            self.array_state_frame,
            text="[]",
            font=("Arial", 14)
        )
        self.initial_array_value.pack(side="left", padx=5)
        
        self.final_array_label = ctk.CTkLabel(
            self.array_state_frame,
            text="Final Array: ",
            font=("Arial", 14, "bold")
        )
        self.final_array_label.pack(side="left", padx=5)
        
        self.final_array_value = ctk.CTkLabel(
            self.array_state_frame,
            text="[]",
            font=("Arial", 14)
        )
        self.final_array_value.pack(side="left", padx=5)
        
        # Canvas title
        self.canvas_title = ctk.CTkLabel(
            self.canvas_frame,
            text="Array Visualization",
            font=("Arial", 20, "bold")
        )
        self.canvas_title.pack(pady=5)
        
        # Create canvas
        self.canvas = ctk.CTkCanvas(
            self.canvas_frame,
            bg=self.colors["background"],
            highlightthickness=0,
            height=400
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)
        
        # State indicator
        self.state_indicator = ctk.CTkLabel(
            self.canvas_frame,
            text="Current State: Normal",
            font=("Arial", 14, "bold")
        )
        self.state_indicator.pack(pady=5)
        
    def setup_controls_frame(self):
        """Setup the controls frame in the left panel"""
        self.controls_frame = ctk.CTkFrame(self.left_panel)
        self.controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Algorithm selection
        self.algorithm_label = ctk.CTkLabel(self.controls_frame, text="Algorithm:")
        self.algorithm_label.pack(side="left", padx=5)
        
        self.algorithm_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=["Bubble Sort", "Selection Sort", "Insertion Sort", 
                   "Merge Sort", "Quick Sort", "Heap Sort", 
                   "Counting Sort", "Radix Sort", "Bucket Sort"],
            variable=self.current_algorithm,
            command=self.on_algorithm_change
        )
        self.algorithm_menu.pack(side="left", padx=5)
        
        # Array size slider
        self.size_label = ctk.CTkLabel(self.controls_frame, text="Array Size:")
        self.size_label.pack(side="left", padx=5)
        
        self.size_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=5,
            to=100,
            number_of_steps=95,
            variable=self.array_size,
            command=self.on_size_change
        )
        self.size_slider.pack(side="left", padx=5, fill="x", expand=True)
        
        self.size_value_label = ctk.CTkLabel(self.controls_frame, text=str(self.array_size.get()))
        self.size_value_label.pack(side="left", padx=5)
        
        # Speed slider
        self.speed_label = ctk.CTkLabel(self.controls_frame, text="Speed:")
        self.speed_label.pack(side="left", padx=5)
        
        self.speed_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=1,
            to=100,
            number_of_steps=99,
            variable=self.sorting_speed
        )
        self.speed_slider.pack(side="left", padx=5, fill="x", expand=True)
        
    def setup_buttons_frame(self):
        """Setup the buttons frame in the left panel"""
        self.buttons_frame = ctk.CTkFrame(self.left_panel)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)
        
        self.generate_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Generate New Array",
            command=self.generate_random_array
        )
        self.generate_btn.pack(side="left", padx=5)
        
        self.sort_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Start Sorting",
            command=self.start_sorting
        )
        self.sort_btn.pack(side="left", padx=5)
        
    def setup_custom_array_frame(self):
        """Setup the custom array input frame in the left panel"""
        self.custom_array_frame = ctk.CTkFrame(self.left_panel)
        self.custom_array_frame.pack(fill="x", padx=10, pady=5)
        
        self.custom_array_label = ctk.CTkLabel(self.custom_array_frame, text="Custom Array:")
        self.custom_array_label.pack(side="left", padx=5)
        
        self.custom_array_entry = ctk.CTkEntry(
            self.custom_array_frame,
            placeholder_text="Enter comma-separated numbers (e.g., 5,3,8,1,2)"
        )
        self.custom_array_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.use_custom_array_btn = ctk.CTkButton(
            self.custom_array_frame,
            text="Use Custom Array",
            command=self.use_custom_array
        )
        self.use_custom_array_btn.pack(side="left", padx=5)
        
    def setup_legend_frame(self):
        """Setup the legend frame in the left panel"""
        self.legend_frame = ctk.CTkFrame(self.left_panel)
        self.legend_frame.pack(fill="x", padx=10, pady=5)
        
        # Create legend items
        legend_items = [
            ("Normal", self.colors["normal"]),
            ("Comparing", self.colors["comparing"]),
            ("Swapping", self.colors["swapping"]),
            ("Sorted", self.colors["sorted"]),
            ("Pivot", self.colors["pivot"]),
            ("Minimum", self.colors["min"])
        ]
        
        for text, color in legend_items:
            item_frame = ctk.CTkFrame(self.legend_frame)
            item_frame.pack(side="left", padx=5)
            
            color_box = ctk.CTkCanvas(item_frame, width=20, height=20, bg=color, highlightthickness=0)
            color_box.pack(side="left", padx=2)
            
            label = ctk.CTkLabel(item_frame, text=text)
            label.pack(side="left", padx=2)
            
    def setup_stats_frame(self):
        """Setup the statistics frame in the right panel"""
        self.stats_frame = ctk.CTkFrame(self.right_panel)
        self.stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="Statistics",
            font=("Arial", 24, "bold")
        )
        self.stats_label.pack(pady=10)
        
        # Create a grid for stats
        self.stats_grid = ctk.CTkFrame(self.stats_frame)
        self.stats_grid.pack(fill="x", padx=10, pady=5)
        
        # Add all the statistics components
        self.setup_stat_component("Comparisons:", "0", self.stats_grid)
        self.setup_stat_component("Swaps:", "0", self.stats_grid)
        self.setup_stat_component("Time:", "0.000 s", self.stats_grid)
        self.setup_stat_component("Status:", "Ready", self.stats_grid)
        
    def setup_stat_component(self, label_text, initial_value, parent):
        """Helper method to setup a statistics component"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 16, "bold")
        )
        label.pack(side="left", padx=5)
        
        value = ctk.CTkLabel(
            frame,
            text=initial_value,
            font=("Arial", 16)
        )
        value.pack(side="right", padx=5)
        
        # Store reference to the value label
        if label_text == "Comparisons:":
            self.comparisons_value = value
        elif label_text == "Swaps:":
            self.swaps_value = value
        elif label_text == "Time:":
            self.time_value = value
        elif label_text == "Status:":
            self.status_value = value
            
    def setup_info_frame(self):
        """Setup the algorithm information frame in the right panel"""
        self.info_frame = ctk.CTkFrame(self.right_panel)
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="Algorithm Information",
            font=("Arial", 24, "bold")
        )
        self.info_label.pack(pady=10)
        
        # Create a scrollable text widget for algorithm info
        self.algorithm_info = ctk.CTkTextbox(
            self.info_frame,
            font=("Arial", 14),
            wrap="word",
            height=300
        )
        self.algorithm_info.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Update algorithm info
        self.update_algorithm_info()
        
    def use_custom_array(self):
        try:
            custom_array_str = self.custom_array_entry.get().strip()
            if custom_array_str:
                # Parse the input string into a list of integers
                custom_array = [int(x.strip()) for x in custom_array_str.split(",") if x.strip()]
                if custom_array:
                    self.array = custom_array
                    self.array_size.set(len(custom_array))
                    self.size_value_label.configure(text=str(len(custom_array)))
                    self.initial_array = self.array.copy()
                    self.initial_array_value.configure(text=str(self.initial_array))
                    self.final_array_value.configure(text="[]")
                    self.draw_array()
                    self.reset_stats()
                else:
                    self.show_error("Please enter valid numbers separated by commas.")
            else:
                self.show_error("Please enter numbers separated by commas.")
        except ValueError:
            self.show_error("Invalid input. Please enter numbers separated by commas.")
            
    def show_error(self, message):
        """Show an error message in a popup"""
        error_window = ctk.CTkToplevel(self.window)
        error_window.title("Error")
        error_window.geometry("400x150")
        
        # Center the error window
        x = self.window.winfo_x() + (self.window.winfo_width() - 400) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 150) // 2
        error_window.geometry(f"+{x}+{y}")
        
        # Add error message
        label = ctk.CTkLabel(
            error_window,
            text=message,
            font=("Arial", 14),
            wraplength=350
        )
        label.pack(pady=20, padx=20)
        
        # Add close button
        button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        button.pack(pady=10)
        
        # Make window modal
        error_window.transient(self.window)
        error_window.grab_set()
        self.window.wait_window(error_window)
        
    def save_screenshot(self, state_type):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{state_type}_state_{timestamp}.png"
        
        # Create a temporary canvas for the screenshot
        temp_canvas = ctk.CTkCanvas(self.window, bg="#2b2b2b", highlightthickness=0)
        temp_canvas.configure(width=self.canvas.winfo_width(), height=self.canvas.winfo_height())
        
        # Draw the array state
        if state_type == "initial" and self.initial_array:
            array_to_draw = self.initial_array
        elif state_type == "final" and self.final_array:
            array_to_draw = self.final_array
        else:
            array_to_draw = self.array
            
        self.draw_array_on_canvas(temp_canvas, array_to_draw)
        
        # Save the canvas as an image
        temp_canvas.postscript(file=filename + ".eps")
        img = Image.open(filename + ".eps")
        img.save(filename, "png")
        os.remove(filename + ".eps")
        
        # Show success message
        success_label = ctk.CTkLabel(
            self.screenshot_frame,
            text=f"Saved {state_type} state to {filename}",
            text_color="green"
        )
        success_label.pack(side="top", pady=5)
        self.window.after(3000, success_label.destroy)
        
    def draw_array_on_canvas(self, canvas, array):
        canvas.delete("all")
        if not array:
            return
            
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
            canvas_height = 400
            
        bar_width = canvas_width / len(array)
        max_height = max(array)
        
        for i, value in enumerate(array):
            x1 = i * bar_width
            y1 = canvas_height
            x2 = (i + 1) * bar_width - 1
            y2 = canvas_height - (value / max_height) * (canvas_height - 20)
            
            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.colors["normal"],
                outline=""
            )
            
    def generate_random_array(self):
        size = self.array_size.get()
        self.array = [random.randint(1, 100) for _ in range(size)]
        self.initial_array = self.array.copy()
        self.initial_array_value.configure(text=str(self.initial_array))
        self.final_array_value.configure(text="[]")
        self.final_array = None
        self.draw_array()
        self.reset_stats()
        
    def draw_array(self):
        self.canvas.delete("all")
        if not self.array:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
            canvas_height = 400
            
        bar_width = canvas_width / len(self.array)
        max_height = max(self.array)
        
        # Draw color tiles for current state
        tile_height = 25
        tile_y = 10
        tile_width = bar_width * 0.8
        tile_spacing = bar_width * 0.2
        
        # Track current state for the indicator
        current_state = "Normal"
        
        for i, value in enumerate(self.array):
            x1 = i * bar_width
            y1 = canvas_height
            x2 = (i + 1) * bar_width - 1
            y2 = canvas_height - (value / max_height) * (canvas_height - 60)  # More space for numbers
            
            # Determine bar color based on its state
            color = self.colors["normal"]
            if hasattr(self, 'comparing_indices') and i in self.comparing_indices:
                color = self.colors["comparing"]
                current_state = "Comparing"
            elif hasattr(self, 'swapping_indices') and i in self.swapping_indices:
                color = self.colors["swapping"]
                current_state = "Swapping"
            elif hasattr(self, 'sorted_indices') and i in self.sorted_indices:
                color = self.colors["sorted"]
                current_state = "Sorted"
            elif hasattr(self, 'pivot_index') and i == self.pivot_index:
                color = self.colors["pivot"]
                current_state = "Pivot"
            elif hasattr(self, 'min_index') and i == self.min_index:
                color = self.colors["min"]
                current_state = "Minimum"
            
            # Draw the bar with gradient effect
            gradient_steps = 5
            step_height = (y1 - y2) / gradient_steps
            for step in range(gradient_steps):
                step_y1 = y1 - step * step_height
                step_y2 = y1 - (step + 1) * step_height
                # Create a slightly darker gradient
                gradient_color = self.adjust_color(color, 1 - (step * 0.1))
                self.canvas.create_rectangle(
                    x1, step_y1, x2, step_y2,
                    fill=gradient_color,
                    outline=""
                )
            
            # Draw the number on top of the bar with better visibility
            text_x = x1 + bar_width / 2
            text_y = y2 - 20
            self.canvas.create_text(
                text_x, text_y,
                text=str(value),
                fill=self.colors["text"],
                font=("Arial", 11, "bold")
            )
            
            # Draw color tile with border
            tile_x = x1 + (bar_width - tile_width) / 2
            self.canvas.create_rectangle(
                tile_x, tile_y,
                tile_x + tile_width, tile_y + tile_height,
                fill=color,
                outline=self.colors["text"],
                width=1
            )
        
        # Update state indicator
        self.state_indicator.configure(text=f"Current State: {current_state}")
        
    def adjust_color(self, hex_color, factor):
        """Adjust color brightness for gradient effect"""
        # Convert hex to RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        # Adjust brightness
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # Ensure values are within range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def update_visualization(self, arr, stats, state=None):
        self.array = arr.copy()
        self.stats = stats
        
        # Update state information
        if state:
            self.comparing_indices = state.get('comparing', [])
            self.swapping_indices = state.get('swapping', [])
            self.sorted_indices = state.get('sorted', [])
            self.pivot_index = state.get('pivot', None)
            self.min_index = state.get('min', None)
        else:
            # Reset state
            self.comparing_indices = []
            self.swapping_indices = []
            self.sorted_indices = []
            self.pivot_index = None
            self.min_index = None
            
        self.draw_array()
        self.update_stats()
        self.window.update()
        time.sleep(1 / (self.sorting_speed.get() * 0.5 + 1))
        
    def start_sorting(self):
        if self.is_sorting:
            return
            
        self.is_sorting = True
        self.sort_btn.configure(state="disabled")
        self.generate_btn.configure(state="disabled")
        self.use_custom_array_btn.configure(state="disabled")
        self.status_value.configure(text="Sorting...")
        
        # Reset stats
        self.stats = {
            "comparisons": 0,
            "swaps": 0,
            "start_time": time.time(),
            "end_time": None,
            "steps": []
        }
        
        # Reset values
        self.comparisons_value.configure(text="0")
        self.swaps_value.configure(text="0")
        self.time_value.configure(text="0.000 s")
        
        # Start sorting in a separate thread
        thread = threading.Thread(target=self.sort_array)
        thread.start()
        
    def sort_array(self):
        algorithm = self.current_algorithm.get()
        arr = self.array.copy()
        
        # Get the appropriate sorting method
        sort_method = getattr(self.sorting_algorithms, algorithm.lower().replace(" ", "_"))
        
        # Execute the sorting algorithm
        sort_method(arr, self.stats)
        
        self.is_sorting = False
        self.stats["end_time"] = time.time()
        self.final_array = arr.copy()
        self.final_array_value.configure(text=str(self.final_array))
        self.update_stats()
        self.status_value.configure(text="Sorted!")
        self.sort_btn.configure(state="normal")
        self.generate_btn.configure(state="normal")
        self.use_custom_array_btn.configure(state="normal")
        
        # Mark all elements as sorted
        self.sorted_indices = list(range(len(arr)))
        self.draw_array()
        
    def update_stats(self):
        """Update statistics display with better formatting"""
        if not hasattr(self, 'stats'):
            return
            
        self.comparisons_value.configure(text=str(self.stats.get('comparisons', 0)))
        self.swaps_value.configure(text=str(self.stats.get('swaps', 0)))
        
        start_time = self.stats.get('start_time')
        end_time = self.stats.get('end_time')
        if start_time and end_time:
            elapsed_time = end_time - start_time  # Now in seconds
            self.time_value.configure(text=f"{elapsed_time:.3f} s")
        else:
            self.time_value.configure(text="0.000 s")
        
        self.status_value.configure(text="Sorting..." if self.is_sorting else "Ready" if not self.final_array else "Sorted!")
        
    def reset_stats(self):
        """Reset statistics to initial state"""
        self.stats = {
            "comparisons": 0,
            "swaps": 0,
            "start_time": None,
            "end_time": None,
            "steps": []
        }
        self.comparisons_value.configure(text="0")
        self.swaps_value.configure(text="0")
        self.time_value.configure(text="0.000 s")
        self.status_value.configure(text="Ready")
        
    def on_algorithm_change(self, choice):
        """Handle algorithm selection change"""
        self.update_algorithm_info()
        
    def on_size_change(self, value):
        """Handle array size slider change"""
        self.array_size.set(int(value))
        self.size_value_label.configure(text=str(int(value)))
        self.generate_random_array()
        
    def update_algorithm_info(self):
        """Update the algorithm information display with better formatting"""
        algorithm = self.current_algorithm.get()
        info = self.get_algorithm_info(algorithm)
        
        # Clear the text box
        self.algorithm_info.delete("0.0", "end")
        
        # Format the text with newlines and spacing for better readability
        text = f"""
{info['name']}

Description:
{info['description']}

Steps:
{info['steps']}

Time Complexity:
  Best: {info['time']['best']}
  Average: {info['time']['average']}
  Worst: {info['time']['worst']}

Space Complexity:
  {info['space']}

"""
        # Add array information if available
        if self.initial_array:
            text += f"\nInitial Array:\n  {self.initial_array}\n"
        if self.final_array:
            text += f"\nFinal Array:\n  {self.final_array}\n"
            
        # Insert the formatted text
        self.algorithm_info.insert("0.0", text)
        
        # Make text widget read-only
        self.algorithm_info.configure(state="disabled")
        
    def get_algorithm_info(self, algorithm):
        """Get information about the selected sorting algorithm"""
        info = {
            "Bubble Sort": {
                "name": "Bubble Sort",
                "description": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
                "steps": """1. Start from the first element
2. Compare adjacent elements
3. Swap if they are in wrong order
4. Move to next pair
5. Repeat until no swaps needed""",
                "time": {
                    "best": "O(n)",
                    "average": "O(n²)",
                    "worst": "O(n²)"
                },
                "space": "O(1)"
            },
            "Selection Sort": {
                "name": "Selection Sort",
                "description": "Divides the input list into two parts: a sorted sublist and an unsorted sublist.",
                "steps": """1. Find minimum element in unsorted array
2. Swap with first element of unsorted part
3. Move boundary of sorted/unsorted subarrays
4. Repeat until array is sorted""",
                "time": {
                    "best": "O(n²)",
                    "average": "O(n²)",
                    "worst": "O(n²)"
                },
                "space": "O(1)"
            },
            "Insertion Sort": {
                "name": "Insertion Sort",
                "description": "Builds the final sorted array one item at a time.",
                "steps": """1. Start with first element as sorted
2. Take next element
3. Compare with sorted elements
4. Insert at correct position
5. Repeat for all elements""",
                "time": {
                    "best": "O(n)",
                    "average": "O(n²)",
                    "worst": "O(n²)"
                },
                "space": "O(1)"
            },
            "Merge Sort": {
                "name": "Merge Sort",
                "description": "A divide-and-conquer algorithm that divides the input array into two halves.",
                "steps": """1. Divide array into two halves
2. Recursively sort each half
3. Merge sorted halves
4. Compare elements from both halves
5. Place smaller element in result""",
                "time": {
                    "best": "O(n log n)",
                    "average": "O(n log n)",
                    "worst": "O(n log n)"
                },
                "space": "O(n)"
            },
            "Quick Sort": {
                "name": "Quick Sort",
                "description": "A divide-and-conquer algorithm that uses a pivot element.",
                "steps": """1. Choose a pivot element
2. Partition array around pivot
3. Place smaller elements before pivot
4. Place larger elements after pivot
5. Recursively sort subarrays""",
                "time": {
                    "best": "O(n log n)",
                    "average": "O(n log n)",
                    "worst": "O(n²)"
                },
                "space": "O(log n)"
            },
            "Heap Sort": {
                "name": "Heap Sort",
                "description": "Converts the array into a max-heap and extracts elements.",
                "steps": """1. Build max heap from array
2. Swap root with last element
3. Reduce heap size by 1
4. Heapify the root
5. Repeat until heap is empty""",
                "time": {
                    "best": "O(n log n)",
                    "average": "O(n log n)",
                    "worst": "O(n log n)"
                },
                "space": "O(1)"
            },
            "Counting Sort": {
                "name": "Counting Sort",
                "description": "Counts occurrences of each element.",
                "steps": """1. Find maximum element
2. Create count array
3. Store count of each element
4. Modify count array for positions
5. Build output array""",
                "time": {
                    "best": "O(n + k)",
                    "average": "O(n + k)",
                    "worst": "O(n + k)"
                },
                "space": "O(n + k)"
            },
            "Radix Sort": {
                "name": "Radix Sort",
                "description": "Sorts numbers by processing individual digits.",
                "steps": """1. Find maximum number
2. Count digits in maximum
3. Sort by each digit
4. Use counting sort for digits
5. Repeat for all digits""",
                "time": {
                    "best": "O(nk)",
                    "average": "O(nk)",
                    "worst": "O(nk)"
                },
                "space": "O(n + k)"
            },
            "Bucket Sort": {
                "name": "Bucket Sort",
                "description": "Distributes elements into buckets and sorts them.",
                "steps": """1. Create empty buckets
2. Insert elements into buckets
3. Sort individual buckets
4. Concatenate sorted buckets
5. Return sorted array""",
                "time": {
                    "best": "O(n + k)",
                    "average": "O(n + k)",
                    "worst": "O(n²)"
                },
                "space": "O(n + k)"
            }
        }
        return info.get(algorithm, info["Bubble Sort"])
        
    def toggle_step_by_step(self):
        """Toggle step-by-step mode on/off"""
        if self.step_by_step.get():
            # Enable step-by-step features
            self.sorting_speed.set(20)  # Slower speed for better visualization
            if self.is_sorting:
                self.pause_sorting()
        else:
            # Disable step-by-step features
            self.sorting_speed.set(50)  # Reset to default speed
            if self.is_sorting:
                self.resume_sorting()
                
    def pause_sorting(self):
        """Pause the sorting process"""
        if hasattr(self, 'sorting_thread') and self.sorting_thread.is_alive():
            self.is_paused = True
            self.status_value.configure(text="Paused")
            
    def resume_sorting(self):
        """Resume the sorting process"""
        if hasattr(self, 'sorting_thread') and self.sorting_thread.is_alive():
            self.is_paused = False
            self.status_value.configure(text="Sorting...")
            
    def run(self):
        self.window.mainloop()

    def setup_comparison_tab(self):
        """Setup the comparison tab"""
        tab = self.tabview.tab("Comparison")
        
        # Create comparison controls
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Algorithm selection for comparison
        self.alg1_var = ctk.StringVar(value="Bubble Sort")
        self.alg2_var = ctk.StringVar(value="Quick Sort")
        
        # First algorithm selection
        alg1_frame = ctk.CTkFrame(controls_frame)
        alg1_frame.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        
        ctk.CTkLabel(alg1_frame, text="Algorithm 1:", font=("Arial", 14, "bold")).pack(pady=5)
        self.alg1_menu = ctk.CTkOptionMenu(
            alg1_frame,
            values=["Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort", 
                   "Insertion Sort", "Selection Sort"],
            variable=self.alg1_var
        )
        self.alg1_menu.pack(pady=5)
        
        # Second algorithm selection
        alg2_frame = ctk.CTkFrame(controls_frame)
        alg2_frame.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        
        ctk.CTkLabel(alg2_frame, text="Algorithm 2:", font=("Arial", 14, "bold")).pack(pady=5)
        self.alg2_menu = ctk.CTkOptionMenu(
            alg2_frame,
            values=["Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort", 
                   "Insertion Sort", "Selection Sort"],
            variable=self.alg2_var
        )
        self.alg2_menu.pack(pady=5)
        
        # Array size selection
        size_frame = ctk.CTkFrame(controls_frame)
        size_frame.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        
        ctk.CTkLabel(size_frame, text="Test Array Sizes:", font=("Arial", 14, "bold")).pack(pady=5)
        self.size_entry = ctk.CTkEntry(
            size_frame,
            placeholder_text="Enter sizes (e.g., 10,50,100,500)"
        )
        self.size_entry.pack(pady=5)
        self.size_entry.insert("0", "10,50,100,500")
        
        # Start comparison button
        self.compare_btn = ctk.CTkButton(
            controls_frame,
            text="Start Comparison",
            command=self.start_comparison,
            font=("Arial", 14, "bold")
        )
        self.compare_btn.pack(side="left", padx=10, pady=5)
        
        # Comparison results
        results_frame = ctk.CTkFrame(tab)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            results_frame,
            text="Comparison Results",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        self.comparison_results = ctk.CTkTextbox(
            results_frame,
            font=("Arial", 14),
            height=400
        )
        self.comparison_results.pack(fill="both", expand=True, padx=10, pady=5)
        
    def start_comparison(self):
        """Start comparing two sorting algorithms"""
        if self.is_sorting:
            self.show_error("Please wait for current sorting to complete")
            return
            
        # Get selected algorithms
        alg1 = self.alg1_var.get()
        alg2 = self.alg2_var.get()
        
        if alg1 == alg2:
            self.show_error("Please select different algorithms for comparison")
            return
            
        # Get test sizes from entry
        try:
            size_text = self.size_entry.get().strip()
            if not size_text:
                raise ValueError("No sizes provided")
            test_sizes = [int(size.strip()) for size in size_text.split(",")]
            if not test_sizes:
                raise ValueError("No valid sizes provided")
            if any(size <= 0 for size in test_sizes):
                raise ValueError("Array sizes must be positive")
            if any(size > 10000 for size in test_sizes):
                raise ValueError("Array sizes must be less than 10000")
        except ValueError as e:
            self.show_error(str(e))
            return
            
        # Disable comparison button during comparison
        self.compare_btn.configure(state="disabled")
        
        # Update status
        self.comparison_results.delete("0.0", "end")
        self.comparison_results.insert("0.0", "Starting comparison...\n")
        self.comparison_results.insert("end", f"Testing sizes: {', '.join(map(str, test_sizes))}\n")
        self.comparison_results.insert("end", f"Algorithm 1: {alg1}\n")
        self.comparison_results.insert("end", f"Algorithm 2: {alg2}\n")
        self.comparison_results.insert("end", "\nRunning comparison...\n")
        self.window.update()
        
        try:
            # Initialize results
            results = {
                alg1: {"times": [], "comparisons": [], "swaps": []},
                alg2: {"times": [], "comparisons": [], "swaps": []}
            }
            
            # Store original stats
            original_stats = self.stats.copy() if hasattr(self, 'stats') else None
            
            # Run comparison for each size
            total_sizes = len(test_sizes)
            for idx, size in enumerate(test_sizes, 1):
                # Update progress
                self.comparison_results.delete("0.0", "end")
                self.comparison_results.insert("0.0", f"Progress: {idx}/{total_sizes} sizes\n")
                self.comparison_results.insert("end", f"Current size: {size}\n")
                self.comparison_results.insert("end", f"Algorithm 1: {alg1}\n")
                self.comparison_results.insert("end", f"Algorithm 2: {alg2}\n\n")
                self.window.update()
                
                # Generate test array
                test_array = [random.randint(1, 1000) for _ in range(size)]
                
                # Test first algorithm
                self.comparison_results.insert("end", f"Running {alg1}...\n")
                self.window.update()
                
                self.current_algorithm.set(alg1)
                arr1 = test_array.copy()
                stats1 = {
                    "comparisons": 0,
                    "swaps": 0,
                    "start_time": time.time(),
                }
                self.stats = stats1
                
                # Custom callback to track only major steps
                def update_callback1(arr, stats, state=None):
                    if state and ("swapping" in state or "sorted" in state):
                        # Only update UI for swaps or when elements are marked as sorted
                        if "swapping" in state:
                            self.comparison_results.insert("end", f"Swapping indices {state['swapping']}\n")
                        elif "sorted" in state and len(state['sorted']) > 0:
                            self.comparison_results.insert("end", f"Marked {len(state['sorted'])} elements as sorted\n")
                        self.window.update()
                    self.update_visualization(arr, stats, state)
                
                # Temporarily replace update callback
                original_callback = self.sorting_algorithms.update_callback
                self.sorting_algorithms.update_callback = update_callback1
                
                sort_method1 = getattr(self.sorting_algorithms, alg1.lower().replace(" ", "_"))
                sort_method1(arr1, stats1)
                stats1["end_time"] = time.time()
                time1 = stats1["end_time"] - stats1["start_time"]  # Now in seconds
                
                # Restore original callback
                self.sorting_algorithms.update_callback = original_callback
                
                self.comparison_results.insert("end", f"\nCompleted {alg1} in {time1:.3f} s\n")
                self.comparison_results.insert("end", f"Total comparisons: {stats1['comparisons']}\n")
                self.comparison_results.insert("end", f"Total swaps: {stats1['swaps']}\n\n")
                self.window.update()
                
                # Test second algorithm
                self.comparison_results.insert("end", f"Running {alg2}...\n")
                self.window.update()
                
                self.current_algorithm.set(alg2)
                arr2 = test_array.copy()
                stats2 = {
                    "comparisons": 0,
                    "swaps": 0,
                    "start_time": time.time(),
                }
                self.stats = stats2
                
                # Custom callback to track only major steps
                def update_callback2(arr, stats, state=None):
                    if state and ("swapping" in state or "sorted" in state):
                        # Only update UI for swaps or when elements are marked as sorted
                        if "swapping" in state:
                            self.comparison_results.insert("end", f"Swapping indices {state['swapping']}\n")
                        elif "sorted" in state and len(state['sorted']) > 0:
                            self.comparison_results.insert("end", f"Marked {len(state['sorted'])} elements as sorted\n")
                        self.window.update()
                    self.update_visualization(arr, stats, state)
                
                # Temporarily replace update callback
                self.sorting_algorithms.update_callback = update_callback2
                
                sort_method2 = getattr(self.sorting_algorithms, alg2.lower().replace(" ", "_"))
                sort_method2(arr2, stats2)
                stats2["end_time"] = time.time()
                time2 = stats2["end_time"] - stats2["start_time"]  # Now in seconds
                
                # Restore original callback
                self.sorting_algorithms.update_callback = original_callback
                
                self.comparison_results.insert("end", f"\nCompleted {alg2} in {time2:.3f} s\n")
                self.comparison_results.insert("end", f"Total comparisons: {stats2['comparisons']}\n")
                self.comparison_results.insert("end", f"Total swaps: {stats2['swaps']}\n\n")
                self.window.update()
                
                # Store results
                for alg, stats in [(alg1, stats1), (alg2, stats2)]:
                    results[alg]["times"].append(stats["end_time"] - stats["start_time"])
                    results[alg]["comparisons"].append(stats["comparisons"])
                    results[alg]["swaps"].append(stats["swaps"])
                
                # Add a small delay to allow UI updates
                time.sleep(0.1)
            
            # Restore original stats
            self.stats = original_stats if original_stats else {"comparisons": 0, "swaps": 0, "start_time": None, "end_time": None}
            self.update_stats()
            
            # Display results
            self.comparison_results.insert("end", "\nComparison completed!\n")
            self.comparison_results.insert("end", "Generating final results...\n")
            self.window.update()
            self.display_comparison_results(results, test_sizes)
            
        except Exception as e:
            error_msg = f"Error during comparison: {str(e)}"
            self.show_error(error_msg)
            self.comparison_results.delete("0.0", "end")
            self.comparison_results.insert("0.0", f"Comparison failed.\nError: {error_msg}\nPlease try again.")
        finally:
            # Re-enable comparison button
            self.compare_btn.configure(state="normal")
            self.window.update()
            
    def display_comparison_results(self, results, sizes):
        """Display the comparison results with better formatting"""
        text = "Algorithm Comparison Results\n"
        text += "=" * 30 + "\n\n"
        
        for alg, data in results.items():
            text += f"{alg}:\n"
            text += "-" * len(alg) + "\n"
            
            # Calculate averages
            avg_time = sum(data['times']) / len(data['times'])
            avg_comparisons = sum(data['comparisons']) / len(data['comparisons'])
            avg_swaps = sum(data['swaps']) / len(data['swaps'])
            
            text += f"Average Time: {avg_time:.3f} s\n"
            text += f"Average Comparisons: {avg_comparisons:,.0f}\n"
            text += f"Average Swaps: {avg_swaps:,.0f}\n\n"
            
            # Add detailed results for each size
            text += "Detailed Results:\n"
            for i, size in enumerate(sizes):
                text += f"\nArray Size: {size}\n"
                text += f"  Time: {data['times'][i]:.3f} s\n"
                text += f"  Comparisons: {data['comparisons'][i]:,}\n"
                text += f"  Swaps: {data['swaps'][i]:,}\n"
            text += "\n" + "=" * 30 + "\n\n"
        
        # Add comparison summary
        text += "Comparison Summary:\n"
        text += "-" * 20 + "\n"
        
        # Compare times
        alg1, alg2 = list(results.keys())
        time_diff = results[alg1]["times"][-1] - results[alg2]["times"][-1]
        faster = alg2 if time_diff > 0 else alg1
        text += f"Faster Algorithm: {faster}\n"
        text += f"Time Difference: {abs(time_diff):.3f} s\n\n"
        
        # Compare operations
        comp_diff = results[alg1]["comparisons"][-1] - results[alg2]["comparisons"][-1]
        more_efficient = alg2 if comp_diff > 0 else alg1
        text += f"More Efficient (Comparisons): {more_efficient}\n"
        text += f"Comparison Difference: {abs(comp_diff):,}\n"
        
        self.comparison_results.delete("0.0", "end")
        self.comparison_results.insert("0.0", text)

if __name__ == "__main__":
    app = SortingVisualizer()
    app.run() 