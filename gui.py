import tkinter as tk
import subprocess
import os

def run_script(file_name):
    try:
        output_text.delete(1.0, tk.END)  # Clear previous output
        result = subprocess.run(
            ['python', file_name],
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            errors="replace"
        )
        output_text.insert(tk.END, result.stdout)
        output_text.tag_add("output", "1.0", tk.END)
    except subprocess.CalledProcessError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error:\n{e.stderr}")
        output_text.tag_add("output", "1.0", tk.END)

# Tkinter setup
root = tk.Tk()
root.title("Run Python Script")
root.geometry("500x400")
root.configure(bg="black")

# Buttons to run different scripts
run_button1 = tk.Button(root, text="Train the Data", command=lambda: run_script("vulnerability.py"), bg="black", fg="white", font=("Helvetica", 14))
run_button1.pack(pady=10)

run_button2 = tk.Button(root, text="Scan for Vulnerability", command=lambda: run_script("scanner.py"), bg="black", fg="white", font=("Helvetica", 14))
run_button2.pack(pady=10)

# Text widget for output display (without scrollbar)
output_text = tk.Text(root, wrap=tk.WORD, width=60, height=20, bg="black", fg="green", insertbackground="white", font=("Helvetica", 14))
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
output_text.tag_configure("output", foreground="green")

root.mainloop()
