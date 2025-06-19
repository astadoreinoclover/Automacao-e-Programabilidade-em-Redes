import socket
import time
import re
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

# Ocultar logs
sys.stderr = open(os.devnull, 'w')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Oculto
def iniciar_navegador():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--headless")  # modo oculto
    options.add_argument("--window-size=1920,1080")  # simula tela maximizada

    navegador = webdriver.Chrome(options=options)
    navegador.get('https://google.com.br')
    return navegador

# Vizivel
# def iniciar_navegador():
#     options = Options()
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#     navegador = webdriver.Chrome(options=options)
#     navegador.maximize_window()
#     navegador.get('https://google.com.br')
#     return navegador

def abrir_tabela_brasileirao(navegador):
    barra_pesquisa = navegador.find_element(By.NAME, 'q')
    barra_pesquisa.send_keys('Campeonato brasileiro 2025')
    barra_pesquisa.send_keys(Keys.ENTER)
    time.sleep(2)

    link = navegador.find_element(By.PARTIAL_LINK_TEXT, "Tabela e Jogos do Brasileirão Série A 2025")
    link.click()
    time.sleep(2)

def extrair_tabela(navegador):
    linhasEstatisticas = navegador.find_elements(By.CSS_SELECTOR, ".tabela__pontos tbody tr")
    clubes = navegador.find_elements(By.CSS_SELECTOR, ".classificacao__equipes--nome")

    campos = [
        "pontos",
        "jogos",
        "vitórias",
        "empates",
        "derrotas",
        "gols_pro",
        "gols_contra",
        "saldo_de_gols",
        "aproveitamento"
    ]

    tabela_classificacao = {}
    if len(clubes) == len(linhasEstatisticas):
        for clube, estatistica in zip(clubes, linhasEstatisticas):
            valores = estatistica.text.split()
            dados_clube = {campo: valor for campo, valor in zip(campos, valores)}
            tabela_classificacao[clube.text] = dados_clube
    else:
        print("Erro: número de clubes e estatísticas não corresponde.")
    return tabela_classificacao

def mostrar_tabela(tabela_classificacao):
    cabecalho = f"{'Clube':<25} {'P':>3} {'J':>3} {'V':>3} {'E':>3} {'D':>3} {'GP':>4} {'GC':>4} {'SG':>4} {'AP':>5}"
    linhas = [cabecalho, "-" * len(cabecalho)]

    for clube, est in tabela_classificacao.items():
        linha = (
            f"{clube:<25} {est['pontos']:>3} {est['jogos']:>3} {est['vitórias']:>3} "
            f"{est['empates']:>3} {est['derrotas']:>3} {est['gols_pro']:>4} "
            f"{est['gols_contra']:>4} {est['saldo_de_gols']:>4} {est['aproveitamento']:>4}%"
        )
        linhas.append(linha)
    return "\n".join(linhas)

def estatisticas_time(tabela_classificacao, nome_time):
    if nome_time not in tabela_classificacao:
        return "Time não encontrado.\n"

    dados = tabela_classificacao[nome_time]
    texto = (
        f"\n{nome_time} disputou {dados['jogos']} jogos.\n"
        f"Vitórias: {dados['vitórias']}, Empates: {dados['empates']}, Derrotas: {dados['derrotas']}.\n"
        f"Gols pró: {dados['gols_pro']}, Gols contra: {dados['gols_contra']}.\n"
        f"Saldo de gols: {dados['saldo_de_gols']}.\n"
        f"Pontos: {dados['pontos']}, Aproveitamento: {dados['aproveitamento']}%\n"
    )
    return texto

def listar_jogos(navegador, tabela_classificacao):
    jogos = navegador.find_elements(By.CSS_SELECTOR, ".lista-jogos__jogo")
    output = []

    for idx, jogo in enumerate(jogos):
        linhas = jogo.text.split('\n')
        linhas = [linha for linha in linhas if linha.strip() and "FIQUE POR DENTRO" not in linha]

        if len(linhas) >= 3:
            linha0 = linhas[0].strip()
            linha0 = re.sub(r"(Hoje)(\d{2}:\d{2})", r"\1 \2", linha0)
            linha0 = re.sub(r"(\d{2}/\d{2})(\d{2}:\d{2})", r"\1 \2", linha0)

            padrao1 = re.compile(r"^(.*?)(\d{2}/\d{2})\s*([A-Za-zÀ-ÿ]+)?\s*(\d{2}:\d{2})$")
            padrao2 = re.compile(r"^(.*?)\s+(Hoje|[A-Za-zÀ-ÿ]+)?\s*•?\s*(\d{2}:\d{2})$")

            m = padrao1.match(linha0)
            n = padrao2.match(linha0)

            if m or n:
                if m:
                    local, data, dia, hora = m.group(1).strip(), m.group(2), m.group(3) or "", m.group(4)
                else:
                    local, data, dia, hora = n.group(1).strip()[:-4], "Hoje", n.group(2) or "", n.group(3)

                if len(linhas) == 3:
                    casa, visitante, placar = linhas[1], linhas[2], None
                elif len(linhas) >= 6:
                    casa, gols_casa, gols_fora, visitante = linhas[1], linhas[2], linhas[3], linhas[4]
                    placar = f"{gols_casa} x {gols_fora}"
                else:
                    continue

                texto = f"{idx + 1}. {casa} x {visitante} - {data or dia} {hora} ({local})"
                if placar:
                    texto += f" - Placar: {placar}"
                output.append(texto)
    return "\n".join(output)

def getGoleadores(navegador):
    goleadores = navegador.find_elements(By.CSS_SELECTOR, ".ranking-item-wrapper")
    out = []
    for i, g in enumerate(goleadores[:10], 1):
        nome = g.find_element(By.CSS_SELECTOR, ".jogador-nome").text
        gols = g.find_element(By.CSS_SELECTOR, ".jogador-gols").text
        pos = g.find_element(By.CSS_SELECTOR, ".jogador-posicao").text
        time = g.find_element(By.CSS_SELECTOR, ".jogador-escudo img").get_attribute("alt")
        out.append(f"{i}. {nome} {pos} com {gols} gols - {time}")
    return "\n".join(out)

def main():
    navegador = iniciar_navegador()
    abrir_tabela_brasileirao(navegador)
    tabela = extrair_tabela(navegador)

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(1)
    print("Servidor ativo. Aguardando cliente...")

    cliente, _ = servidor.accept()

    menu = """\n======= MENU BRASILEIRÃO =======
1 - Mostrar tabela
2 - Estatísticas do time
3 - Jogos da rodada
4 - Artilheiros
5 - Sair
Digite sua opção: """

    while True:
        cliente.sendall(menu.encode())
        opcao = cliente.recv(2048).decode().strip()

        if opcao == '1':
            cliente.sendall((mostrar_tabela(tabela) + "\n").encode())

        elif opcao == '2':
            nomes_times = list(tabela.keys())
            lista_times = "\n".join([f"{i+1}. {nome}" for i, nome in enumerate(nomes_times)])
            cliente.sendall(f"Times disponíveis:\n{lista_times}\nDigite o número do time:\n".encode())

            try:
                indice = int(cliente.recv(1024).decode().strip()) - 1
                if 0 <= indice < len(nomes_times):
                    nome = nomes_times[indice]
                    cliente.sendall(estatisticas_time(tabela, nome).encode())
                else:
                    cliente.sendall("Número inválido. Tente novamente.\n".encode())
            except ValueError:
                cliente.sendall("Entrada inválida. Digite apenas o número do time.\n".encode())
        elif opcao == '3':
            cliente.sendall((listar_jogos(navegador, tabela) + "\n").encode())

        elif opcao == '4':
            cliente.sendall((getGoleadores(navegador) + "\n").encode())

        elif opcao == '5':
            cliente.sendall("Encerrando conexão. Até logo!\n".encode())
            break

        else:
            cliente.sendall("Opção inválida. Tente novamente.\n".encode())

    cliente.close()
    servidor.close()
    navegador.quit()

if __name__ == "__main__":
    main()