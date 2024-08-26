from abc import ABC, abstractmethod
from datetime import datetime

# Clientes
class Cliente:
  def __init__(self, endereco) -> None:
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)
  
  def adicionar_conta(self, conta):
    self.contas.append(conta)

class PessoaFisica(Cliente):
  def __init__(self, endereco, cpf, nome, data_nascimento) -> None:
    super().__init__(endereco=endereco)
    self.cpf = cpf
    self.nome = nome
    self.data_nascimento = data_nascimento


# Transações
class Historico:
  def __init__(self) -> None:
    self._transacoes = []

  def adicionar_transacao(self, transacao):
    self.transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  
  @property
  def transacoes(self):
    return self._transacoes

class Transacao(ABC):
  @abstractmethod
  def registrar(self, conta):
    pass

class Deposito(Transacao):
  def __init__(self, valor) -> None:
    super().__init__()
    self._valor = valor

  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self._valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

  @property
  def valor(self):
    return self._valor

class Saque(Transacao):
  def __init__(self, valor) -> None:
    super().__init__()
    self._valor = valor

  def registrar(self, conta):
    sucesso_transacao = conta.sacar(self._valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

  @property
  def valor(self):
    return self._valor


# Contas
class Conta:
  ult_numero = 0;
  def __init__(self, cliente: Cliente) -> None:
    Conta.ult_numero += 1
    self._saldo = 0
    self._numero = self.ult_numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()
  
  @property
  def saldo(self):
    return self._saldo

  @property
  def numero(self):
    return self._numero

  @property
  def agencia(self):
    return self._agencia
  
  @property
  def cliente(self):
    return self._cliente

  @property
  def historico(self) -> Historico:
    return self._historico
  
  @classmethod
  def nova_conta(cls, cliente: Cliente):
    return cls(cliente=cliente)

  def sacar(self, valor: float):
    if(self._saldo < valor):
      print("Você não tem saldo suficiente para completar este saque. Por favor, verifique seu saldo e tente novamente.")
      return False
    
    self._saldo -= valor
    print(f"Seu saque de R$ {valor} foi processado com sucesso.")
    return True

  def depositar(self, valor: float):
    self._saldo += valor
    print(f"Seu depósito de R$ {valor} foi processado com sucesso e creditado na sua conta!")
    return True

class ContaCorrente(Conta):
  def __init__(self, cliente: Cliente, limite_por_saque=500, limite_saques=3) -> None:
    super().__init__(cliente)
    self.limite_por_saque = limite_por_saque
    self.limite_saques = limite_saques

  def sacar(self, valor: float):
    if (self.limite_por_saque < valor):
      print(f"O valor máximo de saque por transação é R$ {self.limite_por_saque}.")
      return False

    saques_realizados = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

    if(saques_realizados >= self.limite_saques):
      print(f"Você atingiu seu limite diário de saques ({self.limite_saques}). Por favor, tente novamente amanhã.")
      return False

    return super().sacar(valor)

  def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
  
# Utils
def fim():
  print("Obrigado por usar nosso aplicativo! Esperamos vê-lo novamente em breve.", end="\n")
  exit()

def aguardar_tecla():
  print("Pressione Enter para voltar.", end="\n")
  input()

def limpar_cpf(string: str):
  return string.replace(".", "").replace("-", "")

def obter_cliente(clientes: list[PessoaFisica], /, cpf: str):
  cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
  return cliente[0] if cliente else None

def exibir_extrato(conta: ContaCorrente):
  print("\n========= EXTRATO =========")
  for transacao in conta.historico.transacoes:
    print(f"{transacao['data']} - {transacao['tipo']}: R$ {round(abs(transacao['valor']),2)}")
  print("============================")
  print("\n")

  print(f"Saldo Atual: R$ {conta.saldo:.2f}")


# MAIN
def main():
  clientes: list[Cliente] = []
  logado = False
  cliente_atual: PessoaFisica | None = None
  conta_atual: ContaCorrente | None = None
  
  while True:
    # LOGIN/REGISTER
    if not logado:
      option = int(input("""
                       
          ========= SISTEMA BANCÁRIO =========
                   
          [0] Criar Usuário
          [1] Entrar
          [2] Sair
          
          Escolha uma opção: """) or -1)
      print("\n")

      match option:
        case 0:
          nome = input("Informe o seu nome: ")
          cpf = limpar_cpf(input("Informe o seu CPF: "))
          data_nascimento = input("Informe sua data de nascimento (dia/mês/ano): ")
          print("== Informe os dados do seu endereço abaixo ==")
          rua = input("Informe o seu logradouro: ")
          bairro = input("Informe o seu bairro: ")
          cidade = input("Informe a sua cidade: ")
          estado = input("Informe o seu estado: ")

          # Format Address
          endereco = f"{rua} - {bairro} - {cidade}/{estado}"

          clientes.append(PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco))

          aguardar_tecla()
        case 1:
          cpf = limpar_cpf(input("Informe o seu CPF: "))
          cliente = obter_cliente(clientes, cpf=cpf)
          if cliente:
            cliente_atual = cliente
            logado = True
          else:
            print("\nCliente não encontrado")
            aguardar_tecla()

        case 2:
          fim()
        
        case _:
          print("Opção inválida! Tente novamente", end="\n")
          aguardar_tecla()
          
    # CREATE/CHOOSE ACCOUNT
    elif logado and not conta_atual:
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
          nova_conta = ContaCorrente.nova_conta(cliente=cliente_atual)
          cliente_atual.adicionar_conta(nova_conta)
          print("========= Conta Criada =========")
          print(nova_conta)
          print("=========",end="\n")
          aguardar_tecla()
        case 1:
          if(len(cliente_atual.contas) == 0):
            print("Você não possui contas!")
            aguardar_tecla()
          else:
            print("""========= ESCOLHA UMA CONTA =========""")
            for idx, conta in enumerate(cliente_atual.contas):
              print(f"[{idx}] AG: {conta.agencia} - Conta: {conta.numero}")
            print('\n')
            conta_selecionada = int(input("Escolha uma opção: "))

            if((len(cliente_atual.contas) - 1) < conta_selecionada):
              print("Opção inválida!")
              aguardar_tecla()
            else:
              conta_atual = cliente_atual.contas[conta_selecionada]
        case 2:
          logado = False
        case 3:
          fim()

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

      if option == 4:
        fim()
      elif option == 0:
        exibir_extrato(conta_atual)
        aguardar_tecla()
      elif option == 3:
        conta_atual = None
      elif option in [1,2]:
        valor = float(input("Digite um valor: R$ "))
        if(valor <= 0):
          print("O valor deve ser positivo. Por favor, tente novamente com um valor válido.")
          aguardar_tecla()
        else:
          match option:
            case 1:
              cliente_atual.realizar_transacao(conta_atual, Deposito(valor))
              aguardar_tecla()
            case 2:
              cliente_atual.realizar_transacao(conta_atual, Saque(valor))
              aguardar_tecla()
      else:
        print("Opção inválida! Tente novamente", end="\n")
        aguardar_tecla()

main()
