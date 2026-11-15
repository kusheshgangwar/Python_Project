import tkinter as tk
from tkinter import ttk, messagebox

transactions = []


def add_transaction():
    transaction_type = type_var.get().lower()
    category = category_entry.get().strip()
    amount_text = amount_entry.get().strip()

    if not category:
        messagebox.showerror("Error", "Please enter a category.")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    if transaction_type not in ["income", "expense"]:
        messagebox.showerror("Error", "Invalid transaction type.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Amount must be greater than zero.")
        return

    transactions.append({
        "type": transaction_type,
        "category": category,
        "amount": amount
    })

    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    status_var.set("Transaction added successfully!")
    view_transactions()


def view_transactions():
    if not transactions:
        display_text("No transactions found.")
        return

    lines = [
        f"{i}. {item['type'].title()} | {item['category']} | ₹{item['amount']:.2f}"
        for i, item in enumerate(transactions, start=1)
    ]
    display_text("\n".join(lines))


def show_summary():
    income = sum(item["amount"] for item in transactions if item["type"] == "income")
    expenses = sum(item["amount"] for item in transactions if item["type"] == "expense")
    balance = income - expenses

    summary = [
        "----- FINANCIAL SUMMARY -----",
        f"Total Income: ₹{income:.2f}",
        f"Total Expenses: ₹{expenses:.2f}",
        f"Remaining Balance: ₹{balance:.2f}"
    ]
    display_text("\n".join(summary))
    status_var.set("Summary generated.")


def search_category():
    query = search_entry.get().strip().lower()
    if not query:
        messagebox.showerror("Error", "Please enter a category to search.")
        return

    matches = []
    for i, item in enumerate(transactions, start=1):
        if item["category"].lower() == query:
            matches.append(
                f"{i}. {item['type'].title()} | {item['category']} | ₹{item['amount']:.2f}"
            )

    if not matches:
        display_text("No transactions found in this category.")
        status_var.set("No matching category transactions found.")
        return

    display_text("\n".join(matches))
    status_var.set(f"Found {len(matches)} matching transaction(s).")


def delete_transaction():
    try:
        number = int(delete_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid transaction number.")
        return

    if not (1 <= number <= len(transactions)):
        messagebox.showerror("Error", "Invalid transaction number.")
        return

    removed = transactions.pop(number - 1)
    delete_entry.delete(0, tk.END)
    status_var.set(f"Deleted: {removed['type'].title()} | {removed['category']} | ₹{removed['amount']:.2f}")
    view_transactions()


def display_text(message):
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, message)
    output_box.config(state=tk.DISABLED)


def clear_output():
    display_text("")
    status_var.set("Output cleared.")


root = tk.Tk()
root.title("Expense Management System")
root.geometry("750x650")
root.minsize(700, 500)

main_frame = ttk.Frame(root, padding=15)
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = ttk.LabelFrame(main_frame, text="Add Transaction", padding=10)
input_frame.pack(fill=tk.X, pady=(0, 10))

row1 = ttk.Frame(input_frame)
row1.pack(fill=tk.X, pady=4)

ttk.Label(row1, text="Type:", width=12).pack(side=tk.LEFT)
type_var = tk.StringVar(value="expense")
type_combo = ttk.Combobox(row1, textvariable=type_var, values=["income", "expense"], state="readonly", width=15)
type_combo.pack(side=tk.LEFT, padx=(0, 10))

row2 = ttk.Frame(input_frame)
row2.pack(fill=tk.X, pady=4)

ttk.Label(row2, text="Category:", width=12).pack(side=tk.LEFT)
category_entry = ttk.Entry(row2, width=25)
category_entry.pack(side=tk.LEFT, padx=(0, 10))

ttk.Label(row2, text="Amount:", width=10).pack(side=tk.LEFT)
amount_entry = ttk.Entry(row2, width=18)
amount_entry.pack(side=tk.LEFT)

button_frame = ttk.Frame(input_frame)
button_frame.pack(fill=tk.X, pady=(8, 0))

add_button = ttk.Button(button_frame, text="Add", command=add_transaction)
add_button.pack(side=tk.LEFT, padx=(0, 8))
view_button = ttk.Button(button_frame, text="View", command=view_transactions)
view_button.pack(side=tk.LEFT, padx=(0, 8))
summary_button = ttk.Button(button_frame, text="Summary", command=show_summary)
summary_button.pack(side=tk.LEFT, padx=(0, 8))

search_frame = ttk.LabelFrame(main_frame, text="Search / Delete", padding=10)
search_frame.pack(fill=tk.X, pady=(0, 10))

search_row = ttk.Frame(search_frame)
search_row.pack(fill=tk.X, pady=4)

ttk.Label(search_row, text="Search Category:", width=16).pack(side=tk.LEFT)
search_entry = ttk.Entry(search_row, width=25)
search_entry.pack(side=tk.LEFT, padx=(0, 10))
search_button = ttk.Button(search_row, text="Search", command=search_category)
search_button.pack(side=tk.LEFT)

delete_row = ttk.Frame(search_frame)
delete_row.pack(fill=tk.X, pady=4)

ttk.Label(delete_row, text="Delete No.:", width=16).pack(side=tk.LEFT)
delete_entry = ttk.Entry(delete_row, width=10)
delete_entry.pack(side=tk.LEFT, padx=(0, 10))
delete_button = ttk.Button(delete_row, text="Delete", command=delete_transaction)
delete_button.pack(side=tk.LEFT)
clear_button = ttk.Button(delete_row, text="Clear Output", command=clear_output)
clear_button.pack(side=tk.LEFT, padx=(10, 0))

output_frame = ttk.LabelFrame(main_frame, text="Transactions", padding=(10, 8))
output_frame.pack(fill=tk.BOTH, expand=True)

output_box = tk.Text(output_frame, height=18, wrap=tk.WORD, state=tk.DISABLED)
output_box.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_box.config(yscrollcommand=scrollbar.set)

status_var = tk.StringVar(value="Ready")
status_bar = ttk.Label(main_frame, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W, padding=(8, 4))
status_bar.pack(fill=tk.X, pady=(8, 0))

view_transactions()
root.mainloop()
