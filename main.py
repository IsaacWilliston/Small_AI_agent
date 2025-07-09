import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import sys
import os
import threading
import time
from ai_agent import get_answer


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Custom AI Assistant")

        # Enable high DPI awareness
        self.setup_high_dpi()

        # Calculate scale factor for better resolution
        self.scale_factor = self.get_scale_factor()

        # Set window size based on scale factor - larger for high-DPI
        base_width, base_height = 1400, 1000
        self.root.geometry(f"{int(base_width * self.scale_factor)}x{int(base_height * self.scale_factor)}")
        self.root.minsize(int(500 * self.scale_factor), int(400 * self.scale_factor))

        self.is_dark = True
        self.is_processing = False  # Add processing state
        self.conversation_history = []  # Store conversation history

        # Improved color scheme with better contrast
        self.colors = {
            True: {
                "bg": "#1a1a1a",
                "fg": "#f0f0f0",
                "input_bg": "#2d2d2d",
                "button": "#404040",
                "button_hover": "#4a4a4a",
                "button_disabled": "#2a2a2a",
                "accent": "#00d4aa",
                "accent_hover": "#00b890",
                "accent_disabled": "#006b5a",
                "border": "#404040",
                "user_msg": "#e6f3ff",
                "assistant_msg": "#f0f0f0",
                "error_msg": "#ff6b6b",
            },
            False: {
                "bg": "#ffffff",
                "fg": "#1a1a1a",
                "input_bg": "#f8f9fa",
                "button": "#e9ecef",
                "button_hover": "#dee2e6",
                "button_disabled": "#f8f9fa",
                "accent": "#0066cc",
                "accent_hover": "#0052a3",
                "accent_disabled": "#99c2ff",
                "border": "#d1d5db",
                "user_msg": "#0066cc",
                "assistant_msg": "#1a1a1a",
                "error_msg": "#dc3545",
            }
        }

        self.create_widgets()
        self.configure_theme()

        # Bind resize event to maintain proper scaling
        self.root.bind('<Configure>', self.on_window_resize)

        # Set focus to input field
        self.entry.focus_set()

    def setup_high_dpi(self):
        """Enable high DPI awareness for Windows"""
        try:
            if sys.platform == "win32":
                import ctypes
                # Tell Windows this is a high DPI aware application
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    def get_scale_factor(self):
        """Calculate appropriate scale factor based on screen DPI"""
        try:
            # Get screen DPI
            dpi = self.root.winfo_fpixels('1i')
            # Standard DPI is 96, calculate scale factor
            scale = max(1.0, dpi / 96.0)

            # For high-DPI displays like yours (2880x1800), we need more aggressive scaling
            # Your display likely has ~200 DPI, so we want around 2x scaling
            if scale < 1.5:
                scale = 1.5  # Minimum scale for readability

            return min(scale, 3.0)  # Allow up to 3x scaling for very high DPI
        except:
            # Fallback for high-DPI displays
            return 1.8

    def get_scaled_font(self, family, size, weight="normal"):
        """Return font with proper scaling - increased base sizes for high-DPI"""
        # Increase base font sizes for better readability on high-DPI displays
        size_multiplier = 1.2  # 20% larger base fonts
        scaled_size = int(size * size_multiplier * self.scale_factor)
        return (family, scaled_size, weight)

    def increase_scale(self):
        """Increase UI scale factor"""
        self.scale_factor = min(self.scale_factor + 0.1, 3.0)
        self.update_scaling()

    def decrease_scale(self):
        """Decrease UI scale factor"""
        self.scale_factor = max(self.scale_factor - 0.1, 0.8)
        self.update_scaling()

    def update_scaling(self):
        """Update all UI elements with new scale factor"""
        # Update fonts for all widgets
        self.title_label.config(font=self.get_scaled_font("Segoe UI", 16, "bold"))
        self.toggle_btn.config(font=self.get_scaled_font("Segoe UI", 9))
        self.scale_down_btn.config(font=self.get_scaled_font("Segoe UI", 10, "bold"))
        self.scale_up_btn.config(font=self.get_scaled_font("Segoe UI", 10, "bold"))
        self.scale_label.config(font=self.get_scaled_font("Segoe UI", 9))
        self.chat_box.config(font=self.get_scaled_font("Segoe UI", 11))
        self.entry.config(font=self.get_scaled_font("Segoe UI", 11))
        self.send_btn.config(font=self.get_scaled_font("Segoe UI", 10, "bold"))
        self.clear_btn.config(font=self.get_scaled_font("Segoe UI", 10, "bold"))
        self.status_label.config(font=self.get_scaled_font("Segoe UI", 9))

        # Update padding and spacing
        self.main_frame.pack_configure(padx=int(20 * self.scale_factor), pady=int(20 * self.scale_factor))
        self.chat_box.config(
            padx=int(20 * self.scale_factor),
            pady=int(15 * self.scale_factor),
            spacing1=int(5 * self.scale_factor),
            spacing2=int(3 * self.scale_factor),
            spacing3=int(10 * self.scale_factor)
        )
        self.entry.config(
            padx=int(15 * self.scale_factor),
            pady=int(10 * self.scale_factor)
        )
        self.send_btn.config(
            padx=int(20 * self.scale_factor),
            pady=int(10 * self.scale_factor)
        )
        self.clear_btn.config(
            padx=int(15 * self.scale_factor),
            pady=int(8 * self.scale_factor)
        )
        self.toggle_btn.config(
            padx=int(15 * self.scale_factor),
            pady=int(8 * self.scale_factor)
        )

        # Reconfigure theme to update text tags
        self.configure_theme()

    def create_widgets(self):
        # Main container with increased padding for high-DPI
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=int(20 * self.scale_factor),
                             pady=int(20 * self.scale_factor))

        # Title bar
        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=(0, int(10 * self.scale_factor)))

        self.title_label = tk.Label(
            self.title_frame,
            text="🤖 AI Assistant",
            font=self.get_scaled_font("Segoe UI", 16, "bold"),
            anchor="w"
        )
        self.title_label.pack(side=tk.LEFT)

        # Right side button frame
        self.right_buttons_frame = tk.Frame(self.title_frame)
        self.right_buttons_frame.pack(side=tk.RIGHT)

        # Clear conversation button
        self.clear_btn = tk.Button(
            self.right_buttons_frame,
            text="🗑️ Clear",
            command=self.clear_conversation,
            font=self.get_scaled_font("Segoe UI", 9),
            relief=tk.FLAT,
            padx=int(15 * self.scale_factor),
            pady=int(8 * self.scale_factor),
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=(int(10 * self.scale_factor), 0))

        self.toggle_btn = tk.Button(
            self.right_buttons_frame,
            text="🌞 Light Mode",
            command=self.toggle_theme,
            font=self.get_scaled_font("Segoe UI", 9),
            relief=tk.FLAT,
            padx=int(15 * self.scale_factor),
            pady=int(8 * self.scale_factor),
            cursor="hand2"
        )
        self.toggle_btn.pack(side=tk.RIGHT, padx=(int(10 * self.scale_factor), 0))

        # Scale adjustment buttons
        self.scale_frame = tk.Frame(self.right_buttons_frame)
        self.scale_frame.pack(side=tk.RIGHT, padx=(int(10 * self.scale_factor), int(10 * self.scale_factor)))

        tk.Label(self.scale_frame, text="Scale:", font=self.get_scaled_font("Segoe UI", 9)).pack(side=tk.LEFT)

        self.scale_down_btn = tk.Button(
            self.scale_frame,
            text="−",
            command=self.decrease_scale,
            font=self.get_scaled_font("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            width=2,
            cursor="hand2"
        )
        self.scale_down_btn.pack(side=tk.LEFT, padx=(int(5 * self.scale_factor), 0))

        self.scale_label = tk.Label(
            self.scale_frame,
            text=f"{self.scale_factor:.1f}x",
            font=self.get_scaled_font("Segoe UI", 9),
            width=4
        )
        self.scale_label.pack(side=tk.LEFT, padx=int(2 * self.scale_factor))

        self.scale_up_btn = tk.Button(
            self.scale_frame,
            text="+",
            command=self.increase_scale,
            font=self.get_scaled_font("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            width=2,
            cursor="hand2"
        )
        self.scale_up_btn.pack(side=tk.LEFT)

        # Chat container with border
        self.chat_container = tk.Frame(self.main_frame, relief=tk.SOLID, bd=1)
        self.chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, int(10 * self.scale_factor)))

        # Chat box with improved styling
        self.chat_box = scrolledtext.ScrolledText(
            self.chat_container,
            wrap=tk.WORD,
            font=self.get_scaled_font("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=0,
            padx=int(20 * self.scale_factor),
            pady=int(15 * self.scale_factor),
            spacing1=int(5 * self.scale_factor),  # Space above paragraphs
            spacing2=int(3 * self.scale_factor),  # Space between lines
            spacing3=int(2 * self.scale_factor)  # Space below paragraphs
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True)
        self.chat_box.config(state=tk.DISABLED)

        # Input section with improved layout
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X)

        # Input container with border
        self.input_container = tk.Frame(self.input_frame, relief=tk.SOLID, bd=1)
        self.input_container.pack(fill=tk.X, pady=(0, int(10 * self.scale_factor)))

        # Input field
        self.entry = tk.Text(
            self.input_container,
            font=self.get_scaled_font("Segoe UI", 10),
            relief=tk.FLAT,
            highlightthickness=0,
            bd=0,
            height=2,
            padx=int(15 * self.scale_factor),
            pady=int(10 * self.scale_factor),
            wrap=tk.WORD
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Shift-Return>", self.insert_newline)
        self.entry.bind("<Control-a>", self.select_all)

        # Send button with improved styling
        self.send_btn = tk.Button(
            self.input_container,
            text="Send ➤",
            command=self.on_enter,
            font=self.get_scaled_font("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=int(20 * self.scale_factor),
            pady=int(10 * self.scale_factor),
            cursor="hand2"
        )
        self.send_btn.pack(side=tk.RIGHT, fill=tk.Y)

        # Status bar
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X)

        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=self.get_scaled_font("Segoe UI", 9),
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT)

        # Message counter
        self.message_counter = tk.Label(
            self.status_frame,
            text="Messages: 0",
            font=self.get_scaled_font("Segoe UI", 9),
            anchor="e"
        )
        self.message_counter.pack(side=tk.RIGHT)

        # Add welcome message
        self.display_welcome()

    def display_welcome(self):
        """Display a welcome message"""
        welcome_msg = "Hello! I'm your AI assistant. How can I help you today?"
        self.display_chat("Assistant", welcome_msg, role="assistant")

    def configure_theme(self):
        """Apply theme colors with improved styling"""
        theme = self.colors[self.is_dark]

        # Update toggle button text
        self.toggle_btn.config(text="🌞 Light Mode" if self.is_dark else "🌙 Dark Mode")

        # Main window and frames
        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])
        self.title_frame.configure(bg=theme["bg"])
        self.right_buttons_frame.configure(bg=theme["bg"])
        self.input_frame.configure(bg=theme["bg"])
        self.input_container.configure(bg=theme["input_bg"], highlightbackground=theme["border"])
        self.chat_container.configure(bg=theme["border"], highlightbackground=theme["border"])
        self.status_frame.configure(bg=theme["bg"])

        # Labels
        self.title_label.configure(bg=theme["bg"], fg=theme["accent"])
        self.status_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.message_counter.configure(bg=theme["bg"], fg=theme["fg"])

        # Chat box
        self.chat_box.configure(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"],
            selectbackground=theme["accent"],
            selectforeground=theme["bg"]
        )

        # Input field
        self.entry.configure(
            bg=theme["input_bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"],
            selectbackground=theme["accent"],
            selectforeground=theme["bg"]
        )

        # Send button - update based on processing state
        send_bg = theme["accent_disabled"] if self.is_processing else theme["accent"]
        send_hover = theme["accent_disabled"] if self.is_processing else theme["accent_hover"]

        self.send_btn.configure(
            bg=send_bg,
            fg=theme["bg"],
            activebackground=send_hover,
            activeforeground=theme["bg"],
            state=tk.DISABLED if self.is_processing else tk.NORMAL
        )

        # Other buttons
        self.toggle_btn.configure(
            bg=theme["button"],
            fg=theme["fg"],
            activebackground=theme["button_hover"],
            activeforeground=theme["fg"]
        )

        self.clear_btn.configure(
            bg=theme["button"],
            fg=theme["fg"],
            activebackground=theme["button_hover"],
            activeforeground=theme["fg"]
        )

        # Configure text tags for better message display
        self.chat_box.tag_configure("user",
                                    foreground=theme["user_msg"],
                                    font=self.get_scaled_font("Segoe UI", 11, "bold"),
                                    lmargin1=int(20 * self.scale_factor),
                                    lmargin2=int(40 * self.scale_factor))

        self.chat_box.tag_configure("assistant",
                                    foreground=theme["assistant_msg"],
                                    font=self.get_scaled_font("Segoe UI", 11),
                                    lmargin1=int(20 * self.scale_factor),
                                    lmargin2=int(40 * self.scale_factor))

        self.chat_box.tag_configure("error",
                                    foreground=theme["error_msg"],
                                    font=self.get_scaled_font("Segoe UI", 11),
                                    lmargin1=int(20 * self.scale_factor),
                                    lmargin2=int(40 * self.scale_factor))

        self.chat_box.tag_configure("timestamp",
                                    foreground=theme["fg"],
                                    font=self.get_scaled_font("Segoe UI", 9),
                                    lmargin1=int(20 * self.scale_factor))

        # Scale adjustment buttons
        self.scale_frame.configure(bg=theme["bg"])
        self.scale_down_btn.configure(
            bg=theme["button"],
            fg=theme["fg"],
            activebackground=theme["button_hover"],
            activeforeground=theme["fg"]
        )
        self.scale_up_btn.configure(
            bg=theme["button"],
            fg=theme["fg"],
            activebackground=theme["button_hover"],
            activeforeground=theme["fg"]
        )
        self.scale_label.configure(bg=theme["bg"], fg=theme["fg"])

        # Update scale label
        self.scale_label.config(text=f"{self.scale_factor:.1f}x")

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark = not self.is_dark
        self.configure_theme()

    def clear_conversation(self):
        """Clear the conversation history"""
        result = messagebox.askyesno("Clear Conversation",
                                     "Are you sure you want to clear the conversation history?")
        if result:
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.delete(1.0, tk.END)
            self.chat_box.config(state=tk.DISABLED)
            self.conversation_history.clear()
            self.update_message_counter()
            self.display_welcome()

    def select_all(self, event=None):
        """Select all text in the input field"""
        self.entry.tag_add(tk.SEL, "1.0", tk.END)
        return "break"

    def on_enter(self, event=None):
        """Handle send button click or Enter key press"""
        if self.is_processing:
            return "break"

        user_input = self.entry.get("1.0", tk.END).strip()
        if not user_input:
            return "break"

        self.entry.delete("1.0", tk.END)
        self.display_chat("You", user_input, role="user")
        self.conversation_history.append({"role": "user", "content": user_input})
        self.update_message_counter()

        # Show thinking indicator

        # Process response in a separate thread to avoid blocking UI
        threading.Thread(target=self.process_response, args=(user_input,), daemon=True).start()

        return "break"

    def insert_newline(self, event=None):
        """Insert newline on Shift+Enter"""
        return None  # Allow default behavior


    def process_response(self, user_input):
        """Process AI response in a separate thread"""
        try:
            response = get_answer(user_input)
            # Update UI in main thread
            self.root.after(0, self.display_response, response)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, self.display_response, error_msg, True)

    def display_response(self, response, is_error=False):
        """Display AI response (called from main thread)"""

        role = "error" if is_error else "assistant"
        self.display_chat("Assistant", response, role=role, show_timestamp=False)

        if not is_error:
            self.conversation_history.append({"role": "assistant", "content": response})
            self.update_message_counter()

        self.is_processing = False
        self.configure_theme()  # Update button state
        self.status_label.config(text="Ready")
        self.entry.focus_set()  # Return focus to input

    def update_message_counter(self):
        """Update message counter display"""
        count = len([msg for msg in self.conversation_history if msg["role"] == "user"])
        self.message_counter.config(text=f"Messages: {count}")

    def display_chat(self, speaker, message, role="assistant", show_timestamp=True):
        """Display chat message with improved formatting"""
        self.chat_box.config(state=tk.NORMAL)

        if show_timestamp:
            # Add timestamp and speaker
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M")
            self.chat_box.insert(tk.END, f"[{timestamp}] {speaker}:\n", "timestamp")

        # Insert message
        self.chat_box.insert(tk.END, f"{message.strip()}\n\n", role)

        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

        # Auto-scroll to bottom
        self.root.after(1, lambda: self.chat_box.see(tk.END))

    def on_window_resize(self, event=None):
        """Handle window resize events"""
        if event and event.widget == self.root:
            # Maintain proper scaling on resize
            pass

    def on_closing(self):
        """Handle application closing"""
        if self.is_processing:
            result = messagebox.askyesno("Exit",
                                         "AI is still processing. Are you sure you want to exit?")
            if not result:
                return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)

    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()