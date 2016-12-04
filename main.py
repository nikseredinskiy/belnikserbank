import random
import sqlite3 as lite


class Account(object):
    def __init__(self, holder_name):
        self.id = random.randint(0, 999)
        self.holder_name = holder_name
        self.amount = 0

    @staticmethod
    def create_account(holder_name):
        temp = Account(holder_name)
        Account.save_account_to_database(temp)
        print("Account successfully created")
        return temp.id

    @staticmethod
    def init_account(acc_id, holder_name, amount):
        temp = Account(holder_name)
        temp.id = acc_id
        temp.amount = amount
        return temp

    def save_account_to_database(self):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""INSERT INTO accounts (id, holder_name, amount)
                            SELECT * FROM (SELECT ?, ?, ?) AS tmp
                            WHERE NOT EXISTS (
                            SELECT id FROM accounts WHERE id = ?) LIMIT 1;""", (self.id, self.holder_name, self.amount, self.id))
            con.commit()

    @staticmethod
    def update_account_amount(account):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE accounts SET amount=? WHERE id=?""", (account.amount, account.id))
            con.commit()

    @staticmethod
    def fetch_accounts():
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts")

            return cur.fetchall()

    @staticmethod
    def get_all_accounts():
        temp = dict()
        for acc in Account.fetch_accounts():
            temp[acc[0]] = Account.init_account(acc[0], acc[1], acc[2])
        return temp

    @staticmethod
    def make_transaction(transaction):
        if accounts.get(transaction.source_account_id, "404") != "404":
            source_account = accounts.get(transaction.source_account_id)
            if accounts.get(transaction.final_account_id, "404") != "404":
                final_account = accounts.get(transaction.final_account_id)
                if source_account.amount >= transaction.amount > 0:
                    source_account.amount -= transaction.amount
                    final_account.amount += transaction.amount
                    Account.update_account_amount(source_account)
                    Account.update_account_amount(final_account)
                    print("Transaction completed successfully")
                else:
                    print("Not enough money on the source account || Amount can't be negative")
                    print("Transaction doesn't complete")
            else:
                print("Final account doesn't exist")
                print("Transaction doesn't complete")
        else:
            print("Source account doesn't exist")
            print("Transaction doesn't complete")

    @staticmethod
    def increase_amount(account_id, amount):
        if amount > 0:
            source_account = accounts.get(account_id)
            source_account.amount += amount
            Account.update_account_amount(source_account)
            print("Amount successfully increased")

    def print_account_info(self):
        print("{0}'s account {1} info: Amount = {2}".format(self.holder_name, self.id, self.amount))


class Transaction(object):
    def __init__(self, source_account_id, final_account_id, amount):
        self.id = random.randint(0, 99999)
        self.source_account_id = source_account_id
        self.final_account_id = final_account_id
        self.amount = amount


class Menu(object):
    @staticmethod
    def print_header():
        print(""" -------------------------------------""")
        print("""|          Belnikserbank              |""")
        print(""" -------------------------------------""")

    @staticmethod
    def print_main_operations_list():
        print("""|1. Create new account                |""")
        print("""|2. Increase amount                   |""")
        print("""|3. Show accounts list                |""")
        print("""|4. Print account info                |""")
        print("""|5. Make transaction                  |""")
        print("""|6. Cancel transaction                |""")
        print("""|7. Delete this account               |""")
        print("""|8. Quit application                  |""")

    @staticmethod
    def print_footer():
        print(""" -------------------------------------""")

    @staticmethod
    def execute_operating(operation_number, current_account_id):
        if operation_number == "1":
            holder_name = input("Please enter HOLDER_NAME of the new account: ")
            Account.create_account(holder_name)
        if operation_number == "2":
            amount = input("Enter sum of increasing: ")
            Account.increase_amount(current_account_id, int(amount))
        if operation_number == "3":
            temp = Account.get_all_accounts()
            Menu.print_header()
            for i in temp:
                print("""|ID:{0} Name:{1}""".format(temp[i].id, temp[i].holder_name) + " " * (37 - 9 - len(str(temp[i].id) + temp[i].holder_name)) + "|")
            Menu.print_footer()
        if operation_number == "4":
            temp = accounts[current_account_id]
            Menu.print_header()
            print("|" + str(temp.id) + " " + temp.holder_name + " " + str(temp.amount) + " " * (37 - 2 - len(str(temp.id) + temp.holder_name + str(temp.amount))) + "|")
            Menu.print_footer()
        if operation_number == "5":
            final_account_id = input("Enter destination ID: ")
            amount = input("Enter amount of the transaction: ")
            Account.make_transaction(Transaction(current_account_id, int(final_account_id), int(amount)))


accounts = Account.get_all_accounts()
login_id = input("Please enter your account ID: ")
is_working = True
while is_working:
    if accounts.get(int(login_id), "404") != "404":
        Menu.print_header()
        Menu.print_main_operations_list()
        Menu.print_footer()
        operation = input("Enter number of the operation: ")
        if operation != "8":
            Menu.execute_operating(operation, int(login_id))
            accounts = Account.get_all_accounts()
        else:
            is_working = False
    else:
        print("No such account")
        name = input("Enter your name for the new account: ")
        login_id = Account.create_account(name)
        accounts = Account.get_all_accounts()
print("Bye. See you soon!")
