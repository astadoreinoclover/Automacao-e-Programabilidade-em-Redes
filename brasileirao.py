from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Inicializa o navegador
def iniciar_navegador():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    navegador = webdriver.Chrome(options=options)
    navegador.maximize_window()
    navegador.get('https://google.com.br')
    return navegador

# Pesquisa e acessa a página da tabela
def abrir_tabela_brasileirao(navegador):
    barra_pesquisa = navegador.find_element(By.NAME, 'q')
    barra_pesquisa.send_keys('Campeonato brasileiro 2025')
    barra_pesquisa.send_keys(Keys.ENTER)
    time.sleep(2)  # espera carregar resultados

    link = navegador.find_element(By.PARTIAL_LINK_TEXT, "Tabela e Jogos do Brasileirão Série A 2025")
    link.click()
    time.sleep(2)  # espera carregar a página da tabela

# Extrai tabela de classificação
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

# Exibe a tabela formatada
def mostrar_tabela(tabela_classificacao):
    cabecalho = f"{'Clube':<25} {'P':>3} {'J':>3} {'V':>3} {'E':>3} {'D':>3} {'GP':>4} {'GC':>4} {'SG':>4} {'AP':>5}"
    print(cabecalho)
    print("-" * len(cabecalho))

    for clube, estatisticas in tabela_classificacao.items():
        print(f"{clube:<25} "
              f"{estatisticas['pontos']:>3} "
              f"{estatisticas['jogos']:>3} "
              f"{estatisticas['vitórias']:>3} "
              f"{estatisticas['empates']:>3} "
              f"{estatisticas['derrotas']:>3} "
              f"{estatisticas['gols_pro']:>4} "
              f"{estatisticas['gols_contra']:>4} "
              f"{estatisticas['saldo_de_gols']:>4} "
              f"{estatisticas['aproveitamento']:>4}%")

# Exibe estatísticas de um time selecionado
def estatisticas_time(tabela_classificacao):
    print("Times disponíveis:\n")
    for i, clube in enumerate(tabela_classificacao.keys(), start=1):
        print(f"{i}. {clube}")

    try:
        escolha = int(input("\nDigite o número do time desejado: ")) - 1
        nomes_times = list(tabela_classificacao.keys())
        if 0 <= escolha < len(nomes_times):
            time = nomes_times[escolha]
            dados = tabela_classificacao[time]

            texto = (
                f"\n{time} disputou {dados['jogos']} jogos.\n"
                f"Conquistou {dados['vitórias']} vitórias, "
                f"{dados['empates']} empates e {dados['derrotas']} derrotas.\n"
                f"Marcou {dados['gols_pro']} gols e sofreu {dados['gols_contra']}.\n"
                f"Tem um saldo de gols de {dados['saldo_de_gols']}.\n"
                f"Está na {escolha+1} posição com {dados['pontos']} pontos e um aproveitamento de {dados['aproveitamento']}%."
            )
            print(texto)
        else:
            print("Número inválido. Por favor, escolha um número da lista.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Lista jogos da rodada
def listar_jogos(navegador, tabela_classificacao):
    jogos = navegador.find_elements(By.CSS_SELECTOR, ".lista-jogos__jogo")
    jogos_disponiveis = []

    for idx, jogo in enumerate(jogos):
        linhas = jogo.text.split('\n')
        linhas = [linha for linha in linhas if linha.strip() and "FIQUE POR DENTRO" not in linha]

        if len(linhas) >= 3:
            linha0 = linhas[0]
            padrao = re.compile(r"(.*?)(\d{2}/\d{2})([A-Za-zÀ-ÿ]+)?(\d{2}:\d{2})")
            m = padrao.match(linha0)

            if m:
                local = m.group(1).strip()
                data = m.group(2)
                dia = m.group(3) if m.group(3) else ""
                hora = m.group(4)

                if len(linhas) == 3:
                    time_casa = linhas[1]
                    time_visitante = linhas[2]
                    placar = None
                elif len(linhas) >= 6:
                    time_casa = linhas[1]
                    gols_casa = linhas[2]
                    gols_visitante = linhas[3]
                    time_visitante = linhas[4]
                    placar = f"{gols_casa} x {gols_visitante}"
                else:
                    print(f"{idx + 1}. Formato inesperado (linhas insuficientes):", linhas)
                    continue

                jogos_disponiveis.append({
                    "time_casa": time_casa,
                    "time_visitante": time_visitante,
                    "local": local,
                    "data": data,
                    "dia": dia,
                    "hora": hora,
                    "placar": placar
                })

                texto_extra = f" - Placar: {placar}" if placar else ""
                print(f"{idx + 1}. {time_casa} x {time_visitante} - {data} {hora} ({local}){texto_extra}")
            else:
                print(f"{idx + 1}. Erro ao ler local/data/hora: {linha0}")
        else:
            print(f"{idx + 1}. Formato inesperado:", linhas)

# Menu principal
def exibir_menu():
    print("\n======= MENU PRINCIPAL =======")
    print("1 - Mostrar tabela")
    print("2 - Estatísticas do time")
    print("3 - Jogos da rodada")
    print("4 - Sair")

def main():
    navegador = iniciar_navegador()
    abrir_tabela_brasileirao(navegador)
    tabela_classificacao = extrair_tabela(navegador)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            mostrar_tabela(tabela_classificacao)
        elif opcao == '2':
            estatisticas_time(tabela_classificacao)
        elif opcao == '3':
            listar_jogos(navegador, tabela_classificacao)
        elif opcao == '4':
            print("Saindo do programa...")
            navegador.quit()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
