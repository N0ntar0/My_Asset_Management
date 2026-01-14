import customtkinter as ctk

class CustomWindowMixin:
    def setup_custom_title_bar(self, title, resizeable=False, container=None, 
                               title_bg_color="#2b2b2b", title_text_color="white", close_btn_color="white"):
        # Reverted to Standard Window to fix critical input focus issues on Linux
        self.title(title)
        
        # No custom title bar, no overrideredirect
        self.title_bar = None
        self.title_label = None

    def close_window(self):
        self.destroy()

    def start_move(self, event):
        pass

    def do_move(self, event):
        pass

    def start_resize(self, event):
        pass

    def do_resize(self, event, mode="wh"):
        pass

    def bring_resize_grip_to_front(self):
        pass

class CustomToplevel(ctk.CTkToplevel, CustomWindowMixin):
    def __init__(self, master=None, title="Window", w=400, h=300, resizeable=False, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title(title)
        
        # Center Window initially (Approximate)
        if master:
            try:
                mx = master.winfo_x()
                my = master.winfo_y()
                mw = master.winfo_width()
                mh = master.winfo_height()
                x = mx + (mw - w) // 2
                y = my + (mh - h) // 2
                self.geometry(f"{w}x{h}+{x}+{y}")
            except Exception:
                self.geometry(f"{w}x{h}")
        else:
            self.geometry(f"{w}x{h}")

        # Standard Transiency (Keep on top of master)
        self.transient(master)
        
        # Compatibility Content Frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.content_frame.pack(side="top", fill="both", expand=True)
        
        # Ensure input focus (Standard behavior)
        self.after(100, lambda: self.focus_force())

    def _enforce_focus(self):
        pass
