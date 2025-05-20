import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

def minify_html(html):
    # Avoid touching content inside <script> and <style>
    def preserve_blocks(match):
        tag = match.group(1)
        content = match.group(2)
        return f"<{tag}>{content}</{tag}>"

    # Extract and preserve script/style contents
    scripts = re.findall(r'<(script|style)(.*?)>(.*?)</\1>', html, flags=re.DOTALL)
    placeholders = []
    for i, (tag, attrs, content) in enumerate(scripts):
        placeholder = f"___PLACEHOLDER_{i}___"
        full_block = f"<{tag}{attrs}>{content}</{tag}>"
        html = html.replace(full_block, placeholder)
        placeholders.append((placeholder, full_block))

    # Now minify remaining HTML
    html = html.replace('\n', '').replace('\r', '').replace('\t', '')
    html = re.sub(r'>\s+<', '><', html)  # space between tags
    html = re.sub(r'\s{2,}', ' ', html)  # multiple spaces

    # Restore script/style blocks
    for placeholder, original in placeholders:
        html = html.replace(placeholder, original)

    return html.strip()

def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html;*.htm")])
    if not filepath:
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            original_html = file.read()

        minified_html = minify_html(original_html)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html;*.htm")],
            initialfile=f"minified_{os.path.basename(filepath)}"
        )
        if not save_path:
            return

        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(minified_html)

        messagebox.showinfo("Success", f"Minified HTML saved to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file:\n{str(e)}")

# Tkinter UI
root = tk.Tk()
root.title("HTML Minifier")

frame = tk.Frame(root, padx=80, pady=40)
frame.pack()
button = tk.Button(frame, text="Select HTML File", command=select_file, font=('Arial', 12))
button.pack()

root.mainloop()
