import customtkinter as ctk
from .frames import DashboardFrame, SimulatorFrame
from ..data_manager import DataManager
from .custom_window import CustomWindowMixin

class App(ctk.CTk, CustomWindowMixin):
    def __init__(self):
        super().__init__()

        self.geometry("1200x900")
        self.minsize(960, 720)
        
        # Custom Title Bar Setup
        self.setup_custom_title_bar("Nontaro Asset Manager", resizeable=True)

        # Initialize data
        self.data_manager = DataManager()
        
        # Main Container for Content (to separate from Title Bar)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(side="top", fill="both", expand=True)

        # Layout configuration for container
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Frames (Parent is main_container now)
        self.dashboard_frame = DashboardFrame(self.main_container, self.data_manager)
        self.dashboard_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.simulator_frame = SimulatorFrame(self.main_container, self.data_manager, dashboard_callback=self.dashboard_frame.refresh)
        self.simulator_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Bind resize event
        # Note: Binds to self (Window), so still triggered on window resize
        self.bind("<Configure>", self.on_resize)
        self.last_width = 800
        self._resize_after_id = None
        
        self.bring_resize_grip_to_front()

    def on_resize(self, event):
        # Check if it's the main window resizing
        if event.widget == self:
            # Cancel previous scheduled update
            if self._resize_after_id:
                self.after_cancel(self._resize_after_id)
            
            # Schedule new update after 100ms
            self._resize_after_id = self.after(100, lambda: self._delayed_resize_update(event.width))

    def _delayed_resize_update(self, width):
        new_width = width
        # Reference width is now 1200 (default size)
        # Scaling: 1.0 at 1200px
        scale_factor = new_width / 1200.0
        scale_factor = max(0.6, min(scale_factor, 1.5)) # Clamp between 0.6x and 1.5x
        
        # Assuming equal split for frames, approx width is half
        frame_width = new_width // 2
        try:
            self.dashboard_frame.update_appearance(scale_factor, frame_width)
            self.simulator_frame.update_appearance(scale_factor, frame_width)
        except Exception:
            pass
        self._resize_after_id = None

    def run(self):
        self.mainloop()
