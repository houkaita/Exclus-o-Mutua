# Distribuição de Exclusão Mútua em Sistemas Distribuídos

Este projeto implementa um algoritmo de exclusão mútua centralizado para sistemas distribuídos. Ele inclui um coordenador que gerencia o acesso à região crítica e múltiplos processos que solicitam esse acesso.

## Descrição

O objetivo deste trabalho é garantir que vários processos possam acessar uma região crítica de forma exclusiva, utilizando um coordenador central que controla a ordem de acesso. 

### Componentes

- **Coordinator:** O coordenador que gerencia os acessos à região crítica, respondendo a requisições dos processos e mantendo uma fila de pedidos.
- **Process:** Os processos que solicitam acesso à região crítica, escrevem no arquivo `resultado.txt` e liberam o acesso após um tempo de espera.

## Estrutura do Projeto

- `coordinator.py`: Script que implementa o coordenador.
- `process.py`: Script que implementa um processo que se conecta ao coordenador.
- `resultado.txt`: Arquivo onde os processos registram seu acesso à região crítica.

## Requisitos

- Python 3.x
- Bibliotecas padrão do Python: `socket`, `threading`, `queue`, `time`

## Como Rodar

### Passo 1: Iniciar o Coordenador

Primeiro, inicie o coordenador em um terminal. O coordenador ficará ouvindo as requisições dos processos.

```bash
python coordinator.py
```

### Passo 2: Iniciar os Processos
Em outro terminal, inicie os processos. Cada processo deve ser iniciado separadamente com um ID e o número de repetições.

```bash
python process.py 1 5
python process.py 2 5
python process.py 3 5
```

- **1, 2, 3**: IDs dos processos.
- **5**: Número de repetições que o processo solicitará acesso à região crítica.

## Observando a Execução

Durante a execução do projeto, você verá as seguintes mensagens exibidas no terminal, tanto no lado do coordenador quanto no lado dos processos:

- **REQUEST**: Mensagem enviada pelo processo para solicitar acesso à região crítica.
- **GRANT**: Mensagem enviada pelo coordenador para conceder o acesso à região crítica.
- **RELEASE**: Mensagem enviada pelo processo para liberar o acesso à região crítica.

Além disso, o arquivo `resultado.txt` será atualizado pelos processos, registrando os acessos à região crítica.

## Estrutura de Mensagens

As mensagens trocadas entre os processos e o coordenador seguem o formato:

- **REQUEST**: Mensagem enviada pelo processo para solicitar acesso à região crítica.  
  Exemplo: `REQUEST|1|000000`

- **GRANT**: Mensagem enviada pelo coordenador para conceder o acesso à região crítica.  
  Exemplo: `GRANT`

- **RELEASE**: Mensagem enviada pelo processo para liberar o acesso à região crítica.  
  Exemplo: `RELEASE|1|000000`

## Exemplo de Execução

1. O coordenador recebe um `REQUEST` de um processo, coloca-o na fila e, se a fila estiver vazia, envia um `GRANT` ao processo.
2. O processo que recebe o `GRANT` acessa a região crítica, registra a operação no arquivo `resultado.txt`, e então envia um `RELEASE` ao coordenador.
3. O coordenador processa o próximo pedido na fila.

## Requisitos

- Python 3.x
- Biblioteca de sockets
- Biblioteca de threads

## Instruções de Execução

1. **Inicie o coordenador**: Execute o script do coordenador em um terminal.
2. **Inicie os processos**: Execute os scripts dos processos em terminais separados.
