from functools import reduce

def get_balance(transactions: list[float]):
  return reduce(lambda x,y: round(x+y,2), transactions, 0.0)

def deposit(amount: float, transactions):
  transactions.append(amount)
  print(f"Seu depósito de R$ {amount} foi processado com sucesso e creditado na sua conta!")

def withdrawal(amount: float, transactions):
  balance = get_balance(transactions)

  if(balance < amount):
    print("Você não tem saldo suficiente para completar este saque. Por favor, verifique seu saldo e tente novamente.")
    return False

  if(amount > 500):
    print("O valor máximo de saque por transação é R$ 500.")
    return False
  
  transactions.append(-amount)
  print(f"Seu saque de R$ {amount} foi processado com sucesso.")
  return True

def extract(transactions: list[float]):
  balance = get_balance(transactions)

  print("\n========= EXTRATO =========")
  for transaction in transactions:
    transaction_type = "Saque" if transaction < 0 else "Depósito"
    print(f"{transaction_type}: R$ {round(abs(transaction),2)}")
  print("============================")
  print("\n")

  print(f"Saldo Atual: R$ {balance}")

def main():
  transactions: list[float] = []
  withdrawals_per_day = 3
  withdrawals_today = 0

  while True:
    option = int(input("""
                       
          ========= SISTEMA BANCÁRIO =========
                   
          [0] Extrato
          [1] Depósito
          [2] Saque
          [3] Sair
          
          Escolha uma opção: """) or -1)
    print('\n')

    if option == 3:
      print("Obrigado por usar nosso aplicativo! Esperamos vê-lo novamente em breve.", end="\n")
      break
    elif option == 0:
      extract(transactions)
    elif option in [1,2]:
      amount = float(input("Digite um valor: R$ "))
      if(amount <= 0):
        print("O valor deve ser positivo. Por favor, tente novamente com um valor válido.")
      else:
        match option:
          case 1:
            deposit(amount, transactions)
          case 2:
            if(withdrawals_today >= withdrawals_per_day):
              print(f"Você atingiu seu limite diário de saques ({withdrawals_per_day}). Por favor, tente novamente amanhã.")
            else:
              if withdrawal(amount, transactions):
                withdrawals_today += 1

    else:
      print("Opção inválida! Tente novamente", end="\n")
    
    print("Pressione Enter para voltar.", end="\n")
    input()

main()
