class User:
    def __init__(self, username, email_address):
        self.name = username
        self.email = email_address
        self.account_balance = 0
    def make_deposit(self, amount):
        self.account_balance += amount
        print(f"{self.name} you have deposited ${amount} to your account. Your new balance is ${self.account_balance}")
        return self
    def make_withdrawal(self, amount):
        self.account_balance -= amount
        print(f"{self.name} you have withdrawn ${amount} from your account. Your new balance is ${self.account_balance}")
        return self
    def display_user_balance(self):
        print(f"{self.name} your balance is ${self.account_balance}")
        return self
    def transfer_money(self, other_user, amount):
        self.account_balance -= amount
        print(f"{self.name} you have deducted ${amount} from your account. Your new balance is ${self.account_balance}." )
        other_user.account_balance += amount
        print(f"{other_user.name}, {self.name} has added ${amount} to your account. Your new balance is ${other_user.account_balance}." )
        return self

ninja = User("Ninja", "ninja@dojo.com")
pirate = User("Pirate", "pirate@dojo.com")
zombie = User("Zombie", "zombie@dojo.com")

ninja.make_deposit(200).make_deposit(1000).make_deposit(1).make_withdrawal(500).display_user_balance()

pirate.make_deposit(99).make_deposit(666).make_withdrawal(1).make_withdrawal(500).display_user_balance()

zombie.make_deposit(72).make_withdrawal(42).make_withdrawal(1).make_withdrawal(500).display_user_balance()

ninja.transfer_money(zombie, 500)
