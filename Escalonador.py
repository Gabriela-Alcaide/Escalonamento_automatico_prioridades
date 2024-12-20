# -*- coding: utf-8 -*-
"""EP1 - Escalonador.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kw6QwtM0qAsPwNOly1lmUeztCBhwJ2Tm
"""

import os

#BCP - BLOCO DE CONTROLE DE PROCESSOS
# cada linha da tabela de processos deverá conter uma referência ao BCP
# o BCP irá conter toda a informação necessária para que o processo, após interrompido temporariamente, volte a rodar (salvar o contexto!)
# o BCP deverá conter (pelo menos) o Contador de Programa, o estado do processo (Executando, Pronto e Bloqueado), sua prioridade, o estado atual
# dos seus registradores de uso geral (X e Y), uma referência à região da memória em que está o código do programa executado (representado, por exemplo,
# por um arranjo de Strings, contendo a lista de instruções do programa), bem como o nome do programa.

class BCP:
  def __init__ (self, nome, prioridade, codigo, quanta_por_surto): # Construtor da classe BCP
    self.nome = nome # Representa o processo associado ao BCP
    self.pc = 0 # Inicializando o Contador de Programa com 0
    self.estado = "Pronto" # O processo começa na fila de prontos
    self.prioridade = prioridade # A prioridade do processo é aquela passada como parâmetro
    self.X = 0 # Inicializada com 0, vamos guardar dados temporários aqui,
    self.Y = 0 # e aqui também!
    self.creditos = prioridade # Inicializado com a mesma prioridade do processo e será decrementado quando o processo for executado
    self.codigo = codigo # Referência ao segmento de texto programa
    self.quanta_por_surto = quanta_por_surto # Quantum lido do arquivo quantum.txt
    self.tempo_bloqueado = 0 # Representa quanto tempo o processo está esperando a E/S

# LEITURA QUANTUM
# função recebe um arquivo txt correspondente ao quantum utilizado e retorna o quantum

def leituraQuantum(file):
    f = open(file, 'r')
    quantum = int(f.read()[0])
    return quantum

# LEITURA PRIORIDADES
# função recebe um arquivo txt correpondente à lista de prioridades e retorna um array em que prioridades[i] = prioridade do arquivo número i+1

def leituraPrioridades(file, prioridades):
    f = open(file, 'r')
    i = 0
    for i in f:
        prioridades.append(int(i.strip()))
    return prioridades

# LEITURA DE TODOS OS ARQUIVOS NA PASTA './programas'

def readAllFiles(prioridades:list[int], programasNomes:list[str]):
    uploaded = os.listdir('./programas')

    quantProgramas = 0
    quantum = 0

    for i in uploaded:
        if 'quantum.txt'==i:
            quantum = leituraQuantum('./programas/'+i)
        elif 'prioridades.txt'==i:
            prioridades = leituraPrioridades('./programas/'+i, prioridades)
        else:
            programasNomes.append(i)
            quantProgramas+=1

    programasNomes = sorted(programasNomes, key=lambda x:int(x.split('.')[0]))

    return (quantum, quantProgramas)

prioridades = []
programasNomes = []

(quantum, quantProgramas) = readAllFiles(prioridades, programasNomes)

# CLASSE PROCESSO
# o método __init__ realiza a leitura de um processo e armaze seus dados em um BCP
# quando for criada a tabela de prioridades, será necessário colocar o BCP na tabela (acho que seria mais fácil fazer pelo método __init__ de BCP)

# Os processos vão de 01 a 10.

class processo:
  def __init__(self, file, prioridade, quanta_por_surto):
        # Cria o BCP (Bloco de Controle de Processo) associado ao processo
        f = open(file, 'r')
        nome = f.readline().strip()
        numero = os.path.split(file)[-1]
        numero = int(numero.split('.')[0])
        codigo = []
        line = f.readline().strip()
        while line != "":
          codigo.append(line)
          line = f.readline().strip()
        self.bcp = BCP(nome, prioridade[numero-1], codigo, quanta_por_surto)

  def get_estado(self): # Metodo getter para estado
    return self.bcp.estado # Atributo privado

  def set_estado(self, estado): # Metodo setter para estado
    self.bcp.estado = estado

from pickle import TRUE
#Tabela de processos
#Recebe a lista dos programas cujos os quais foram feitas as respectivas leituras assim como suas prioridades
# Possui duas tabelas internas, de processos prontos (ordenado por suas prioridades) e processos bloqueados
# Ao ser inicializada todos os processos passados como parâmetro através da lista de programas vão para a tabela de prontos

class TabelaDeProcessos:

  # MÉTODO CONSTRUTOR - INICIALIZA OS ATRIBUTOS DA TABELA DE PROCESSO.
  def __init__(self, programasNomes, prioridades, quanta_por_surto):
    # Fila de prontos - começa com todos os processos, ordenados em ordem decrescente dos créditos.
    self.fila_prontos = []
    for i in programasNomes:
      self.fila_prontos.append(processo('./programas/'+i, prioridades, quanta_por_surto))
      self.fila_prontos.sort(key=lambda p:p.bcp.creditos, reverse=True)
    # Fila de bloqueados - começa vazia.
    self.fila_bloqueados = []

  # MÉTODO QUE DIZ SE A FILA DE PRONTOS TEM PROCESSOS.
  def ha_prontos(self):
    return len(self.fila_prontos) != 0

  # MÉTODO QUE DIZ SE A FILA DE BLOQUEADOS TEM PROCESSOS.
  def ha_bloqueados(self):
    return len(self.fila_bloqueados) != 0

  # MÉTODO QUE ESCALONA UM DOS PROCESSOS PRONTOS - ESCOLHE O QUE TEM MAIS CRÉDITOS NO MOMENTO.
  def escalonar_pronto(self):
    return self.fila_prontos[0]

  # MÉTODO QUE ORDENA A FILA DE PRONTOS - ORDEM DECRESCENTE DE CRÉDITOS.
  def ordena_prontos(self):
    self.fila_prontos.sort(key=lambda p:p.bcp.creditos, reverse=True)

  # MÉTODO QUE INSERE UM PROCESSO NA FILA DE PRONTOS + ORDENA ESSA FILA.
  def inserir_prontos(self, processo):
    self.fila_prontos.append(processo)
    self.ordena_prontos()

  # MÉTODO QUE REMOVE UM PROCESSO DA FILA DE PRONTOS.
  def remover_prontos(self, processo):
    self.fila_prontos.remove(processo)

  # MÉTODO QUE INSERE UM PROCESSO NA FILA DE BLOQUEADOS.
  def inserir_bloqueados(self, processo):
    self.fila_bloqueados.append(processo)

  # MÉTODO QUE REMOVE UM PROCESSO DA FILA DE BLOQUEADOS.
  def remover_bloqueados(self, processo):
    self.fila_bloqueados.remove(processo)

# Escalonador.
# Recebe um processo.
def escalonador(processo, tabela_processos, vals_medias):

  # Escrevendo o nome do processo que será executado.
  with open(nome_arquivo, "a") as arquivo:
      arquivo.write(f"Executando {processo.bcp.nome}\n")

  # Marcar que mais um quantum será rodado.
  vals_medias["num_quanta"] = vals_medias["num_quanta"] + 1

  i = 0

  # Para cada quanta que esse processo roda por vez:
  for i in range (1,processo.bcp.quanta_por_surto+1):

    # Obtém a próxima instrução a ser executada.
    instrucao = processo.bcp.codigo[processo.bcp.pc]

    # Incrementa PC.
    processo.bcp.pc = processo.bcp.pc + 1

    # Executa a instrução.
    # Se tem "X=", atualizar registrador X desse processo.
    if "X=" in instrucao:
      # Atualiza estado no BCP para "Executando".
      processo.bcp.estado = "Executando"
      processo.bcp.X = int(instrucao.split("=")[1])
      # Marcar que mais uma instrução foi executada.
      vals_medias["num_instrucoes"] = vals_medias["num_instrucoes"] + 1

    # Se tem "Y=", atualizar registrador Y desse processo.
    if "Y=" in instrucao:
      # Atualiza estado no BCP para "Executando".
      processo.bcp.estado = "Executando"
      processo.bcp.Y = int(instrucao.split("=")[1])
      # Marcar que mais uma instrução foi executada.
      vals_medias["num_instrucoes"] = vals_medias["num_instrucoes"] + 1

    # Se tem "E/S":
    if "E/S" in instrucao:
      # Atualizada o estado no BCP para "Bloqueado".
      processo.bcp.estado = "Bloqueado"
      # Atualizar o tempo que o processo deve ficar bloqueado (=2).
      processo.bcp.tempo_bloqueado = 2
      # Vai para fila de bloqueados.
      tabela_processos.inserir_bloqueados(processo)
      # Sai da fila de prontos.
      tabela_processos.remover_prontos(processo)
      # Escrever o nome do processo que inicia uma E/S.
      with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"E/S iniciada em {processo.bcp.nome}\n")
      # Escrever o nome do processo que está sendo interrompido, e o número de instruções executadas até a interrupção.
      with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"Interrompendo {processo.bcp.nome} após {i} instruções\n")
      # Sinalizar que houve mais uma interrupção de processo.
      vals_medias["num_interrupcoes"] = vals_medias['num_interrupcoes'] + 1
      # Marcar que mais uma instrução foi executada.
      vals_medias["num_instrucoes"] = vals_medias["num_instrucoes"] + 1
      break

    # Se tem "SAIDA":
    if "SAIDA" in instrucao:
      # Atualiza estado para "Finalizado".
      processo.bcp.estado = "Finalizado"
      # Sai da fila de prontos.
      tabela_processos.remover_prontos(processo)
      # Não há mais o que fazer com esse processo.
      # Escrever o nome do processo que terminou, com seus registradores.
      with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{processo.bcp.nome} terminado. X={processo.bcp.X}. Y={processo.bcp.Y}\n")
      # Sinalizar que houve mais uma interrupção de processo.
      vals_medias["num_interrupcoes"] = vals_medias['num_interrupcoes'] + 1
      # Marcar que mais uma instrução foi executada.
      vals_medias["num_instrucoes"] = vals_medias["num_instrucoes"] + 1
      break

  if i == processo.bcp.quanta_por_surto and processo.bcp.estado != "Bloqueado":
    # Escrever o nome do processo que está sendo interrompido, e o número de instruções executadas até a interrupção.
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"Interrompendo {processo.bcp.nome} após {i} instruções\n")
    # Sinalizar que houve mais uma interrupção de processo.
    vals_medias["num_interrupcoes"] = vals_medias['num_interrupcoes'] + 1

  # Decrementar 01 crédito.
  if processo.bcp.creditos > 0:
    processo.bcp.creditos = processo.bcp.creditos - 1

  tabela_processos.ordena_prontos()

  # Decremente 01 de todos os processos na fila de bloqueados (contanto que tempo_bloqueado > 0.)
  processos_a_desbloquear = []
  for i in tabela_processos.fila_bloqueados:
    if i.bcp.tempo_bloqueado > 0 and i != processo:
      i.bcp.tempo_bloqueado = i.bcp.tempo_bloqueado - 1
      if i.bcp.tempo_bloqueado == 0:
        # Se tempo_bloqueado == 0, não está mais bloqueado.
        i.bcp.estado = "Pronto"
        processos_a_desbloquear.append(i)
        # Insere na fila de prontos, conforme prioridade.
        tabela_processos.inserir_prontos(i)

  for i in processos_a_desbloquear:
    tabela_processos.remover_bloqueados(i)

  if all(i.bcp.creditos == 0 for i in tabela_processos.fila_prontos + tabela_processos.fila_bloqueados):
    for j in tabela_processos.fila_prontos:
      j.bcp.creditos = j.bcp.prioridade
    for k in tabela_processos.fila_bloqueados:
      k.bcp.creditos = k.bcp.prioridade
    tabela_processos.ordena_prontos()

# Gerando arquivo para escrita.
if quantum < 10:
  nome_arquivo = f"log0{quantum}.txt"
else:
  nome_arquivo = f"log{quantum}.txt"

# Criar a tabela de processos.
tabela_processos = TabelaDeProcessos(programasNomes, prioridades, quantum)

# Escrever os processos carregados - na ordem em que estão na fila de prontos.
for p in tabela_processos.fila_prontos:
  with open(nome_arquivo, "a") as arquivo:
    arquivo.write(f"Carregando {p.bcp.nome}\n")

# No início, todos os processos estão em fila_prontos.
total_processos = len(programasNomes)

# Valores para médias.
vals_medias = {"num_interrupcoes": 0, "num_instrucoes": 0, "num_quanta": 0}

while True:

  if tabela_processos.ha_prontos():
    escalonador(tabela_processos.escalonar_pronto(), tabela_processos, vals_medias)
    tabela_processos.ordena_prontos()

  elif tabela_processos.ha_bloqueados():
    for i in tabela_processos.fila_bloqueados:
      i.bcp.tempo_bloqueado = i.bcp.tempo_bloqueado - 1
      if i.bcp.tempo_bloqueado == 0:
        i.bcp.estado = "Pronto"
        tabela_processos.inserir_prontos(i)
        tabela_processos.remover_bloqueados(i)
        escalonador(i, tabela_processos, vals_medias)
        break

  else:
    break

# Número de interrupções de processos.
num_interrupcoes = vals_medias["num_interrupcoes"]

# Número de instruções executadas.
num_instrucoes = vals_medias["num_instrucoes"]

# Número de quanta rodados.
num_quanta = vals_medias["num_quanta"]

# Escrever média de trocas.
with open(nome_arquivo, "a") as arquivo:
  arquivo.write(f"MEDIA DE TROCAS: {num_interrupcoes / total_processos}\n")

# Escrever média de instruções.
with open(nome_arquivo, "a") as arquivo:
  arquivo.write(f"MEDIA DE INSTRUCOES: {num_instrucoes / num_quanta}\n")

# Escrever o quantum usado.
with open(nome_arquivo, "a") as arquivo:
  arquivo.write(f"QUANTUM: {quantum}\n")

# Baixar o logfile gerado se estiver usando o google colab.
# from google.colab import files
# files.download(nome_arquivo)

