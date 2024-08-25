from functools import reduce
from datetime import date

# ACCOUNT MANAGEMENT
def get_balance(transactions: list[float]):
  return reduce(lambda x,y: round(x+y,2), transactions, 0.0)

def deposit(amount: float, account: dict):
  account['transactions'].append(amount)
  print(f"Seu depósito de R$ {amount} foi processado com sucesso e creditado na sua conta!")

def withdrawal(*, amount: float, account: dict):
  balance = get_balance(account['transactions'])

  if(balance < amount):
    print("Você não tem saldo suficiente para completar este saque. Por favor, verifique seu saldo e tente novamente.")
    return False

  if(amount > 500):
    print("O valor máximo de saque por transação é R$ 500.")
    return False
  
  if(account['withdrawals_today'] >= account['withdrawals_per_day']):
    print(f"Você atingiu seu limite diário de saques ({account['withdrawals_per_day']}). Por favor, tente novamente amanhã.")
    return False
  
  account['transactions'].append(-amount)
  account['withdrawals_today'] += 1
  print(f"Seu saque de R$ {amount} foi processado com sucesso.")
  return True

def extract(balance: float, /, transactions: list[float]):
  print("\n========= EXTRATO =========")
  for transaction in transactions:
    transaction_type = "Saque" if transaction < 0 else "Depósito"
    print(f"{transaction_type}: R$ {round(abs(transaction),2)}")
  print("============================")
  print("\n")

  print(f"Saldo Atual: R$ {balance}")

# LOGIN/REGISTER
def create_user(users: list[dict], /, name: str, birth_date: date, cpf: str, address: str):
  already_exists_user = [user for user in users if user["cpf"] == cpf]

  if(len(already_exists_user) > 0):
    return print("\nNão foi possível realizar o cadastro. O CPF já está em uso!")

  users.append({ "name": name, "birth_date": birth_date, "cpf": cpf, "address": address })
  print("\nUsuário Criado!")

def login(users: list[dict], /, cpf: str):
  already_exists_user = [user for user in users if user["cpf"] == cpf]

  if(len(already_exists_user) == 0):
    return False

  return True

# ACCOUNTS
def get_accounts_by_cpf(accounts: list[dict], /, cpf: str):
  return [account for account in accounts if account["cpf"] == cpf]

def get_account(accounts: list[dict], /, number: int):
  return [account for account in accounts if account["number"] == number][0]

def create_account(accounts: list[dict], /, cpf: str):
  new_account = {
    "ag": "0001",
    "number": 1 if len(accounts) == 0 else accounts[-1].get("number", 0) + 1,
    "cpf": cpf,
    "transactions": [],
    'withdrawals_per_day': 3,
    'withdrawals_today': 0
  }

  accounts.append(new_account)
  print("========= Conta Criada =========")
  print(f"AG: {new_account['ag']}")
  print(f"Conta {new_account['number']}")
  print("=========",end="\n")
  return;

# Utils
def end():
  print("Obrigado por usar nosso aplicativo! Esperamos vê-lo novamente em breve.", end="\n")
  exit()

def await_key():
  print("Pressione Enter para voltar.", end="\n")
  input()

def clean_digits(string: str):
  return string.replace(".", "").replace("-", "")


# MAIN
def main():
  users: list[dict] = []
  accounts: list[dict] = []
  logged = False
  current_cpf = ""
  selected_account = 0
  
  while True:
    # LOGIN/REGISTER
    if not logged:
      option = int(input("""
                       
          ========= SISTEMA BANCÁRIO =========
                   
          [0] Criar Usuário
          [1] Entrar
          [2] Sair
          
          Escolha uma opção: """) or -1)
      print("\n")

      match option:
        case 0:
          name = input("Informe o seu nome: ")
          cpf = clean_digits(input("Informe o seu CPF: "))
          birth_date = input("Informe sua data de nascimento (dia/mês/ano): ")
          print("== Informe os dados do seu endereço abaixo ==")
          street = input("Informe o seu logradouro: ")
          neighborhood = input("Informe o seu bairro: ")
          city = input("Informe a sua cidade: ")
          state = input("Informe o seu estado: ")

          # Format Address
          address = f"{street} - {neighborhood} - {city}/{state}"

          create_user(users, name=name, cpf=cpf, birth_date=birth_date, address=address)
          await_key()
        case 1:
          cpf = clean_digits(input("Informe o seu CPF: "))
          if login(users, cpf=cpf):
            current_cpf = cpf
            logged = True
          else:
            print("\nUsuário não encontrado")
            await_key()

        case 2:
          end()
        
        case _:
          print("Opção inválida! Tente novamente", end="\n")
          await_key()
          
    # CREATE/CHOOSE ACCOUNT
    elif logged and not selected_account:
      option = int(input("""
                       
          ========= SISTEMA BANCÁRIO =========
                   
          [0] Criar Conta
          [1] Entrar em Conta
          [2] Voltar
          [3] Sair
          
          Escolha uma opção: """) or -1)
      print("\n")

      match option:
        case 0:
          create_account(accounts, cpf=current_cpf)
          await_key()
        case 1:
          user_accounts = get_accounts_by_cpf(accounts, cpf=current_cpf)
          if(len(user_accounts) == 0):
            print("Você não possui contas!")
            await_key()
          else:
            print("""========= ESCOLHA UMA CONTA =========""")
            for idx, account in enumerate(user_accounts):
              print(f"[{idx}] Conta: {account['number']}")
            print('\n')
            selected = int(input("Escolha uma opção: "))

            if((len(user_accounts) - 1) < selected):
              print("Opção inválida!")
              await_key()
            else:
              selected_account = user_accounts[selected]['number']
        case 2:
          logged = False
        case 3:
          end()

    # ACCOUNT MANAGEMENT
    else:
      option = int(input("""
                        
            ========= SISTEMA BANCÁRIO =========
                    
            [0] Extrato
            [1] Depósito
            [2] Saque
            [3] Voltar
            [4] Sair
            
            Escolha uma opção: """) or -1)
      print("\n")

      account = get_account(accounts, number=selected_account)
      if option == 4:
        end()
      elif option == 0:
        extract(get_balance(account['transactions']), transactions=account['transactions'])
        await_key()
      elif option == 3:
        selected_account = 0
      elif option in [1,2]:
        amount = float(input("Digite um valor: R$ "))
        if(amount <= 0):
          print("O valor deve ser positivo. Por favor, tente novamente com um valor válido.")
          await_key()
        else:
          match option:
            case 1:
              deposit(amount, account)
              await_key()
            case 2:
              withdrawal(amount=amount, account=account)
              await_key()
      else:
        print("Opção inválida! Tente novamente", end="\n")
        await_key()

main()
