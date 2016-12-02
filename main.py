import random
import sqlite3 as lite


class Account(object):
    def __init__(self, holder_name):
        self.id = random.randint(0, 99999)
        self.holder_name = holder_name
        self.amount = 0
        accounts[self.id] = self
        self.save_account_to_database()

    def save_account_to_database(self):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""INSERT INTO accounts(id, holder_name, amount) VALUES (?, ?, ?);""", (self.id,
                                                                                                self.holder_name,
                                                                                                self.amount))
            con.commit()

    @staticmethod
    def update_account_amount(account):
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE accounts SET amount=? WHERE id=?""", (account.amount, account.id))
            con.commit()

    @staticmethod
    def get_all_accounts():
        con = lite.connect('database.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT (id, holder_name, amount) FROM accounts")

            return cur.fetchall()

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

    def increase_amount(self, amount):
        if amount > 0:
            source_account = accounts.get(self.id)
            source_account.amount += amount
            Account.update_account_amount(source_account)

    def print_account_info(self):
        print("{0}'s account {1} info: Amount = {2}".format(self.holder_name, self.id, self.amount))


class Transaction(object):
    def __init__(self, source_account_id, final_account_id, amount):
        self.id = random.randint(0, 99999)
        self.source_account_id = source_account_id
        self.final_account_id = final_account_id
        self.amount = amount

accounts = Account.get_all_accounts()
first_account = Account("Mikita Seradzinski")
first_account.increase_amount(1000000)
second_account = Account("Anastasia Sadovaya")

first_account.print_account_info()
second_account.print_account_info()

Account.make_transaction(Transaction(first_account.id, second_account.id, 1000))
first_account.print_account_info()
second_account.print_account_info()
