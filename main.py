import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Configurable variables
CSV_FILE = "dream_journal.csv"

box_width = 40
title_height = 1.5
desc_height = 5
combo_width = 10
calendar_width = 20

# Field definitions
fields = [
    ("date", "Dream date"),
    ("dream_title", "Dream title"),
    ("dream_text", "Dream description"),
    ("tags", "Tag (a, b, c)"),
    ("vividness", "Vividness (1-5)"),
    ("lucid", "Lucid dream (0=no, 1=sì)"),
    ("satisfaction", "Sleep satisfaction (1-5)"),
    ("hours", "Hours slept"),
    ("technique", "Technique (WILD, MILD, ecc.)")
]

# Helper functions
def create_text_entry(frame, key, height):
    txt = tk.Text(frame, width=box_width, height=height)
    txt.grid(row=fields.index((key, next(label for k, label in fields if k == key))), column=1)
    return txt

def create_combobox(frame, key, values, width):
    combo = ttk.Combobox(frame, values=values, state="readonly", width=width)
    combo.grid(row=fields.index((key, next(label for k, label in fields if k == key))), column=1, sticky="w")
    return combo

def create_date_entry(frame, key):
    cal = DateEntry(frame, width=calendar_width, date_pattern="yyyy-mm-dd")
    cal.grid(row=fields.index((key, next(label for k, label in fields if k == key))), column=1)
    return cal

def create_standard_entry(frame, key):
    entry = ttk.Entry(frame, width=20)
    entry.grid(row=fields.index((key, next(label for k, label in fields if k == key))), column=1)
    return entry

def save_entry(data):
    file_exists = os.path.exists(CSV_FILE)

    # Ensure all fields are present in the DataFrame
    if file_exists:
        existing_df = pd.read_csv(CSV_FILE)
        for field in fields:
            if field[0] not in existing_df.columns:
                existing_df[field[0]] = None
        existing_df.to_csv(CSV_FILE, index=False)

    df = pd.DataFrame([data])
    df.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)
    messagebox.showinfo("Saved", "Dream saved successfully.")

def read_csv_safe():
    try:
        df = pd.read_csv(CSV_FILE)
        return df
    except pd.errors.ParserError as e:
        messagebox.showerror("Errore", f"CSV file error (incompatible row/column number). Correct manually the file.\n\nDettagli: {e}")
        # Attempt to recover by reading only valid rows
        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()
        valid_lines = [line for line in lines if line.count(',') == lines[0].count(',')]
        with open(CSV_FILE, 'w') as file:
            file.writelines(valid_lines)
        return pd.read_csv(CSV_FILE)

def submit_form():
    data = {}
    for key in entries:
        widget = entries[key]
        if isinstance(widget, tk.Text):
            val = widget.get("1.0", "end").strip()
        else:
            val = widget.get()
        if not val:
            messagebox.showwarning("Error", f"Missing: {key}")
            return
        data[key] = val
    save_entry(data)
    for key in entries:
        widget = entries[key]
        if isinstance(widget, tk.Text):
            widget.delete("1.0", "end")
        elif isinstance(widget, ttk.Combobox):
            widget.set("")
        else:
            widget.delete(0, tk.END)

def show_entries():
    df = read_csv_safe()
    if df.empty:
        messagebox.showwarning("Error", "No dreams found.")
        return

    top = tk.Toplevel(root)
    top.title("📜 Logged Dreams")

    filter_frame = ttk.Frame(top, padding=10)
    filter_frame.pack()

    ttk.Label(filter_frame, text="Filter by tags:").grid(row=0, column=0, sticky="w")
    tag_filter = ttk.Entry(filter_frame, width=30)
    tag_filter.grid(row=0, column=1, sticky="w")

    ttk.Label(filter_frame, text="Search by content or title:").grid(row=1, column=0, sticky="w")
    search_filter = ttk.Entry(filter_frame, width=30)
    search_filter.grid(row=1, column=1, sticky="w")

    ttk.Label(filter_frame, text="Sort by:").grid(row=2, column=0, sticky="w")
    sort_filter = ttk.Combobox(filter_frame, values=["Date (newest)", "Date (oldest)", "Vividness", "Satisfaction"], state="readonly", width=30)
    sort_filter.grid(row=2, column=1, sticky="w")

    def apply_filters():
        filtered_df = df.copy()

        # Filter by tag
        tags = tag_filter.get().strip()
        if tags:
            filtered_df = filtered_df[filtered_df["tags"].str.contains('|'.join(tags.split(",")), na=False, case=False)]

        # Search by content or title
        search_query = search_filter.get().strip()
        if search_query:
            filtered_df = filtered_df[filtered_df["dream_text"].str.contains(search_query, na=False, case=False) |
                                       filtered_df["dream_title"].str.contains(search_query, na=False, case=False)]

        # Sort by selected filter
        sort_option = sort_filter.get()
        if sort_option == "Date (newest)":
            filtered_df = filtered_df.sort_values(by="date", ascending=False)
        elif sort_option == "Date (oldest)":
            filtered_df = filtered_df.sort_values(by="date", ascending=True)
        elif sort_option == "Vividness":
            filtered_df = filtered_df.sort_values(by="vividness", ascending=False)
        elif sort_option == "Satisfaction":
            filtered_df = filtered_df.sort_values(by="satisfaction", ascending=False)

        # Display filtered dreams
        text.delete("1.0", "end")
        for _, row in filtered_df.iterrows():
            text.insert("end", f"🗓️ {row['date']}\n")
            text.insert("end", f"Lucid: {row['lucid']} | Vividness: {row['vividness']} | Hours: {row['hours']} | Satisfaction: {row['satisfaction']} | Technique: {row['technique']}\n")
            text.insert("end", f"Tags: {row['tags']}\n")
            text.insert("end", f"✏️ {row['dream_text']}\n")
            text.insert("end", "-"*80 + "\n")

    ttk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=3, column=0, columnspan=2, pady=10)

    text = tk.Text(top, wrap="word", width=100, height=30)
    text.pack(padx=10, pady=10)

    apply_filters()

def show_graphs_filtered():
    df = read_csv_safe()
    if df.empty:
        return

    try:
        df["date"] = pd.to_datetime(df["date"])
    except:
        messagebox.showerror("Error", "Date format invalid.")
        return

    start = start_date.get_date()
    end = end_date.get_date()
    filtered = df[(df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))]

    if filtered.empty:
        messagebox.showinfo("No data", "No dreams in this range.")
        return

    for col in ["vividness", "lucid", "satisfaction", "hours"]:
        filtered[col] = pd.to_numeric(filtered[col], errors='coerce')

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    filtered["vividness"].dropna().astype(int).plot(kind=graph_type.get())
    plt.title("Vividness")

    plt.subplot(2, 2, 2)
    filtered["lucid"].dropna().astype(int).value_counts().plot(kind="bar")
    plt.title("Lucid dreams")

    plt.subplot(2, 2, 3)
    filtered["satisfaction"].dropna().astype(int).plot(kind=graph_type.get())
    plt.title("Sleep satisfaction")

    plt.subplot(2, 2, 4)
    filtered["hours"].dropna().astype(float).plot(kind=graph_type.get())
    plt.title("Hours slept")

    plt.tight_layout()
    plt.show()

# GUI
root = tk.Tk()
root.title("🌙 Dream Journal")
frame = ttk.Frame(root, padding=10)
frame.grid()

entries = {}

# Interfaccia campi
for key, label in fields:
    ttk.Label(frame, text=label).grid(row=fields.index((key, label)), column=0, sticky="w", pady=3)
    if key == "date":
        entries[key] = create_date_entry(frame, key)
    elif key == "dream_title":
        entries[key] = create_text_entry(frame, key, title_height)
    elif key == "dream_text":
        entries[key] = create_text_entry(frame, key, desc_height)
    elif key in ["vividness", "satisfaction"]:
        entries[key] = create_combobox(frame, key, [1, 2, 3, 4, 5], combo_width)
    elif key == "lucid":
        entries[key] = create_combobox(frame, key, [0, 1], combo_width)
    elif key == "technique":
        entries[key] = create_combobox(frame, key, ["", "WILD", "MILD", "SSILD", "DEILD", "other"], 15)
    elif key == "tags":
        entries[key] = create_standard_entry(frame, key)
    else:
        entries[key] = create_standard_entry(frame, key)

# Pulsanti
ttk.Button(frame, text="💾 Save", command=submit_form).grid(row=len(fields), column=0, pady=10)
ttk.Button(frame, text="📊 Graphs", command=show_graphs_filtered).grid(row=len(fields), column=1, sticky="w")
ttk.Button(frame, text="📖 Read dreams", command=show_entries).grid(row=len(fields)+1, column=0, pady=5)

# Filtri data per grafici
ttk.Label(frame, text="From date:").grid(row=len(fields)+2, column=0, sticky="e")
start_date = DateEntry(frame, width=calendar_width, date_pattern="yyyy-mm-dd")
start_date.grid(row=len(fields)+2, column=1, sticky="w")

ttk.Label(frame, text="To date:").grid(row=len(fields)+3, column=0, sticky="e")
end_date = DateEntry(frame, width=calendar_width, date_pattern="yyyy-mm-dd")
end_date.grid(row=len(fields)+3, column=1, sticky="w")

# GUI additions for graph type
graph_type = tk.StringVar(value="line")
ttk.Label(frame, text="Graph type:").grid(row=len(fields)+4, column=0, sticky="e")
graph_type_combo = ttk.Combobox(frame, textvariable=graph_type, values=["line", "bar", "hist"], state="readonly", width=10)
graph_type_combo.grid(row=len(fields)+4, column=1, sticky="w")

root.mainloop()
