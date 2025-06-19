import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.chrome.options import Options

# Selenium original

def iniciar_navegador():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")
    navegador = webdriver.Chrome(options=options)
    navegador.maximize_window()
    navegador.get('https://google.com.br')
    return navegador

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
    campos = ["pontos", "jogos", "vitórias", "empates", "derrotas", "gols_pro", "gols_contra", "saldo_de_gols", "aproveitamento"]
    tabela_classificacao = {}
    if len(clubes) == len(linhasEstatisticas):
        for clube, estatistica in zip(clubes, linhasEstatisticas):
            valores = estatistica.text.split()
            dados_clube = {campo: valor for campo, valor in zip(campos, valores)}
            tabela_classificacao[clube.text] = dados_clube
    return tabela_classificacao

def listar_jogos(navegador):
    jogos = navegador.find_elements(By.CSS_SELECTOR, ".lista-jogos__jogo")
    jogos_disponiveis = []

    for jogo in jogos:
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
                elif n:
                    local = n.group(1).strip()[:-4]
                    data, dia, hora = "Hoje", n.group(2) or "", n.group(3)

                if len(linhas) == 3:
                    time_casa, time_visitante, placar = linhas[1], linhas[2], None
                elif len(linhas) >= 6:
                    time_casa, gols_casa, gols_visitante, time_visitante = linhas[1], linhas[2], linhas[3], linhas[4]
                    placar = f"{gols_casa} x {gols_visitante}"
                else:
                    continue

                jogos_disponiveis.append(f"{time_casa} x {time_visitante} - {data or dia} {hora} ({local})" + (f" - Placar: {placar}" if placar else ""))
    return jogos_disponiveis

def get_goleadores(navegador):
    goleadores = navegador.find_elements(By.CSS_SELECTOR, ".ranking-item-wrapper")
    lista = []
    for goleador in goleadores[:10]:
        nome = goleador.find_element(By.CSS_SELECTOR, ".jogador-nome").text
        gols = goleador.find_element(By.CSS_SELECTOR, ".jogador-gols").text
        posicao = goleador.find_element(By.CSS_SELECTOR, ".jogador-posicao").text
        imagem = goleador.find_element(By.CSS_SELECTOR, ".jogador-escudo img")
        time = imagem.get_attribute("alt")
        lista.append(f"{nome} ({posicao}) - {gols} gols - {time}")
    return lista

# GUI Tkinter

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Brasileirão 2025")
        self.root.geometry("800x600")

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 10))
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.btn1 = tk.Button(btn_frame, text="1 - Mostrar Tabela", command=self.mostrar_tabela)
        self.btn1.pack(side=tk.LEFT, padx=5)

        self.btn2 = tk.Button(btn_frame, text="2 - Estatísticas Time", command=self.estatisticas_time)
        self.btn2.pack(side=tk.LEFT, padx=5)

        self.btn3 = tk.Button(btn_frame, text="3 - Jogos da Rodada", command=self.jogos_rodada)
        self.btn3.pack(side=tk.LEFT, padx=5)

        self.btn4 = tk.Button(btn_frame, text="4 - Artilheiros", command=self.artilheiros)
        self.btn4.pack(side=tk.LEFT, padx=5)

        self.btn5 = tk.Button(btn_frame, text="5 - Sair", command=self.encerrar)
        self.btn5.pack(side=tk.LEFT, padx=5)

        self.navegador = iniciar_navegador()
        abrir_tabela_brasileirao(self.navegador)
        self.tabela = extrair_tabela(self.navegador)

    def mostrar_tabela(self):
        self.output.delete(1.0, tk.END)
        cabecalho = f"{'Clube':<25} {'P':>3} {'J':>3} {'V':>3} {'E':>3} {'D':>3} {'GP':>4} {'GC':>4} {'SG':>4} {'AP':>5}"
        self.output.insert(tk.END, cabecalho + "\n" + "-" * len(cabecalho) + "\n")
        for clube, stats in self.tabela.items():
            linha = f"{clube:<25} {stats['pontos']:>3} {stats['jogos']:>3} {stats['vitórias']:>3} {stats['empates']:>3} {stats['derrotas']:>3} {stats['gols_pro']:>4} {stats['gols_contra']:>4} {stats['saldo_de_gols']:>4} {stats['aproveitamento']:>4}%"
            self.output.insert(tk.END, linha + "\n")

    def estatisticas_time(self):
        self.output.delete(1.0, tk.END)
        nomes = list(self.tabela.keys())
        escolha = tk.simpledialog.askinteger("Escolha", f"Digite o número do time:\n" + "\n".join([f"{i+1}. {nome}" for i, nome in enumerate(nomes)]))
        if escolha and 1 <= escolha <= len(nomes):
            clube = nomes[escolha - 1]
            stats = self.tabela[clube]
            msg = (
                f"{clube} disputou {stats['jogos']} jogos.\n"
                f"Vitórias: {stats['vitórias']} | Empates: {stats['empates']} | Derrotas: {stats['derrotas']}\n"
                f"Gols pró: {stats['gols_pro']} | Contra: {stats['gols_contra']} | SG: {stats['saldo_de_gols']}\n"
                f"Aproveitamento: {stats['aproveitamento']}%\n"
            )
            self.output.insert(tk.END, msg)
        else:
            messagebox.showerror("Erro", "Número inválido.")

    def jogos_rodada(self):
        self.output.delete(1.0, tk.END)
        jogos = listar_jogos(self.navegador)
        for j in jogos:
            self.output.insert(tk.END, j + "\n")

    def artilheiros(self):
        self.output.delete(1.0, tk.END)
        artilheiros = get_goleadores(self.navegador)
        for a in artilheiros:
            self.output.insert(tk.END, a + "\n")

    def encerrar(self):
        self.navegador.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
