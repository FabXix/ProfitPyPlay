import random
from faker import Faker
from colorama import Fore, Style, init
import time

init(autoreset=True)
fake = Faker()

class Company:
    def __init__(self, name, value, income):
        self._name = name
        self._value = value
        self._income = income
        self.previous_income = income
        self.previous_rank = None
        self.news = []

    @property
    def name(self):
        return self._name
    
    @property
    def income(self):
        return self._income
    
    @income.setter
    def income(self, new_income):
        self._income = new_income

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if new_value >= 0:
            self._value = new_value
        else:
            raise ValueError("El valor de la empresa no puede ser negativo.")

    def simulate_value_change(self):
        growth_rate = random.uniform(-0.2, 0.2)
        self.value += self.value * growth_rate
        return growth_rate

    def simulate_income_change(self):
        income_growth_rate = random.uniform(-0.1, 0.1)
        self.previous_income = self.income
        self.income += self.income * income_growth_rate

    def add_news(self, news):
        self.news.append(news)

class User:
    def __init__(self, balance):
        self._balance = balance
        self.investments = {}
        self.total_invested = 0
        self.total_profit_loss = 0
        
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, new_balance):
        if new_balance >= 0:
            self._balance = new_balance
        else:
            raise ValueError("El balance no puede ser negativo.")

    def invest_in_company(self, company, amount):
        if amount > self.balance:
            print(Fore.RED + "You don't have enough money to invest that amount.")
            return

        self.balance -= amount
        self.total_invested += amount
        if company not in self.investments:
            self.investments[company] = {'amount': amount, 'profit_loss': 0}
        else:
            self.investments[company]['amount'] += amount

        print(Fore.GREEN + f"Successfully invested ${amount:.2f} in {company.name}.")
        print(f"New balance: ${self.balance:.2f}")

    def withdraw_from_specific_company(self, company, amount=None):
        if company not in self.investments:
            print(Fore.RED + "You have no investments in this company.")
            return

        invested_amount = self.investments[company]['amount']
        profit_loss = self.investments[company]['profit_loss']
        
        current_value = invested_amount + profit_loss
        
        if amount is None or amount > current_value:
            amount = current_value
        
        withdrawal_ratio = amount / current_value

        self.balance += amount
        self.total_invested -= invested_amount * withdrawal_ratio
        self.total_profit_loss += profit_loss * withdrawal_ratio

        if amount == current_value:
            del self.investments[company]
        else:
            self.investments[company]['amount'] -= invested_amount * withdrawal_ratio
            self.investments[company]['profit_loss'] -= profit_loss * withdrawal_ratio

        print(Fore.GREEN + f"Withdrew ${amount:.2f} from {company.name}.")
        print(f"New balance: ${self.balance:.2f}")

    def show_investment_summary(self):
        if not self.investments:
            print(Fore.YELLOW + "You have no current investments.")
        else:
            print(Style.BRIGHT + "Your current investments:")
            total_value = 0
            for company, details in self.investments.items():
                investment_value = details['amount'] + details['profit_loss']
                total_value += investment_value
                profit_loss = details['profit_loss']
                color = Fore.GREEN if profit_loss >= 0 else Fore.RED
                print(f"{company.name}: Invested: ${details['amount']:.2f}, Current Value: ${investment_value:.2f}, "
                      f"Profit/Loss: {color}${profit_loss:.2f}")
            print(f"Total value of your investments: ${total_value:.2f}")
            print(f"Total profit/loss: {Fore.GREEN if self.total_profit_loss >= 0 else Fore.RED}${self.total_profit_loss:.2f}")

def simulate(companies, user):
    print(Fore.CYAN + "\nSimulating market changes...")

    for company in companies:
        growth_rate = company.simulate_value_change()
        company.simulate_income_change()
        if company in user.investments:
            current_investment = user.investments[company]['amount']
            profit_loss = current_investment * growth_rate
            user.investments[company]['profit_loss'] += profit_loss

    print("\nMarket simulation complete.")

def main():
    companies = [Company(fake.company(), random.uniform(1000000, 10000000), random.uniform(500000, 2000000)) for _ in range(20)]
    
    user = User(100000)

    while True:
        
        for idx, company in enumerate(companies):
            company.previous_rank = idx

        sorted_companies = sorted(companies, key=lambda x: x.value, reverse=True)

        print(Fore.YELLOW + "\nCompanies sorted by value (highest to lowest):")
        for idx, company in enumerate(sorted_companies):
            income_color = Fore.GREEN if company.income > company.previous_income else Fore.RED
            arrow = ""
            if company.previous_rank is not None:
                if company.previous_rank == idx:
                    arrow = "―"
                elif company.previous_rank > idx:
                    arrow = "↑"
                elif company.previous_rank < idx:
                    arrow = "↓"
                
            print(f"{idx + 1}. {company.name} - Value: ${company.value:.2f} - Income: {income_color}${company.income:.2f} {arrow}")

        print(f"\nYour balance: ${user.balance:.2f}")
        
        action = input("Choose an action: (1) Invest, (2) Withdraw, (3) Show Investments, (4) Show Recent Activities, (5) Exit, ( ) Simulate: ").strip()

        if action == '1':
            company_index = int(input("Choose a company index to invest in: ").strip()) - 1
            amount = float(input("Enter the amount to invest: ").strip())
            user.invest_in_company(sorted_companies[company_index], amount)

        elif action == '2':
            user.show_investment_summary()
            if user.investments:
                investment_list = list(user.investments.keys())
                for idx, company in enumerate(investment_list):
                    print(f"{idx + 1}. {company}")

                company_index = int(input("Choose a company index to withdraw from: ").strip()) - 1
                company = investment_list[company_index]
                withdraw_all = input("Withdraw all? (y/n): ").strip().lower()
                if withdraw_all == 'y':
                    user.withdraw_from_specific_company(company)
                else:
                    amount = float(input("Enter the amount to withdraw: ").strip())
                    user.withdraw_from_specific_company(company, amount)

        elif action == '3':
            user.show_investment_summary()

        elif action == '4':
            print(Fore.CYAN + "\nRecent Company Activities:")
            recent_activities = []
            for company in sorted_companies:
                if company.news:
                    for news in company.news[-5:]:
                        recent_activities.append(f"{company.name}: {news}")
            if recent_activities:
                for activity in recent_activities[-5:]:
                    print(f"- {activity}")
            else:
                print("No recent activities available.")

        elif action == '5':
            print("See you! o/")
            time.sleep(2)
            break

        if action not in ['1', '2', '3', '4']:
            simulate(companies, user)
            for company in sorted_companies:
                if random.random() < 0.5:
                    company.add_news(f"{company.name} has implemented a new strategy!")

def print_welcome_message():
    welcome_text = "Welcome to ProfitPyPlay"
    print(Fore.CYAN + Style.BRIGHT + " " * 5 + "╔══════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT + " " * 5 + "║ " + Fore.GREEN + Style.BRIGHT + welcome_text + " " * (29 - len(welcome_text)) + "║")
    print(Fore.CYAN + Style.BRIGHT + " " * 5 + "╚══════════════════════════════╝")
    print(Fore.YELLOW + Style.BRIGHT + " " * 5 + "Let's start investing wisely!")

print_welcome_message()

if __name__ == "__main__":
    main()
