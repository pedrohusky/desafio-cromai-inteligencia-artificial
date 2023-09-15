import shutil
import os
import concurrent.futures
import customtkinter as ttk
from tqdm import tqdm

from remover_solo import processar_imagem, processar_imagem_exemplo

# Defina algumas constantes para melhor legibilidade e manutenção

# O caminho da pasta de entrada com imagens a serem processadas
PASTA_ENTRADA = "./case_segmentacao/inputs"
PASTA_EXEMPLOS = "./case_segmentacao/exemplos"

# O caminho da pasta de saída onde as imagens segmentadas serão salvas
PASTA_SAIDA = "outputs"
PASTA_EXEMPLOS_SAIDA = "exemplos_outputs"

# Variáveis globais para controle do modo de debug e mostrar pasta de saída
DEBUG_MODE = False
MOSTRAR_PASTA_SAIDA = True

# Número de processadores a serem usados (75% dos processadores disponíveis)
NUM_PROCESSADORES = max(1, int(0.75 * os.cpu_count()))


def criar_pasta_saida(pasta_saida):
    """Crie a pasta de saída se ela não existir ou limpe-a se existir.

    :param pasta_saida: O caminho da pasta de saída.
    """
    if os.path.exists(pasta_saida):
        shutil.rmtree(pasta_saida)
    os.makedirs(pasta_saida, exist_ok=True)


def processar_imagem_arquivo(nome_arquivo):
    caminho_imagem_entrada = os.path.join(PASTA_ENTRADA, nome_arquivo)
    processar_imagem(caminho_imagem_entrada, debug=DEBUG_MODE)


def processar_imagem_exemplo_arquivo(nome_arquivo):
    caminho_imagem_exemplo = os.path.join(PASTA_EXEMPLOS, nome_arquivo)
    processar_imagem_exemplo(caminho_imagem_exemplo, debug=DEBUG_MODE)


def processar_imagens_entrada():
    """
    Processa as imagens de entrada na pasta especificada por PASTA_ENTRADA.
    """
    criar_pasta_saida(PASTA_SAIDA)
    arquivos_imagem = [arquivo_imagem for arquivo_imagem in os.listdir(PASTA_ENTRADA)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_PROCESSADORES) as executor:
        list(tqdm(executor.map(processar_imagem_arquivo, arquivos_imagem), total=len(arquivos_imagem)))
    if MOSTRAR_PASTA_SAIDA:
        abrir_pasta_saida()


def processar_exemplos():
    """
    Processa os exemplos na pasta especificada por PASTA_EXEMPLOS.
    """
    criar_pasta_saida(PASTA_EXEMPLOS_SAIDA)
    arquivos_exemplo = [arquivo_imagem for arquivo_imagem in os.listdir(PASTA_EXEMPLOS)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_PROCESSADORES) as executor:
        list(tqdm(executor.map(processar_imagem_exemplo_arquivo, arquivos_exemplo), total=len(arquivos_exemplo)))
    if MOSTRAR_PASTA_SAIDA:
        abrir_pasta_saida(PASTA_EXEMPLOS_SAIDA)


def abrir_pasta_saida(pasta=PASTA_SAIDA):
    """
    Abre a pasta de saída no explorador de arquivos.

    :param pasta: O caminho da pasta a ser aberta.
    """
    os.system(f"start {pasta}")


def criar_interface():
    """
    Cria a interface gráfica utilizando o tkinter.
    """
    # Crie uma janela principal
    janela_principal = ttk.CTk()
    janela_principal.title("Removedor de Solo - v1.0")
    ttk.set_appearance_mode("System")
    ttk.set_default_color_theme("blue")

    def processar_com_debug_interface():
        global DEBUG_MODE
        DEBUG_MODE = debug_var.get()

    def processar_com_mostrar_pasta_saida_interface():
        global MOSTRAR_PASTA_SAIDA
        MOSTRAR_PASTA_SAIDA = mostrar_pasta_saida_var.get()

    # Crie um frame principal
    frame_principal = ttk.CTkFrame(janela_principal)
    frame_principal.pack(pady=10, padx=10)

    # Crie um botão para processar as imagens de entrada
    botao_processar = ttk.CTkButton(frame_principal, text="Processar Imagens de Entrada",
                                    command=processar_imagens_entrada)
    botao_processar.pack(pady=10, padx=10)

    # Crie um botão para processar os exemplos
    botao_processar_exemplos = ttk.CTkButton(frame_principal, text="Processar Exemplos (Tirar prova Final)",
                                             command=processar_exemplos)
    botao_processar_exemplos.pack(pady=10, padx=10)

    # Crie um botão para abrir a pasta de saída
    botao_abrir_pasta_saida = ttk.CTkButton(frame_principal, text="Abrir Pasta de Saída", command=abrir_pasta_saida)
    botao_abrir_pasta_saida.pack(pady=10, padx=10)

    # Crie um checkbox para ativar o modo de debug
    debug_var = ttk.BooleanVar()
    checkbox_debug = ttk.CTkCheckBox(frame_principal, text="Modo de Debug (máscaras para debug)", variable=debug_var,
                                     command=processar_com_debug_interface)
    checkbox_debug.pack(pady=10, padx=10)

    # Crie um checkbox para mostrar a pasta de saída após o processamento
    mostrar_pasta_saida_var = ttk.BooleanVar(value=True)
    checkbox_mostrar_pasta_saida = ttk.CTkCheckBox(frame_principal, text="Mostrar Pasta de Saída ao Concluir",
                                                   variable=mostrar_pasta_saida_var,
                                                   command=processar_com_mostrar_pasta_saida_interface)
    checkbox_mostrar_pasta_saida.pack(pady=10, padx=10)

    # Inicie a interface gráfica
    janela_principal.mainloop()


if __name__ == "__main__":
    import sys

    # Aceita comandos pelo CMD, ou simplesmente iniciando destacar_plantas.py

    if "--debug" in sys.argv:
        DEBUG_MODE = True
        sys.argv.remove("--debug")

    if len(sys.argv) > 1:
        if sys.argv[1] == "processar_imagens":
            processar_imagens_entrada()
        elif sys.argv[1] == "processar_exemplos":
            processar_exemplos()
        elif sys.argv[1] == "interface":
            criar_interface()
    else:
        criar_interface()
