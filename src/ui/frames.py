import customtkinter as ctk
from ..data_manager import DataManager
from ..logic import calculate_allocation

from ..config import (
    FONT_FAMILY, 
    FONT_SIZE_SMALL, FONT_SIZE_NORMAL, FONT_SIZE_LARGE, FONT_SIZE_TITLE,
    BASE_FONT_TITLE, BASE_FONT_NORMAL, BASE_FONT_ENTRIES, BASE_FONT_BUTTONS,
    BUTTON_HEIGHT_SMALL, BUTTON_HEIGHT_NORMAL
)
from .custom_window import CustomToplevel

class ResizableFrame(ctk.CTkFrame):
# ... (rest of class unchanged) ...

# ... (DashboardFrame changes) ...

    def show_history_popup(self):
        # Use CustomToplevel
        top = CustomToplevel(self, title="History (Last 10)", w=600, h=400)
        # Geometry is handled roughly by init if w/h passed, or we can override
        top.geometry("600x400")
        
        # Bring to front
        top.attributes("-topmost", True)
        
        # Use content_frame
        textbox = ctk.CTkTextbox(top.content_frame, font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_NORMAL))
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        
        logs = self.data_manager.get_recent_logs(10)
        text = "\n".join(logs) if logs else "履歴はありません"
        
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")

# ...

    def edit_assets_flow(self):
        # 1. Warning Popup
        popup = CustomToplevel(self, title="Confirmation", w=400, h=200)
        
        # Calculate center position relative to main window
        self._center_popup(popup, 400, 200)
        popup.attributes("-topmost", True)
        
        label = ctk.CTkLabel(popup.content_frame, text="資産状況を変更しますか？", font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_LARGE))
        label.pack(expand=True, padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(popup.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        # Yes -> Open Edit Form
        yes_btn = ctk.CTkButton(btn_frame, text="Yes", fg_color="red", width=100, 
                                command=lambda: [popup.destroy(), self.show_edit_form()])
        yes_btn.pack(side="left", padx=20, expand=True)
        
        # No -> Close
        no_btn = ctk.CTkButton(btn_frame, text="No", width=100, command=popup.destroy)
        no_btn.pack(side="right", padx=20, expand=True)

    def show_edit_form(self):
        # 2. Edit Popup
        edit_win = CustomToplevel(self, title="Edit Assets", w=500, h=600)
        edit_win.geometry("500x600")
        edit_win.attributes("-topmost", True)
        
        edit_entries = {}
        assets = [
            ("ソニー銀行 (予備費)", "sony_bank"),
            ("SBI証券 (投資)", "sbi_securities"),
            ("PayPay銀行 (生活費)", "paypay_bank"),
            ("住信SBI (生活防衛)", "sumishin_sbi")
        ]
        
        font_config = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_LARGE)
        
        for i, (label_text, key) in enumerate(assets):
            label = ctk.CTkLabel(edit_win.content_frame, text=label_text, font=font_config)
            label.pack(anchor="w", padx=20, pady=(10, 0))
            
            entry = ctk.CTkEntry(edit_win.content_frame, font=font_config)
            entry.pack(fill="x", padx=20, pady=(0, 10))
            entry.insert(0, str(self.data_manager.get_asset(key)))
            edit_entries[key] = entry
            
        save_btn = ctk.CTkButton(edit_win.content_frame, text="保存", font=font_config, 
                                 command=lambda: self.save_from_popup(edit_entries, edit_win))
        save_btn.pack(pady=(20, 10), padx=20, fill="x")

        # Reset Button (Red)
        reset_btn = ctk.CTkButton(edit_win.content_frame, text="資産状況のリセット", font=font_config, fg_color="#FF5555", hover_color="#DD3333",
                                  command=lambda: self.confirm_reset_step1(edit_win))
        reset_btn.pack(pady=(0, 20), padx=20, fill="x")

    def confirm_reset_step1(self, parent):
        # Confirmation 1
        popup = CustomToplevel(self, title="caution! (1/2)", w=350, h=200)
        self._center_popup(popup, 350, 200)
        popup.attributes("-topmost", True)
        
        label = ctk.CTkLabel(popup.content_frame, text="全ての資産情報を0にリセットしますか？\nこの操作は取り消せません。", 
                             font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_NORMAL), justify="center")
        label.pack(expand=True, padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(popup.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        yes_btn = ctk.CTkButton(btn_frame, text="次へ", fg_color="red", width=100, 
                                command=lambda: [popup.destroy(), self.confirm_reset_step2(parent)])
        yes_btn.pack(side="left", padx=20, expand=True)
        
        no_btn = ctk.CTkButton(btn_frame, text="キャンセル", width=100, command=popup.destroy)
        no_btn.pack(side="right", padx=20, expand=True)

    def confirm_reset_step2(self, parent):
        # Confirmation 2
        popup = CustomToplevel(self, title="final confirmation (2/2)", w=350, h=200)
        self._center_popup(popup, 350, 200)
        popup.attributes("-topmost", True)
        
        label = ctk.CTkLabel(popup.content_frame, text="本当に実行しますか？\n全てのデータが失われます。", 
                             font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_NORMAL, weight="bold"), text_color="red", justify="center")
        label.pack(expand=True, padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(popup.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        yes_btn = ctk.CTkButton(btn_frame, text="実行する", fg_color="red", width=100, 
                                command=lambda: [popup.destroy(), self.execute_reset(parent)])
        yes_btn.pack(side="left", padx=20, expand=True)
        
        no_btn = ctk.CTkButton(btn_frame, text="キャンセル", width=100, command=popup.destroy)
        no_btn.pack(side="right", padx=20, expand=True)

# ...

# SimulatorFrame
    def show_logic_edit_form(self):
        edit_win = CustomToplevel(self, title="Edit Settings", w=400, h=350)
        # Center popup
        master_win = self.winfo_toplevel()
        x = master_win.winfo_x() + (master_win.winfo_width() - 400)//2
        y = master_win.winfo_y() + (master_win.winfo_height() - 300)//2
        edit_win.geometry(f"400x350+{x}+{y}")
        edit_win.attributes("-topmost", True)
        
        settings = self.data_manager.get_settings()
        entries = {}
        
        font_config = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_NORMAL)
        
        fields = [
            ("生活費目標 (PayPay)", "living_target", 100000),
            ("予備費目標 (Sony)", "buffer_target", 500000),
            ("生活防衛資金目安 (SBI)", "life_defense_target", 1500000)
        ]
        
        for label_text, key, default in fields:
            lbl = ctk.CTkLabel(edit_win.content_frame, text=label_text, font=font_config)
            lbl.pack(anchor="w", padx=20, pady=(10, 0))
            
            entry = ctk.CTkEntry(edit_win.content_frame, font=font_config)
            entry.pack(fill="x", padx=20, pady=(0, 10))
            val = settings.get(key, default)
            entry.insert(0, str(val))
            entries[key] = entry
            
        save_btn = ctk.CTkButton(edit_win.content_frame, text="保存", font=font_config, 
                                 command=lambda: self.save_logic_settings(entries, edit_win))
        save_btn.pack(pady=20, padx=20, fill="x")
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.widgets = {
            "title": [],
            "normal": [],
            "mode": [],
            "entries": [],
            "buttons": []
        }
        self.wrappable_widgets = []
        
        # Base font sizes
        self.base_sizes = {
            "title": BASE_FONT_TITLE,
            "normal": BASE_FONT_NORMAL,
            "mode": BASE_FONT_NORMAL,
            "entries": BASE_FONT_ENTRIES,
            "buttons": BASE_FONT_BUTTONS
        }

    def add_widget(self, category, widget, wrap=False):
        if category in self.widgets:
            self.widgets[category].append(widget)
        if wrap:
            self.wrappable_widgets.append(widget)

    def update_appearance(self, scale_factor, width):
        """Updates font size and text wrapping for all registered widgets"""
        
        # Calculate wrap length (Frame width - padding)
        # Deduct: App Padding (20) + Frame Grid Padding (40) + Inner Padding (20) + Scrollbar (20) ~= 100
        # Using 120 for safety margin
        wrap_length = max(100, width - 120)

        for category, widget_list in self.widgets.items():
            new_size = int(self.base_sizes[category] * scale_factor)
            # Base font config for category
            is_category_bold = category in ["title", "mode", "buttons"]
            
            for widget in widget_list:
                # Force bold for Buttons, or if category implies bold
                # Also logic_title (starts with 【) looks better bold, but sticking to logic safe for now
                use_bold = is_category_bold or isinstance(widget, ctk.CTkButton)
                
                font_config = ctk.CTkFont(family=FONT_FAMILY, size=new_size, weight="bold" if use_bold else "normal")
                widget.configure(font=font_config)
                
        # Apply wrapping ONLY to specified widgets
        for widget in self.wrappable_widgets:
             if isinstance(widget, ctk.CTkLabel):
                widget.configure(wraplength=wrap_length)
             # If we decide to wrap other widgets (like buttons?), handled here.

    def _center_popup(self, popup, w, h):
        master = self.winfo_toplevel()
        x = master.winfo_x() + (master.winfo_width() - w) // 2
        y = master.winfo_y() + (master.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

class DashboardFrame(ResizableFrame):
    def __init__(self, master, data_manager: DataManager, **kwargs):
        super().__init__(master, **kwargs)
        self.data_manager = data_manager
        
        self.grid_columnconfigure(1, weight=1, minsize=200)
        
        # Initial Font Config
        title_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["title"], weight="bold")
        normal_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["normal"])
        mode_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["mode"], weight="bold")
        entry_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["entries"])
        button_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold")

        self.label = ctk.CTkLabel(self, text="資産状況", font=title_font)
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.add_widget("title", self.label)

        # Asset Inputs (Now Labels)
        self.amount_labels = {} # Key-based access for logic
        assets = [
            ("ソニー銀行 (予備費)", "sony_bank"),
            ("SBI証券 (投資)", "sbi_securities"),
            ("PayPay銀行 (生活費)", "paypay_bank"),
            ("住信SBI (生活防衛)", "sumishin_sbi")
        ]
        
        # Emphasis font for amounts (Simple bold, no monospace required without yen alignment)
        amount_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["entries"], weight="bold")

        for i, (label_text, key) in enumerate(assets):
            label = ctk.CTkLabel(self, text=label_text, font=normal_font)
            label.grid(row=i+1, column=0, padx=20, pady=10, sticky="w")
            self.add_widget("normal", label)
            
            value = self.data_manager.get_asset(key)
            amount_text = f"{value:,}"
            
            amount_label = ctk.CTkLabel(self, text=amount_text, font=amount_font, anchor="e", justify="right")
            amount_label.grid(row=i+1, column=1, padx=20, pady=10, sticky="ew")
            self.amount_labels[key] = amount_label
            # We add to "entries" category for font resizing compatibility if base_sizes["entries"] is used
            self.add_widget("entries", amount_label)

        # Edit Button (changed from Save)
        self.edit_button = ctk.CTkButton(self, text="資産状況を編集", command=self.edit_assets_flow, font=button_font, height=BUTTON_HEIGHT_NORMAL, anchor="center")
        self.edit_button.grid(row=len(assets)+1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.add_widget("buttons", self.edit_button)
        
        # Mode Display (moved logic later to avoid duplication issue)
        self.mode_label = ctk.CTkLabel(self, text="現在のモード: -", font=mode_font)
        self.mode_label.grid(row=len(assets)+2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.add_widget("mode", self.mode_label)

        # Log Command Block (Last 2 logs)
        self.log_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.log_frame.grid(row=len(assets)+3, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_box = ctk.CTkTextbox(self.log_frame, height=120, font=normal_font, activate_scrollbars=True)
        self.log_box.grid(row=0, column=0, sticky="ew")
        self.log_box.configure(state="disabled", fg_color=("gray90", "gray15")) # Darker background
        self.add_widget("normal", self.log_box)

        # History Button
        self.history_btn = ctk.CTkButton(self.log_frame, text="履歴", width=60, command=self.show_history_popup, font=button_font, height=BUTTON_HEIGHT_NORMAL, anchor="center")
        self.history_btn.grid(row=0, column=1, padx=(10, 0), sticky="e")
        self.add_widget("buttons", self.history_btn)

        self.refresh()

    def result_text_scrolled(self, *args):
        pass

    def edit_assets_flow(self):
        # 1. Warning Popup
        popup = CustomToplevel(self, title="Confirmation")
        
        # Calculate center position relative to main window
        popup_w = 480
        popup_h = 380
        self._center_popup(popup, popup_w, popup_h)
        
        # Attributes handled by CustomToplevel logic (topmost/lift)
        
        label = ctk.CTkLabel(popup.content_frame, text="資産状況を変更しますか？", font=ctk.CTkFont(family=FONT_FAMILY, size=24))
        label.pack(expand=True, padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(popup.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        # Yes -> Open Edit Form
        yes_btn = ctk.CTkButton(btn_frame, text="Yes", fg_color="red", width=100, 
                                command=lambda: [popup.destroy(), self.show_edit_form()],
                                font=ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold"),
                                height=BUTTON_HEIGHT_NORMAL, anchor="center")
        yes_btn.pack(side="left", padx=20, expand=True)
        
        # No -> Close
        no_btn = ctk.CTkButton(btn_frame, text="No", width=100, command=popup.destroy,
                               font=ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold"),
                               height=BUTTON_HEIGHT_NORMAL, anchor="center")
        no_btn.pack(side="right", padx=20, expand=True)

    def show_edit_form(self):
        # 2. Edit Popup
        edit_win = CustomToplevel(self, title="Edit Assets")
        self._center_popup(edit_win, 550, 650)
        # Attributes handled by CustomToplevel
        
        edit_entries = {}
        assets = [
            ("ソニー銀行 (予備費)", "sony_bank"),
            ("SBI証券 (投資)", "sbi_securities"),
            ("PayPay銀行 (生活費)", "paypay_bank"),
            ("住信SBI (生活防衛)", "sumishin_sbi")
        ]
        
        font_config = ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold")
        
        for i, (label_text, key) in enumerate(assets):
            label = ctk.CTkLabel(edit_win.content_frame, text=label_text, font=font_config)
            label.pack(anchor="w", padx=20, pady=(10, 0))
            
            entry = ctk.CTkEntry(edit_win.content_frame, font=font_config)
            entry.pack(fill="x", padx=20, pady=(0, 10))
            # Fix: Force focus on click for Linux
            entry.bind("<Button-1>", lambda event, e=entry: e.focus_force())
            
            entry.insert(0, str(self.data_manager.get_asset(key)))
            edit_entries[key] = entry
            
        save_btn = ctk.CTkButton(edit_win.content_frame, text="保存", font=font_config, 
                                 command=lambda: self.save_from_popup(edit_entries, edit_win),
                                 height=BUTTON_HEIGHT_NORMAL, anchor="center")
        save_btn.pack(pady=(20, 10), padx=20, fill="x")

        # Reset Button (Red)
        reset_btn = ctk.CTkButton(edit_win.content_frame, text="資産状況のリセット", font=font_config, fg_color="#FF5555", hover_color="#DD3333",
                                  command=lambda: self.confirm_reset_step1(edit_win),
                                  height=BUTTON_HEIGHT_NORMAL, anchor="center")
        reset_btn.pack(pady=(0, 20), padx=20, fill="x")

    def confirm_reset_step1(self, parent):
        # Confirmation 1
        popup = CustomToplevel(self, title="caution! (1/2)")
        self._center_popup(popup, 450, 360)
        # Attributes handled by CustomToplevel
        
        label = ctk.CTkLabel(popup.content_frame, text="全ての資産情報を0にリセットしますか？\nこの操作は取り消せません。", 
                             font=ctk.CTkFont(family=FONT_FAMILY, size=20), justify="center")
        label.pack(expand=True, padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(popup.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        yes_btn = ctk.CTkButton(btn_frame, text="次へ", fg_color="red", width=100, 
                                command=lambda: [popup.destroy(), self.confirm_reset_step2(parent)],
                                font=ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold"),
                                height=BUTTON_HEIGHT_NORMAL, anchor="center")
        yes_btn.pack(side="left", padx=20, expand=True)
        
        no_btn = ctk.CTkButton(btn_frame, text="キャンセル", width=100, command=popup.destroy,
                               font=ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold"),
                               height=BUTTON_HEIGHT_NORMAL, anchor="center")
        no_btn.pack(side="right", padx=20, expand=True)

    def confirm_reset_step2(self, parent):
        # Confirmation 2
        popup = CustomToplevel(self, title="final confirmation (2/2)")
        self._center_popup(popup, 450, 360)
        # Attributes handled by CustomToplevel
        
        label = ctk.CTkLabel(popup.content_frame, text="本当に実行しますか？\n全てのデータが失われます。", 
                             font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color="red", justify="center")
        label.pack(expand=True, padx=20, pady=20)
        
        btn_frame = ctk.CTkFrame(popup.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        yes_btn = ctk.CTkButton(btn_frame, text="実行する", fg_color="red", width=100, 
                                command=lambda: [popup.destroy(), self.execute_reset(parent)],
                                font=ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold"),
                                height=BUTTON_HEIGHT_NORMAL, anchor="center")
        yes_btn.pack(side="left", padx=20, expand=True)
        
        no_btn = ctk.CTkButton(btn_frame, text="キャンセル", width=100, command=popup.destroy,
                               font=ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"], weight="bold"),
                               height=BUTTON_HEIGHT_NORMAL, anchor="center")
        no_btn.pack(side="right", padx=20, expand=True)

    def execute_reset(self, parent_window):
        # ... existing code ...
        self.data_manager.reset_assets()
        self.data_manager.add_log("資産状況がリセットされました")
        parent_window.destroy()
        self.refresh()
        
    # _center_popup moved to ResizableFrame

    def save_from_popup(self, entries, window):
        for key, entry in entries.items():
            try:
                value = int(entry.get())
                self.data_manager.update_asset(key, value)
            except ValueError:
                pass 
        
        self.data_manager.add_log("手動で資産状況を更新しました")
        window.destroy()
        self.refresh() # Update dashboard view

    def save_assets(self):
        # Deprecated directly
        pass 

    def update_mode_display(self):
        settings = self.data_manager.get_settings()
        sony_bank = self.data_manager.get_asset("sony_bank")
        paypay_bank = self.data_manager.get_asset("paypay_bank")
        
        # Pass dynamic thresholds AND current living expenses
        result = calculate_allocation(0, sony_bank, current_living_expenses=paypay_bank,
                                   living_target=settings.get("living_target", 100000),
                                   buffer_target=settings.get("buffer_target", 500000))
        self.mode_label.configure(text=f"現在のモード: {result['mode']}")

    def update_log_display(self):
        logs = self.data_manager.get_recent_logs(2)
        if logs:
            # Insert newline after timestamp for dashboard display
            formatted_logs = [log.replace("] ", "]\n", 1) for log in logs]
            text = "\n\n".join(formatted_logs)
        else:
            text = "履歴はありません"
        
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.insert("0.0", text)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def show_history_popup(self):
        top = CustomToplevel(self, title="History (Last 10)")
        self._center_popup(top, 750, 620)
        
        # Attributes handled by CustomToplevel
        
        textbox = ctk.CTkTextbox(top.content_frame, font=ctk.CTkFont(family=FONT_FAMILY, size=20))
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        
        logs = self.data_manager.get_recent_logs(10)
        text = "\n".join(logs) if logs else "履歴はありません"
        
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")

    def refresh(self):
        """Reloads data from DataManager and updates entries"""
        # Get dynamic settings
        settings = self.data_manager.get_settings()
        
        # Define thresholds from settings
        thresholds = {
            "sony_bank": settings.get("buffer_target", 500000),
            "paypay_bank": settings.get("living_target", 100000),
            "sumishin_sbi": settings.get("life_defense_target", 1500000)
        }

        # Colors
        COLOR_OK = "#2CC985" # Light Green (CTK Greenish)
        COLOR_WARN = "#FF5555" # Red
        
        for key, label in self.amount_labels.items():
            value = self.data_manager.get_asset(key)
            label.configure(text=f"{value:,}")
            
            # Determine color
            if key in thresholds:
                if value < thresholds[key]:
                    label.configure(text_color=COLOR_WARN)
                else:
                    label.configure(text_color=COLOR_OK)
            else:
                # No threshold (e.g. Investment), always OK
                label.configure(text_color=COLOR_OK)
                
        self.update_mode_display()
        self.update_log_display()

class SimulatorFrame(ResizableFrame):
    def __init__(self, master, data_manager: DataManager, dashboard_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_manager = data_manager
        self.dashboard_callback = dashboard_callback
        self.current_result = None

        self.grid_columnconfigure(0, weight=1, minsize=300)
        self.grid_rowconfigure(4, weight=1) # Make text area expandable

        # Initial Font Config
        title_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["title"], weight="bold")
        normal_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["normal"])
        entry_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["entries"])
        button_font = ctk.CTkFont(family=FONT_FAMILY, size=self.base_sizes["buttons"])

        self.label = ctk.CTkLabel(self, text="配分シミュレーター", font=title_font)
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.add_widget("title", self.label)

        self.surplus_entry = ctk.CTkEntry(self, placeholder_text="今回の収入額 (ソニー銀行入金)", font=entry_font)
        self.surplus_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.add_widget("entries", self.surplus_entry)

        self.calc_button = ctk.CTkButton(self, text="配分を計算", command=self.calculate, font=button_font, height=BUTTON_HEIGHT_NORMAL, anchor="center")
        self.calc_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.add_widget("buttons", self.calc_button)
        
        # Apply button (Initially hidden)
        self.apply_button = ctk.CTkButton(self, text="結果を反映する (YES)", command=self.apply_allocation, fg_color="green", font=button_font, height=BUTTON_HEIGHT_NORMAL, anchor="center")
        self.add_widget("buttons", self.apply_button)

        self.result_text = ctk.CTkTextbox(self, width=300, height=200, font=normal_font)
        self.result_text.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        self.result_text.configure(state="disabled", fg_color=("gray90", "gray15")) # Read-only style
        self.add_widget("normal", self.result_text)

        # Logic Summary (Label with background frame, no scroll)
        self.widgets["small"] = []
        self.base_sizes["small"] = 18

        # Logic Header (Title + Edit Button)
        self.logic_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logic_header_frame.grid(row=5, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        self.logic_title = ctk.CTkLabel(self.logic_header_frame, text="【ロジック概要】", font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"), anchor="w")
        self.logic_title.pack(side="left")
        self.add_widget("small", self.logic_title)
        
        self.edit_logic_btn = ctk.CTkButton(self.logic_header_frame, text="設定変更", width=80, height=BUTTON_HEIGHT_SMALL, command=self.show_logic_edit_form, font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), anchor="center")
        self.edit_logic_btn.pack(side="right")
        self.add_widget("small", self.edit_logic_btn) 

        # Frame for background color
        self.logic_bg = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        self.logic_bg.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.logic_label = ctk.CTkLabel(self.logic_bg, text="", 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=18),
                                        justify="left", anchor="w")
        self.logic_label.pack(fill="both", padx=10, pady=10)
        
        # Add to widgets for resizing (wrapping handled dynamically by event)
        self.add_widget("small", self.logic_label)
        
        # Bind configure event to update wraplength dynamically
        self.logic_bg.bind("<Configure>", self._update_logic_wrap)
        
        self.update_logic_text()

    def _update_logic_wrap(self, event):
        # Update wraplength to match the frame width minus padding (20px)
        wrap_width = max(100, event.width - 20)
        self.logic_label.configure(wraplength=wrap_width)

    def update_logic_text(self):
        settings = self.data_manager.get_settings()
        living = settings.get("living_target", 100000)
        buffer_val = settings.get("buffer_target", 500000)
        defense = settings.get("life_defense_target", 1500000)
        
        text = (
            f"1. 生活費補填モード (PayPay < {living:,}円)\n"
            f"   → 不足分を最優先で充当\n\n"
            f"2. 予備費補填モード (ソニー < {buffer_val:,}円)\n"
            f"   → 残余の50%を予備費、50%を投資\n\n"
            f"3. 余剰金運用モード (上記以外)\n"
            f"   → 全額を投資用口座へ\n\n"
            f"4. 生活防衛資金目安: {defense:,}円"
        )
        self.logic_label.configure(text=text)
    def calculate(self):
        self.apply_button.grid_forget() # Hide apply button on new calc
        self.current_result = None
        
        settings = self.data_manager.get_settings()
        
        try:
            surplus = int(self.surplus_entry.get())
            current_buffer = self.data_manager.get_asset("sony_bank")
            current_living = self.data_manager.get_asset("paypay_bank")
            
            result = calculate_allocation(surplus, current_buffer, current_living,
                                       living_target=settings.get("living_target", 100000),
                                       buffer_target=settings.get("buffer_target", 500000))
            self.current_result = result
            
            output = f"現在のモード: {result['mode']}\n\n"
            output += f"配分シミュレーション:\n"
            
            if result['living_expenses'] > 0:
                new_living = current_living + result['living_expenses']
                output += f"  PayPay銀行 (生活費): {current_living:,} → {new_living:,} (+{result['living_expenses']:,}) 円\n"
                
            if result['buffer'] > 0:
                new_buffer = current_buffer + result['buffer']
                output += f"  ソニー銀行 (予備費): {current_buffer:,} → {new_buffer:,} (+{result['buffer']:,}) 円\n"
            else:
                pass
            
            new_buffer = current_buffer + result['buffer']
            output += f"  ソニー銀行 (予備費): {current_buffer:,} → {new_buffer:,} (+{result['buffer']:,}) 円\n"
            
            # Investment (SBI)
            current_invest = self.data_manager.get_asset("sbi_securities")
            new_invest = current_invest + result['investment']
            output += f"  投資用口座        : {current_invest:,} → {new_invest:,} (+{result['investment']:,}) 円\n\n"
            
            output += "この結果を資産残高に反映しますか？"
            
            self.result_text.configure(state="normal")
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", output)
            self.result_text.configure(state="disabled")
            
            # Show Apply button
            self.apply_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            
        except ValueError:
            self.result_text.configure(state="normal")
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", "有効な数字を入力してください。")
            self.result_text.configure(state="disabled")

    def show_logic_edit_form(self):
        edit_win = CustomToplevel(self, title="Edit Settings")
        # Center popup
        self._center_popup(edit_win, 500, 450)
        # Attributes handled by CustomToplevel
        
        settings = self.data_manager.get_settings()
        entries = {}
        
        font_config = ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold")
        
        fields = [
            ("生活費目標 (PayPay)", "living_target", 100000),
            ("予備費目標 (Sony)", "buffer_target", 500000),
            ("生活防衛資金目安 (SBI)", "life_defense_target", 1500000)
        ]
        
        for label_text, key, default in fields:
            lbl = ctk.CTkLabel(edit_win.content_frame, text=label_text, font=font_config)
            lbl.pack(anchor="w", padx=20, pady=(10, 0))
            
            entry = ctk.CTkEntry(edit_win.content_frame, font=font_config)
            entry.pack(fill="x", padx=20, pady=(0, 10))
            # Fix: Force focus on click for Linux
            entry.bind("<Button-1>", lambda event, e=entry: e.focus_force())

            val = settings.get(key, default)
            entry.insert(0, str(val))
            entries[key] = entry
            
        save_btn = ctk.CTkButton(edit_win.content_frame, text="保存", font=font_config, 
                                 command=lambda: self.save_logic_settings(entries, edit_win),
                                 height=BUTTON_HEIGHT_NORMAL, anchor="center")
        save_btn.pack(pady=20, padx=20, fill="x")

    def save_logic_settings(self, entries, window):
        new_settings = {}
        for key, entry in entries.items():
            try:
                new_settings[key] = int(entry.get())
            except ValueError:
                pass
        
        self.data_manager.update_settings(new_settings)
        self.update_logic_text()
        if self.dashboard_callback:
            self.dashboard_callback() # Refresh dashboard colors/mode
        window.destroy()

    def apply_allocation(self):
        if not self.current_result:
            return

        # Update Data
        current_sony = self.data_manager.get_asset("sony_bank")
        current_invest = self.data_manager.get_asset("sbi_securities")
        current_paypay = self.data_manager.get_asset("paypay_bank")
        
        new_sony = current_sony + self.current_result['buffer']
        new_invest = current_invest + self.current_result['investment']
        new_paypay = current_paypay + self.current_result['living_expenses']
        
        self.data_manager.update_asset("sony_bank", new_sony)
        self.data_manager.update_asset("sbi_securities", new_invest)
        self.data_manager.update_asset("paypay_bank", new_paypay)
        
        # Add Log
        log_parts = []
        if self.current_result['living_expenses'] > 0:
            log_parts.append(f"生活費 +{self.current_result['living_expenses']:,}円")
        if self.current_result['buffer'] > 0:
            log_parts.append(f"予備費 +{self.current_result['buffer']:,}円")
        if self.current_result['investment'] > 0:
            log_parts.append(f"投資 +{self.current_result['investment']:,}円")
            
        log_msg = "入金反映: " + ", ".join(log_parts)
        self.data_manager.add_log(log_msg)

        # Notify Dashboard
        if self.dashboard_callback:
            self.dashboard_callback()
            
        # Reset UI
        self.result_text.configure(state="normal")
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", "資産状況を更新しました。")
        self.result_text.configure(state="disabled")
        
        self.apply_button.grid_forget()
        self.surplus_entry.delete(0, 'end')
        self.current_result = None
