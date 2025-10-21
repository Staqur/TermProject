#Budget tracker by Mason Riegel

import json
import os
from datetime import datetime
from collections import defaultdict


class Transaction:

    def __init__(self, amount, category, description, date_str):
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date_str

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }


def load_transactions():
    """Load transactions from file and normalize types."""
    try:
        if os.path.exists("budget_data.json"):
            with open("budget_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)

                for t in data.get("income", []):
                    t["amount"] = float(t["amount"])
                for t in data.get("expenses", []):
                    t["amount"] = float(t["amount"])
                return {"income": data.get("income", []), "expenses": data.get("expenses", [])}
        else:
            return {"income": [], "expenses": []}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"income": [], "expenses": []}


def save_transactions(data):
    """Save transactions to file."""
    try:
        with open("budget_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("✓ Data saved.")
    except Exception as e:
        print(f"Error saving data: {e}")


def _now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_income(data):
    """Add income transaction (amount must be positive)."""
    try:
        print("\n--- Add Income ---")
        amount = float(input("Enter amount: $"))
        if amount <= 0:
            print("Amount must be positive.")
            return

        category = input("Enter category (salary, freelance, other): ").strip() or "other"
        description = input("Enter description: ").strip()
        date_str = _now_str()

        transaction = Transaction(amount, category, description, date_str)
        data["income"].append(transaction.to_dict())
        print(f"Income of ${amount:.2f} added.")
    except ValueError:
        print("Invalid amount. Please enter a number.")
    except Exception as e:
        print(f"Error adding income: {e}")


def add_expense(data):
    """Add expense transaction (stored as a positive amount; subtracted later)."""
    try:
        print("\n--- Add Expense ---")
        amount = float(input("Enter amount: $"))
        if amount <= 0:
            print("Amount must be positive.")
            return

        print("Categories: food, rent, utilities, entertainment, transportation, other")
        category = input("Enter category: ").strip() or "other"
        description = input("Enter description: ").strip()
        date_str = _now_str()

        transaction = Transaction(amount, category, description, date_str)
        data["expenses"].append(transaction.to_dict())
        print(f"Expense of ${amount:.2f} added.")
    except ValueError:
        print("Invalid amount. Please enter a number.")
    except Exception as e:
        print(f"Error adding expense: {e}")


def view_summary(data):
    """Display totals, plus a simple monthly rollup."""
    print("\n========== BUDGET SUMMARY ==========")

    total_income = sum(t["amount"] for t in data["income"])
    total_expenses = sum(t["amount"] for t in data["expenses"])
    balance = total_income - total_expenses

    print(f"Total Income:    ${total_income:.2f}")
    print(f"Total Expenses:  ${total_expenses:.2f}")
    print(f"Balance:         ${balance:.2f}")
    print("===================================")

    # Monthly summary (income - expenses) by YYYY-MM
    monthly = defaultdict(float)
    for t in data["income"]:
        month = t["date"][:7]
        monthly[month] += t["amount"]
    for t in data["expenses"]:
        month = t["date"][:7]
        monthly[month] -= t["amount"]

    if monthly:
        print("\nBy month (income - expenses):")
        for m in sorted(monthly):
            print(f"  {m}: ${monthly[m]:.2f}")

    if balance < 0:
        print("\nWARNING: You are spending more than you earn.")
    elif balance > 0:
        print("\nNice—you're net positive this period.")


def view_transactions(data):
    """View all transactions."""
    print("\n--- INCOME ---")
    if not data["income"]:
        print("No income recorded yet.")
    else:
        for i, t in enumerate(data["income"], 1):
            print(f"{i}. ${t['amount']:.2f} - {t['category']}")
            print(f"   {t['description']} ({t['date']})")

    print("\n--- EXPENSES ---")
    if not data["expenses"]:
        print("No expenses recorded yet.")
    else:
        for i, t in enumerate(data["expenses"], 1):
            print(f"{i}. ${t['amount']:.2f} - {t['category']}")
            print(f"   {t['description']} ({t['date']})")


def show_menu():
    """Display main menu."""
    print("\n========== PERSONAL BUDGET TRACKER ==========")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Summary")
    print("4. View All Transactions")
    print("5. Exit")
    print("(tip: expenses are stored positive; I subtract them in the summary)")
    print("============================================")


def main():
    """Run the program."""
    print("Welcome to Personal Budget Tracker!")
    data = load_transactions()

    while True:
        show_menu()
        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice == "1":
                add_income(data)
                save_transactions(data)  # autosave after change
            elif choice == "2":
                add_expense(data)
                save_transactions(data)  # autosave after change
            elif choice == "3":
                view_summary(data)
            elif choice == "4":
                view_transactions(data)
            elif choice == "5":
                print("Saving and exiting...")
                save_transactions(data)
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt:
            print("\nInterrupted. Saving data and exiting...")
            save_transactions(data)
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()