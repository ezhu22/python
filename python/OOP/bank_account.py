class User:
    def __init__(self, name, email_address):
        self.name = name
        self.email = email_address
        self.account = BankAccount(interest_rate = 2, balance = 0)
    def make_deposit(self, amount):
        self.account.balance += amount
        print(f"{self.name} you have deposited ${amount} to your account. Your new balance is ${self.account.balance}")
        return self
    def make_withdrawal(self, amount):
        self.account.balance -= amount
        print(f"{self.name} you have withdrawn ${amount} from your account. Your new balance is ${self.account.balance}")
        return self
    def display_user_balance(self):
        print(f"{self.name} your balance is ${self.account.balance}")
        return self
    def transfer_money(self, other_user, amount):
        self.account.balance -= amount
        print(f"{self.name} you have deducted ${amount} from your account. Your new balance is ${self.account.balance}." )
        other_user.account.balance += amount
        print(f"{other_user.name}, {self.name} has added ${amount} to your account. Your new balance is ${other_user.account.balance}." )
        return self

class BankAccount:
    def __init__(self, interest_rate=2, balance=0):
        self.interest_rate = interest_rate
        self.balance = round(balance, 2)
    def deposit(self, amount):
        self.balance += amount
        print(f"You have deposited ${amount} to your account. Your new balance is ${self.balance}.")
        return self
    def withdrawal(self, amount):
        self.balance -= amount
        print(f"You have withdrawn ${amount} from your account. Your new balance is ${self.balance}.")
        return self
    def display_account_info(self):
        print(f"Your current balance is ${self.balance}.")
        return self
    def yield_interest(self):
        if (self.balance > 0):
            self.balance = round(self.balance * (1 + (self.interest_rate / 100)) , 2)
            print(f"Your interest rate is currently {round(self.interest_rate,2)}%, when applied to your account, you now have a balance of ${self.balance}.")
        else:
            print("Your account is currently overdrafted.")


ninja = User('Ninja', 'ninja@dojo.com')
ninja.account.interest_rate = 5
ninja.account.balance = 5000
ninja.account.deposit(1).deposit(100).deposit(1000).withdrawal(2000).yield_interest()

ninja.make_deposit(200)

ninja.display_user_balance
