Budget Tracker

By Mason Riegel

Description

This is a simple Python program that helps users track their income and expenses. The goal of this project is to give users an easy way to record money coming in and money going out, and to show a quick summary of their financial balance. It can be used by anyone who wants a basic budgeting tool without needing spreadsheets or complicated apps.

The program runs in the command line and saves all data to a file named budget_data.json. That way, you don’t lose your transactions when you close the program. Each time you add new income or expenses, the program automatically saves your data.

Features:
Add your personal income with its own category, description, and it timestamps the data
Add expenses with its category, description, and a timestamp as well.
.json file to retain data after closing program
Display total income, expenses and balance
Shows breakdown of net income
Warns you when you are spending more than you are earning

How it Works:
When the program starts, it loads up the budget_data.json file to recall data, if it doesnt exist the program will generate it.
When you run the python application, in the command line you will be prompted with options 1-5.
1.) Add Income
2.) Add Expense
3.) View Summary
4.) View All Transactions
5.) Exit
