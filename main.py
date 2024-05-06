import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import browser

if __name__ == "__main__":
    entries = []

    # Search For History Database Paths
    history_files = browser.get_browsers()
    
    print(history_files)