import tkinter as tk
def calculator():
    def update_entry(value):
        current_text = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, current_text + value)

    # Function to evaluate the expression in the entry widget and display the result
    def calculate():
        expression = entry.get()
        try:
            result = eval(expression)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    # Create the main window
    window = tk.Tk()
    window.title("Calculator")

    # Create an entry widget to display the expression and result
    entry = tk.Entry(window, font=('Arial', 20), justify="right")
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Define button labels
    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+'
    ]

    # Create and place the buttons
    row, col = 1, 0
    for button in buttons:
        if button == '=':
            tk.Button(window, text=button, width=10, command=calculate).grid(row=row, column=col, padx=5, pady=5)
        else:
            tk.Button(window, text=button, width=10, command=lambda val=button: update_entry(val)).grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 3:
            col = 0
            row += 1

    # Run the main event loop
    window.mainloop()
