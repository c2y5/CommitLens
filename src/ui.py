# src/ui.py

import os
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.cache import delete_cache
class ChartViewer:
    def __init__(self, figures, chart_dir="charts", repo_type=None, identifier=None):
        self.repo_type = repo_type
        self.identifier = identifier
        self.figures = figures
        self.chart_dir = chart_dir
        self.index = 0

        self.root = tk.Tk()
        self.root.title("Git Commit Visualiser - Charts")

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

        self.canvas = None
        self.display_chart()

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        tk.Button(self.btn_frame, text="Previous", command=self.prev_chart).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Next", command=self.next_chart).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Save Charts", command=self.save_charts).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Delete Cache", command=self.delete_cache).pack(side=tk.LEFT, padx=5)

        self.root.mainloop()

    def display_chart(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        fig = self.figures[self.index]

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.root.title(f"Viewing Chart {self.index + 1} of {len(self.figures)}")

    def next_chart(self):
        self.index = (self.index + 1) % len(self.figures)
        self.display_chart()

    def prev_chart(self):
        self.index = (self.index - 1) % len(self.figures)
        self.display_chart()

    def save_charts(self):
        os.makedirs(self.chart_dir, exist_ok=True)
        for i, fig in enumerate(self.figures, 1):
            filename = f"chart_{i}.png"
            path = os.path.join(self.chart_dir, filename)
            fig.savefig(path)
        messagebox.showinfo("Saved", f"All charts saved to ./{self.chart_dir}")

    def delete_cache(self):
        if self.repo_type and self.identifier:
            deleted = delete_cache(self.repo_type, self.identifier)
            if deleted:
                messagebox.showinfo("Cache", "Cache for this repo deleted.")
            else:
                messagebox.showwarning("Cache", "No cache found for this repo.")
        else:
            messagebox.showwarning("Cache", "Repo info not provided, cannot delete cache.")
