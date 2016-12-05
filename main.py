import random
import sqlite3 as lite


class Account(object):
    def __init__(self, holder_name, password):
        self.id = random.randint(0, 999)
        self.holder_name = holder_name
        self.amount = 0
        self.password = password

    @staticmethod
    def create_account(holder_name, password):
        temp = Account(holder_name, password)
        Account.save_account_to_database(temp)
        print("Account successfully created")
        return temp.id

    @staticmethod
    def init_account(acc_id, holder_name, amount, password):
        temp = Account(holder_name, password)
        temp.id = acc_id
        temp.amount = amount
        return temp

    def save_account_to_database(self):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""INSERT INTO accounts (id, holder_name, amount, password)
                            SELECT * FROM (SELECT ?, ?, ?, ?) AS tmp
                            WHERE NOT EXISTS (
                            SELECT id FROM accounts WHERE id = ?) LIMIT 1;""",
                        (self.id, self.holder_name, self.amount, self.password, self.id))
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
            temp[acc[0]] = Account.init_account(acc[0], acc[1], acc[2], acc[3])
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
                    transaction.save_transaction_to_database()
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

    @staticmethod
    def decrease_amount(account_id, amount):
        if amount > 0:
            source_account = accounts.get(account_id)
            if source_account.amount > amount:
                source_account.amount -= amount
                Account.update_account_amount(source_account)
                print("Amount successfully decreased")
            else:
                print("Not enough money for decreasing")

    def print_account_info(self):
        print("{0}'s account {1} info: Amount = {2}".format(self.holder_name, self.id, self.amount))


class Transaction(object):
    def __init__(self, source_account_id, final_account_id, amount):
        self.id = random.randint(0, 99999)
        self.source_account_id = source_account_id
        self.final_account_id = final_account_id
        self.amount = amount

    def save_transaction_to_database(self):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""INSERT INTO transactions (id, source_account_id, final_account_id, amount)
                                    SELECT * FROM (SELECT ?, ?, ?, ?) AS tmp
                                    WHERE NOT EXISTS (
                                    SELECT id FROM transactions WHERE id = ?) LIMIT 1;""",
                        (self.id, self.source_account_id, self.final_account_id, self.amount, self.id))
            con.commit()

    @staticmethod
    def fetch_account_transactions(account_id):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM transactions WHERE source_account_id = ?", (account_id,))

            return cur.fetchall()

    @staticmethod
    def get_all_accounts_transactions(account_id):
        temp = dict()
        for acc_tr in Transaction.fetch_account_transactions(account_id):
            temp[acc_tr[0]] = Transaction.init_transaction(acc_tr[0], acc_tr[1], acc_tr[2], acc_tr[3])
        return temp

    @staticmethod
    def init_transaction(tr_id, tr_source_id, tr_final_id, tr_amount):
        temp = Transaction(tr_source_id, tr_final_id, tr_amount)
        temp.id = tr_id
        return temp

    def delete_transaction(self):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""DELETE FROM transactions WHERE id = ?""", (self.id,))
            con.commit()

    def cancel_transaction(self):
        Account.increase_amount(self.source_account_id, self.amount)
        Account.decrease_amount(self.final_account_id, self.amount)
        self.delete_transaction()


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
            password = input("Enter password for the new account: ")
            Account.create_account(holder_name, password)
        if operation_number == "2":
            amount = input("Enter sum of increasing: ")
            Account.increase_amount(current_account_id, int(amount))
        if operation_number == "3":
            temp = Account.get_all_accounts()
            Menu.print_header()
            for i in temp:
                print("""|ID:{0} Name:{1}""".format(temp[i].id, temp[i].holder_name) + " " * (
                    37 - 9 - len(str(temp[i].id) + temp[i].holder_name)) + "|")
            Menu.print_footer()
        if operation_number == "4":
            temp = accounts[current_account_id]
            Menu.print_header()
            print("|" + str(temp.id) + " " + temp.holder_name + " " + str(temp.amount) + " " * (
                37 - 2 - len(str(temp.id) + temp.holder_name + str(temp.amount))) + "|")
            Menu.print_footer()
        if operation_number == "5":
            final_account_id = input("Enter destination ID: ")
            amount = input("Enter amount of the transaction: ")
            Account.make_transaction(Transaction(current_account_id, int(final_account_id), int(amount)))
        if operation_number == "6":
            transactions_list = Transaction.get_all_accounts_transactions(current_account_id)
            Menu.print_header()
            for i in transactions_list:
                print("""|ID:{0} To:{1} Amount:{2}""".format(transactions_list[i].id,
                                                             transactions_list[i].final_account_id,
                                                             transactions_list[i].amount) + " " * (
                          37 - 15 - len(str(transactions_list[i].id)) - len(str(transactions_list[i].final_account_id))
                          - len(str(transactions_list[i].amount))) + "|")
            Menu.print_footer()
            cancel_transaction_id = input("Enter Transaction ID: ")
            for i in transactions_list:
                if transactions_list[i].id == int(cancel_transaction_id):
                    transactions_list[i].cancel_transaction()
                    break


accounts = Account.get_all_accounts()
is_working = True
login_id = input("Please enter your account ID: ")
if accounts.get(int(login_id), "404") != "404":
    user_password = input("Enter password: ")
    if user_password == accounts.get(int(login_id)).password:
        is_auth = True
while is_working:
    if accounts.get(int(login_id), "404") != "404" and is_auth:
        Menu.print_header()
        Menu.print_main_operations_list()
        Menu.print_footer()
        operation = input("Enter number of the operation: ")
        if operation != "8":
            Menu.execute_operating(operation, int(login_id))
            accounts = Account.get_all_accounts()
        else:
            is_working = False
    elif accounts.get(int(login_id), "404") != "404" and not is_auth:
        print("Wrong password")
        is_working = False
    elif accounts.get(int(login_id), "404") == "404":
        print("No such account")
        name = input("Enter your name for the new account: ")
        user_pass = input("Enter password for the new account: ")
        login_id = Account.create_account(name, user_pass)
        is_auth = True
        accounts = Account.get_all_accounts()
print("Bye. See you soon!")
