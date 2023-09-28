import tkinter as tk
from tkinter import simpledialog, messagebox

# class representing a bank account of a person
class CardHolder:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction = []  # List to store transaction history

    # Method to record a new transaction in the account history
    def record_transaction(self, description):
        self.transaction.append(description)

# Class for the displaying the transaction history
class Transaction_History:
    @staticmethod
    def display_history(CardHolder):
        transact = "\n".join(CardHolder.transaction)
        messagebox.showinfo("Transaction History", f"Transactions:\n{transact}")

# Class to handle withdrawal
class Withdraw:
    @staticmethod
    def withdraw(CardHolder, amount):
        if (CardHolder.balance >= amount):
            CardHolder.balance = CardHolder.balance - amount
            CardHolder.record_transaction(f"Withdrew ${amount}")
            messagebox.showinfo("Success", f"${amount} has been withdrawn!")
        else:
            messagebox.showerror("Error!", "Not Enough Balance!")

# Class to handle deposit 
class Deposit:
    @staticmethod
    def deposit(CardHolder, amount):
        CardHolder.balance = CardHolder.balance + amount
        CardHolder.record_transaction(f"Deposited ${amount}")
        messagebox.showinfo("Success", f"${amount} has been deposited.")

# Class to handle funds transfer 
class Transfer:
    @staticmethod
    def transfer(sender_account, receiver_account, amount):
        if sender_account.balance >= amount:
            sender_account.balance = sender_account.balance + amount
            sender_account.balance = sender_account.balance + amount
            sender_account.record_transaction(f"Transferred ${amount} to {receiver_account.user_id}")
            receiver_account.record_transaction(f"Received ${amount} from {sender_account.user_id}")
            messagebox.showinfo("Success", f"Transferred ${amount} to {receiver_account.user_id}")
        else:
            messagebox.showerror("Error", "Insufficient funds")

# Main Tkinter GUI class
class ATMApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM")
        self.master.geometry("400x400")

        # Configure rows and columns for layout
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Initialize some demo accounts
        self.accounts = {
            "S": CardHolder("S", "0602", 5000),
            "M": CardHolder("M", "2204", 5000)
        }

        self.create_login_window()

    # Method to create login window

    def create_login_window(self):
        title = tk.Label(self.master, text="ATM", font=("Helvetica", 16))
        title.grid(row=0, columnspan=2, pady=20)

        tk.Label(self.master, text="User ID").grid(row=1, column=0, padx=20, pady=10)
        tk.Label(self.master, text="PIN").grid(row=2, column=0, padx=20, pady=10)

        self.e1 = tk.Entry(self.master)
        self.e2 = tk.Entry(self.master, show="*")

        self.e1.grid(row=1, column=1, padx=20, pady=10)
        self.e2.grid(row=2, column=1, padx=20, pady=10)

        tk.Button(self.master, text="Quit", command=self.master.destroy).grid(row=4, columnspan=2, pady=5)

        tk.Button(self.master, text="Login", command=self.login).grid(row=3, columnspan=2, pady=5)

    def login(self):
        user_id = self.e1.get()
        pin = self.e2.get()

        if user_id in self.accounts and self.accounts[user_id].pin == pin:
            self.current_account = self.accounts[user_id]
            messagebox.showinfo("Success!")
            self.show_options()
        else:
            messagebox.showerror("Error", "Invalid User ID or PIN")

    def show_options(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title = tk.Label(self.master, text="ATM", font=("Helvetica", 16))
        title.grid(row=0, columnspan=2, pady=20)

        tk.Button(self.master, text="Transactions History", command=lambda: Transaction_History.display_history(self.current_account)).grid(row=1, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Withdraw", command=self.withdraw_gui).grid(row=2, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Deposit", command=self.deposit_gui).grid(row=3, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Transfer", command=self.transfer_gui).grid(row=4, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Quit", command=self.master.destroy).grid(row=5, columnspan=2, padx=20, pady=5)

    def withdraw_gui(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            Withdraw.withdraw(self.current_account, amount)

    def deposit_gui(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            Deposit.deposit(self.current_account, amount)

    def transfer_gui(self):
        transfer_id = simpledialog.askstring("Transfer", "Enter User ID to transfer to:")
        if transfer_id in self.accounts:
            amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
            if amount is not None:
                Transfer.transfer(self.current_account, self.accounts[transfer_id], amount)
        else:
            messagebox.showerror("Error", "Invalid User ID")

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()