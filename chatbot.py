

import tkinter as tk
from tkinter import Menu, messagebox
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import base64
import io
import json
import threading
from textwrap import wrap


try:
    from PIL import Image, ImageTk
    PILLOW_INSTALLED = True
except ImportError:
    PILLOW_INSTALLED = False

# --- 1. NLTK Data Check ---
# Ensures that the necessary NLTK models are downloaded.
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet.zip/wordnet/index.sense')
except LookupError:
    # A friendly error message if data is missing.
    tk.Tk().withdraw() # Hide the root window
    messagebox.showerror("NLTK Data Missing",
                         "A required NLTK dataset is missing.\n"
                         "Please run `import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')` in a Python shell to fix this.")
    exit()

# --- 2. Enhanced NLP Engine ---
# This class handles all the natural language processing tasks.
class EnhancedNLPEngine:
    def __init__(self, faq_data):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.faq_data = faq_data
        self.conversation_history = []
        self._train()

    def _train(self):
        """Pre-processes the FAQ data and trains the TF-IDF vectorizer."""
        self.questions = [item["question"] for item in self.faq_data]
        self.answers = [item["answer"] for item in self.faq_data]
        processed_faqs = [self._preprocess_text(q) for q in self.questions]
        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(processed_faqs)

    def _preprocess_text(self, text):
        """Tokenizes, lemmatizes, and removes stop words from text."""
        tokens = nltk.word_tokenize(text.lower())
        lemmatized_tokens = [self.lemmatizer.lemmatize(w) for w in tokens if w.isalnum() and w not in self.stop_words]
        return " ".join(lemmatized_tokens)

    def get_most_similar_answer(self, user_question):
        """Finds the most relevant answer from the FAQ data."""
        context = " ".join(self.conversation_history[-2:])
        full_question = context + " " + user_question
        processed_user_question = self._preprocess_text(full_question)
        user_vector = self.vectorizer.transform([processed_user_question])
        similarities = cosine_similarity(user_vector, self.faq_vectors)
        most_similar_index = similarities.argmax()
        self.conversation_history.append(user_question)

        if similarities[0, most_similar_index] > 0.15:
            return self.answers[most_similar_index]
        else:
            return self.get_fallback_response()

    def get_fallback_response(self):
        """Provides a default response when no good answer is found."""
        return "I'm sorry, I don't have a specific answer for that. Could you please try rephrasing your question?"

    def clear_history(self):
        """Clears the conversation history."""
        self.conversation_history = []


# --- 3. The Professional Chat Application Class ---
# This class builds and manages the entire graphical user interface.
class ChatApplication(tk.Tk):
    def __init__(self, nlp_engine):
        super().__init__()
        if not PILLOW_INSTALLED:
            messagebox.showerror("Pillow Library Missing", "The 'Pillow' library is recommended. Please install it using: pip install Pillow")
        
        self.nlp_engine = nlp_engine
        self.title("Intelligent FAQ Assistant")
        self.geometry("500x700")
        self.minsize(450, 600)

        # --- UI Theme and Asset Configuration ---
        self.BG_COLOR = "#ededed"
        self.USER_BUBBLE_COLOR = "#dcf8c6"
        self.BOT_BUBBLE_COLOR = "#ffffff"
        self.TEXT_COLOR = "#1f1f1f"
        self.HEADER_COLOR = "#005e54"
        self.FONT = ("Segoe UI", 11)
        self.FONT_SMALL = ("Segoe UI", 8)
        self.typing_indicator = None

        # --- List to track all message labels for responsive resizing ---
        self.message_labels = []

        self._setup_ui()

    def _setup_ui(self):
        """ the main UI elements of the application."""
        # --- Header ---
        header_frame = tk.Frame(self, bg=self.HEADER_COLOR, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="Intelligent FAQ Assistant", font=("Segoe UI", 14, "bold"), bg=self.HEADER_COLOR, fg="white")
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        clear_button = tk.Button(header_frame, text="Clear", font=("Segoe UI", 10), command=self.clear_chat, relief=tk.FLAT, bg=self.HEADER_COLOR, fg="white", activebackground="#007a6e", activeforeground="white", bd=0, cursor="hand2")
        clear_button.pack(side=tk.RIGHT, padx=15)

        # --- Chat Area with Scrolling ---
        chat_container = tk.Frame(self, bg=self.BG_COLOR)
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(chat_container, bg=self.BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG_COLOR)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Bind the resize event of the canvas to a handler function ---
        self.canvas.bind('<Configure>', self._on_resize)

        # --- Message Input Footer ---
        footer_frame = tk.Frame(self, bg="#f0f0f0", height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5, padx=10)
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)

        self.user_entry = tk.Text(footer_frame, height=1, bg="white", fg=self.TEXT_COLOR, font=self.FONT,
                                  padx=15, pady=10, relief=tk.SOLID, insertbackground=self.TEXT_COLOR, bd=1, highlightthickness=0)
        self.user_entry.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=10)
        self.user_entry.bind("<Return>", self._on_enter_pressed)
        self.user_entry.bind("<KeyRelease>", self._on_text_change)

        self.send_button = tk.Button(footer_frame, text="Send", bg=self.HEADER_COLOR, fg="white",
                                     activebackground="#007a6e", activeforeground="white", 
                                     font=("Segoe UI", 10, "bold"), command=self.send_message_thread,
                                     borderwidth=0, relief=tk.FLAT, cursor="hand2", padx=10)
        self.send_button.grid(row=0, column=1, pady=10, sticky="ns")

        # Add initial greeting message after a short delay.
        self.after(200, lambda: self._add_message_to_gui("Bot", "Hello! I'm your intelligent FAQ assistant. How can I help you today?"))

    def _on_resize(self, event):
        """Dynamically adjusts the wraplength of all messages on window resize."""
        # Calculate the new max width for message bubbles based on the canvas width
        max_width = event.width - 40
        
        if max_width < 100:
            max_width = 100
        
        # Update all existing message labels
        for label in self.message_labels:
            if label.winfo_exists():
                label.config(wraplength=max_width)

    def _on_enter_pressed(self, event):
        """Handles the Enter key press to send a message."""
        self.send_message_thread()
        return "break"

    def _on_text_change(self, event):
        """Auto-adjusts the height of the text entry box based on content."""
        num_lines = self.user_entry.count("1.0", "end-1c", "displaylines") or 1
        self.user_entry.config(height=min(num_lines, 4))

    def send_message_thread(self):
        """Initiates message processing in a separate thread to keep the UI responsive."""
        user_input = self.user_entry.get("1.0", tk.END).strip()
        if user_input:
            self._add_message_to_gui("You", user_input)
            self.user_entry.delete("1.0", tk.END)
            self.user_entry.config(state=tk.DISABLED)
            
            threading.Thread(target=self.process_bot_response, args=(user_input,), daemon=True).start()

    def process_bot_response(self, user_input):
        """Handles the logic of getting and displaying the bot's response."""
        self.after(100, self.show_typing_indicator)
        
        bot_response = self.nlp_engine.get_most_similar_answer(user_input)
        
        self.after(500, self.remove_typing_indicator)
        self.after(600, self._add_message_to_gui, "Bot", bot_response, True)
        self.after(600, lambda: self.user_entry.config(state=tk.NORMAL))

    def _add_message_to_gui(self, sender, message, show_feedback=False):
        """Creates and adds a chat bubble widget to the scrollable frame."""
        is_user = sender == "You"
        bubble_color = self.USER_BUBBLE_COLOR if is_user else self.BOT_BUBBLE_COLOR
        anchor = "e" if is_user else "w"
        
        bubble_frame = tk.Frame(self.scrollable_frame, bg=self.BG_COLOR)
        
        max_width = self.canvas.winfo_width() - 40
        if max_width < 100:
            max_width = 300
            
        wrapped_message = "\n".join(wrap(message, width=60))
        
        msg_label = tk.Label(bubble_frame, text=wrapped_message, font=self.FONT, bg=bubble_color, 
                             fg=self.TEXT_COLOR, justify="left", wraplength=max_width,
                             padx=10, pady=5, relief="solid", borderwidth=0)
        
        # --- FIX: Add the new label to our tracking list ---
        self.message_labels.append(msg_label)
        
        timestamp = datetime.now().strftime('%H:%M')
        time_label = tk.Label(bubble_frame, text=timestamp, font=self.FONT_SMALL, bg=self.BG_COLOR, fg="#888")
        
        if is_user:
            msg_label.pack(side=tk.TOP, anchor="e", pady=(0, 2))
            time_label.pack(side=tk.TOP, anchor="e", padx=(0,5))
        else:
            msg_label.pack(side=tk.TOP, anchor="w", pady=(0, 2))
            time_label.pack(side=tk.TOP, anchor="w", padx=(5,0))

        bubble_frame.pack(fill="x", padx=10, pady=5, anchor=anchor)

        if show_feedback:
            self.add_feedback_buttons(bubble_frame, anchor)
        
        self.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def add_feedback_buttons(self, parent_frame, anchor):
        """Adds thumbs up/down buttons below a bot message."""
        feedback_frame = tk.Frame(parent_frame, bg=self.BG_COLOR)
        
        like_button = tk.Button(feedback_frame, text="👍", font=self.FONT, command=lambda: self.log_feedback("positive", feedback_frame), relief=tk.FLAT, bg=self.BG_COLOR, activebackground=self.BG_COLOR, bd=0, cursor="hand2")
        like_button.pack(side=tk.LEFT, padx=0)

        dislike_button = tk.Button(feedback_frame, text="👎", font=self.FONT, command=lambda: self.log_feedback("negative", feedback_frame), relief=tk.FLAT, bg=self.BG_COLOR, activebackground=self.BG_COLOR, bd=0, cursor="hand2")
        dislike_button.pack(side=tk.LEFT)
        
        feedback_frame.pack(anchor=anchor, pady=(0, 5))

    def log_feedback(self, feedback_type, frame_to_replace):
        """Logs user feedback and updates the UI."""
        last_question = self.nlp_engine.conversation_history[-1] if self.nlp_engine.conversation_history else "N/A"
        feedback_log = {"timestamp": datetime.now().isoformat(), "question": last_question, "feedback": feedback_type}
        try:
            with open("feedback_log.json", "a") as f:
                f.write(json.dumps(feedback_log) + "\n")
        except IOError as e:
            print(f"Error writing to feedback log: {e}")
        
        for widget in frame_to_replace.winfo_children():
            widget.destroy()
        feedback_confirm_label = tk.Label(frame_to_replace, text="Thanks for your feedback!", font=self.FONT_SMALL, bg=self.BG_COLOR, fg="#888")
        feedback_confirm_label.pack()

    def show_typing_indicator(self):
        """Displays a 'Bot is typing...' bubble."""
        if self.typing_indicator: return
        self.typing_indicator = tk.Frame(self.scrollable_frame, bg=self.BG_COLOR)
        typing_label = tk.Label(self.typing_indicator, text="Bot is typing...", font=("Segoe UI", 11, "italic"), bg=self.BOT_BUBBLE_COLOR, 
                                fg=self.TEXT_COLOR, padx=10, pady=5, relief="solid", borderwidth=0)
        typing_label.pack(anchor="w")
        self.typing_indicator.pack(fill="x", padx=10, pady=5, anchor="w")
        self.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def remove_typing_indicator(self):
        """Removes the typing indicator bubble."""
        if self.typing_indicator:
            self.typing_indicator.destroy()
            self.typing_indicator = None

    def clear_chat(self):
        """Clears the chat window and conversation history."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the entire chat history?"):
            self.nlp_engine.clear_history()
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # ---  Clear the tracked labels list ---
            self.message_labels.clear()

            self.after(100, lambda: self._add_message_to_gui("Bot", "Chat cleared! How can I help you now?"))

if __name__ == "__main__":
    # The knowledge base for the chatbot.
    faq_data = [
        {"question": "What are your shipping options?", "answer": "We offer standard (3-5 business days), expedited (2 business days), and next-day shipping."},
        {"question": "How can I track my order?", "answer": "Once your order has shipped, you will receive an email with a tracking number and a link to the carrier's website."},
        {"question": "What is your return policy?", "answer": "We accept returns on all unused items within 30 days of purchase for a full refund. Please visit our returns page to start the process."},
        {"question": "How do I contact customer support?", "answer": "You can contact our support team via email at support@example.com or by calling us at 1-800-123-4567 during business hours."},
        {"question": "Do you ship internationally?", "answer": "Yes, we ship to most countries worldwide. International shipping rates and times vary by destination."},
        {"question": "What payment methods do you accept?", "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay."},
        {"question": "How do I change my shipping address?", "answer": "If your order has not yet shipped, you can change the shipping address from your account page. If it has already shipped, please contact the carrier directly."},
        {"question": "My order arrived damaged, what should I do?", "answer": "We're sorry to hear that. Please contact customer support with your order number and a photo of the damaged item, and we will arrange for a replacement or refund."},
        {"question": "How long does a refund take?", "answer": "Once we receive your returned item, refunds are typically processed within 3-5 business days to your original payment method."},
        {"question": "Can I cancel my order?", "answer": "You can cancel your order within one hour of placing it. Go to your order history and select the 'Cancel Order' option. After that, the order cannot be canceled."},
        {"question": "How do I reset my password?", "answer": "On the login page, click the 'Forgot Password' link. Enter your email address, and we will send you instructions to reset it."},
        {"question": "Do you have a physical store?", "answer": "Currently, we are an online-only retailer and do not have any physical store locations."},
        {"question": "What is the warranty on your products?", "answer": "Our products come with a one-year limited warranty that covers manufacturing defects. It does not cover accidental damage."},
        {"question": "Are there any discounts for new customers?", "answer": "Yes! New customers can use the code NEW15 at checkout to get 15% off their first order."},
        {"question": "How do I use a promo code?", "answer": "You can enter your promo code in the designated field on the checkout page before completing your payment."},
        {"question": "Is my personal information secure?", "answer": "Absolutely. We use industry-standard SSL encryption to protect your details. Your payment information is never stored on our servers."}
    ]
    
    # Initialize the NLP engine and run the application.
    nlp_engine = EnhancedNLPEngine(faq_data)
    app = ChatApplication(nlp_engine)
    app.mainloop()
