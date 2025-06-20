### Renato Cardozo e Victor Xavier

# 🏆 Sistema de Monitoramento do Campeonato Brasileiro (Série A) - 2025

Este projeto é um **sistema interativo em Python** que utiliza **Selenium** para automatizar a navegação e coleta de informações em tempo real sobre o Campeonato Brasileiro Série A. Ele permite ao usuário visualizar a tabela de classificação, consultar estatísticas específicas de um time e listar os jogos da rodada atual, tudo diretamente no terminal.

---

## 📋 Funcionalidades

- ✅ Acessa automaticamente o Google e pesquisa pela tabela do Brasileirão Série A.
- ✅ Extrai os dados da **tabela de classificação**: pontos, jogos, vitórias, empates, derrotas, gols, saldo e aproveitamento.
- ✅ Permite consultar as **estatísticas detalhadas de um time específico**.
- ✅ Exibe os **jogos da rodada**, com local, data, horário e, se disponível, o placar.
- ✅ Interface de texto simples com **menu interativo** para navegação.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Selenium
- Google Chrome
- ChromeDriver
- Regex (re)
- time

---

## 🧠 Estrutura do Código

### `iniciar_navegador()`
Configura o Selenium WebDriver com um `user-agent` customizado e abre o Google Chrome com a janela maximizada.

### `abrir_tabela_brasileirao(navegador)`
Pesquisa automaticamente no Google por "Campeonato Brasileiro 2025" e acessa a página com a tabela atualizada.

### `extrair_tabela(navegador)`
Extrai os dados da tabela de classificação, retornando um dicionário com:
- Posição
- Clube
- Pontos
- Jogos
- Vitórias
- Empates
- Derrotas
- Gols pró/contra
- Saldo de gols
- Aproveitamento

### `mostrar_tabela(tabela_classificacao)`
Imprime no terminal a **tabela de classificação** de forma formatada e legível.

### `estatisticas_time(tabela_classificacao)`
Permite ao usuário escolher um time da lista e exibe:
- Número de jogos
- Vitórias, empates e derrotas
- Gols pró e contra
- Saldo de gols
- Posição na tabela
- Aproveitamento

### `listar_jogos(navegador, tabela_classificacao)`
Coleta e exibe os **jogos da rodada**, incluindo:
- Time da casa e visitante
- Local
- Data e hora
- Placar (caso disponível)

### `getGoleadores(navegador)`
Coleta e exibe os 10 maiores **artilheiros**, incluindo:
- Nome do jogador
- Número de gols
- Time
- Posição

### `exibir_menu()` e `main()`
Apresenta o **menu principal** ao usuário com as opções:
- Mostrar Tabela
- Estatísticas do Time
- Jogos da Rodada
- Sair

---

## 🔧 Pré-requisitos

1. **Python 3 instalado**  
   Verifique com:
   ```bash
   python --version
   ```

2. **Instale as dependências:**
   ```bash
   pip install selenium
   ```

3. **Baixe o [ChromeDriver](https://sites.google.com/chromium.org/driver/)** compatível com sua versão do Google Chrome e adicione-o ao PATH.

---

## ▶️ Como Executar

1. Clone ou baixe este repositório.
2. Execute o script com:
   ```bash
   python brasileirao.py
   ```
3. Navegue pelo menu interativo no terminal.

---

## ⚠️ Observações

- O sistema depende do **layout da página do Google e do ge.globo.com**, portanto **quebras podem ocorrer** se houver mudanças no HTML dessas páginas.
- É necessária uma **conexão ativa com a internet**.
- A execução pode demorar alguns segundos devido ao uso de `time.sleep()` para garantir que os elementos sejam carregados.

---

## 🕒 Estatísticas de tempo

A métrica de tempo é feita por cada consulta que o script permite.

 - Tempo de execução de script: Até 5s
 - Tempo de execução de manual: Até 60s

 - Tempo de diferença: até 55s

Levando em consideração uma média de 8 pesquisas por dia.

 - 8 * 55 = 440s

Levando em consideração 1 ano de 365 dias.

 - 440 * 365 = 160.600s

Levando em consideração 8 funcionários.

 - 160600 * 8 = 1.284.800s

Transformando em horas trabalhadas:

 - 1.284.800s = 356h +

Levando em consideração uma média de 27 reais por hora:

 - Gera uma economia de R$ 9.612

## 🌐 Comunicação Cliente-Servidor com Socket
**O sistema possui uma arquitetura cliente-servidor baseada em sockets TCP, permitindo que o menu seja acessado remotamente via terminal.**

**🔄 Como funciona:**
O servidor é responsável por inicializar o navegador, coletar os dados do campeonato via Selenium e responder às requisições dos clientes.
O cliente conecta-se ao servidor e interage com o menu pelo terminal.
A comunicação ocorre em tempo real, com envio e recebimento de mensagens codificadas em UTF-8.

## 🔐 Variáveis de Ambiente
**Para facilitar a configuração, os dados de rede são armazenados no arquivo .env:**

**📄 Arquivo .env**
Crie um arquivo chamado .env com as seguintes variáveis:
 ```bash
   HOST='Seu ip'
   PORT='Sua porta'
 ```
Essas variáveis são carregadas no código usando a biblioteca python-dotenv.

Instalação:

```bash
   pip install python-dotenv
```

## 📁 Estrutura do Projeto
```bash
📁 Automacao-e-Programabilidade-em-Redes/
├── servidor.py               # Código principal do servidor
├── cliente.py                # Código cliente com menu interativo
├── .env                      # Configuração de IP e porta
├── .gitignore                # Ignora o .env e outros arquivos desnecessários
└── README.md                 # Documentação do projeto
```
## Rodar o servidor
```bash
python servidor.py
```

## Rodar o cliente
```bash
python cliente.py
```
ou se prefirir
```bash
telnet 'ip' 'porta'
```

## 🧼 Futuras Melhorias

- Substituir `sleep()` por `WebDriverWait` para aguardar elementos dinamicamente.
- Adicionar exportação da tabela em CSV.
- Criar interface gráfica (GUI).
- Permitir busca por nome do time diretamente.

---
