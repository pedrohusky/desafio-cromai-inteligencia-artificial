import os
import cv2
import numpy as np

# Caminhos
PASTA_SAIDA = "outputs"
PASTA_EXEMPLOS_SAIDA = "exemplos_outputs"

# O limite inferior para cores verdes no formato HSV
LIMITE_INFERIOR_VERDE = np.array([19, 61, 35])  # Ajuste o valor de matiz para verde

# O limite superior para cores verdes no formato HSV
LIMITE_SUPERIOR_VERDE = np.array([90, 255, 255])  # Ajuste o valor de matiz para verde

# A cor de fundo a ser usada para a imagem segmentada no formato BGR
COR_FUNDO = [0, 0, 0]

# Número mínimo de objetos detectados na segmentação verde para alternar para cores de reserva
MIN_OBJETOS_VERDE = 300
MAX_OBJETOS_VERDE = 230

# Este fallback só ocorre se o número de objetos verdes detectados for < MIN_OBJETOS_VERDE
LIMITE_INFERIOR_RESERVA = np.array([11, 60, 35])
LIMITE_SUPERIOR_RESERVA = np.array([90, 255, 255])


def dilatar_contornos(mascara, tamanho_dilatacao=0):
    """
    Dilata os contornos na imagem de máscara fornecida usando um tamanho de kernel especificado.

    :param mascara: A imagem de máscara.
    :param tamanho_dilatacao: O tamanho do kernel usado para a dilatação. O padrão é 5.
    :return: ndarray: A imagem de máscara dilatada.
    """
    kernel = np.ones((tamanho_dilatacao, tamanho_dilatacao), np.uint8)
    mascara_dilatada = cv2.dilate(mascara, kernel, iterations=1)
    return mascara_dilatada


def fechar_buracos(mascara, shape=(5, 5)):
    """
    Fecha buracos na imagem de máscara.

    :param mascara: A imagem de máscara a ser fechada.
    :param shape: O tamanho do kernel. Padrão: (5, 5).
    :return:
        A imagem de máscara fechada.
    """
    kernel = np.ones(shape, np.uint8)
    mascara_segmentada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    return mascara_segmentada


def encontrar_objetos(mascara):
    """
    Encontre componentes conectados na máscara e retorne o número de objetos.

    :param mascara: A imagem de entrada.

    :return:
        Etiquetas e estatísticas (objetos).
    """
    _, etiquetas, estatisticas, _ = cv2.connectedComponentsWithStats(mascara, connectivity=8)
    return etiquetas, estatisticas


def encontrar_cores(imagem, limite_superior_cor, limite_inferior_cor):
    """
    Encontra os objetos com base nos limites de cor especificados no espaço de cores HSV.

    :param imagem: A imagem de entrada.
    :param limite_superior_cor: O limite de cor superior no espaço de cores HSV.
    :param limite_inferior_cor: O limite de cor inferior no espaço de cores HSV.

    :return:
        A máscara, etiquetas e estatísticas dos objetos encontrados.
    """
    mascara = cv2.inRange(imagem, limite_inferior_cor, limite_superior_cor)
    etiquetas, estatisticas = encontrar_objetos(mascara)
    return mascara, etiquetas, estatisticas


def encontrar_segmentos(imagem, limite_superior_cor, limite_inferior_cor, nome_arquivo=""):
    """
    Dada uma imagem, limites de cor superior e inferior e um nome de arquivo, esta função encontra segmentos na imagem com base nos limites de cor especificados.

    :param imagem: A imagem de entrada.
    :param limite_superior_cor: O limite de cor superior no espaço de cores HSV.
    :param limite_inferior_cor: O limite de cor inferior no espaço de cores HSV.
    :param nome_arquivo: O nome do arquivo (para exibição de informações).

    :return:
        A máscara segmentada e a imagem HSV.
    """
    imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    mascara, _, primeira_estatistica = encontrar_cores(imagem_hsv, limite_superior_cor, limite_inferior_cor)
    #print(f"Encontrados {len(primeira_estatistica)} objetos verdes em {nome_arquivo} na primeira verificação")

    if 310 >= len(primeira_estatistica) - 1 >= 100 or len(
            primeira_estatistica) - 1 <= 50:
        mascara, _, segunda_estatistica = encontrar_cores(imagem_hsv, LIMITE_SUPERIOR_RESERVA,
                                                          LIMITE_INFERIOR_RESERVA)
        #print(f"Encontrados {len(segunda_estatistica)} objetos em {nome_arquivo} usando fallback.")

        if len(segunda_estatistica) - 1 >= 2000:
            mascara, _, segunda_estatistica = encontrar_cores(imagem_hsv, np.array([90, 255, 255]),
                                                              np.array([19, 25, 35]))
            #print(f"Encontrados {len(segunda_estatistica)} objetos em {nome_arquivo} usando o segundo fallback.")

    if len(primeira_estatistica) - 1 >= 2000:
        mascara, _, segunda_estatistica = encontrar_cores(imagem_hsv, np.array([90, 255, 255]),
                                                          np.array([25, 35, 35]))
        #print(f"Encontrados {len(segunda_estatistica)} objetos em {nome_arquivo} usando o terceiro fallback.")

        if len(segunda_estatistica) - 1 >= 3500:
            mascara, _, primeira_estatistica = encontrar_cores(imagem_hsv, limite_superior_cor,
                                                               limite_inferior_cor)
            #print(f"Encontrados mais que 2000 objetos em {nome_arquivo}. Retornado para a máscara inicial.")

    return mascara, imagem_hsv


def aumentar_nitidez(imagem):
    """
    Aumenta a nitidez da imagem aplicando detecção de bordas usando o algoritmo Canny.

    :param imagem: A imagem de entrada.

    :return:
        A imagem com nitidez aumentada.
    """
    # Aplicar deteção de bordas Canny
    bordas = cv2.Canny(imagem, threshold1=100, threshold2=200)  # Ajuste os limites conforme necessário

    # Crie a imagem segmentada aplicando as bordas como máscara
    imagem_segmentada = imagem.copy()
    imagem_segmentada[bordas != 0] = COR_FUNDO

    return imagem_segmentada


def gerar_nome_e_caminho(arquivo, pasta_saida):
    """
    Gera um nome para a imagem e o caminho de saída usando o nome do prórprio arquivo
    :param arquivo: Caminho completo da imagem
    :param pasta_saida: O nome da pasta de saída
    :return:
    """
    nome_arquivo = os.path.basename(arquivo)
    caminho_imagem_saida = os.path.join(pasta_saida, nome_arquivo)
    return nome_arquivo, caminho_imagem_saida


def converter_mascara_para_rgb(mascara):
    """
    Converte a máscara para RGB para ser possível adicioná-la ao resultado estacado.
    :param mascara: A máscara a ser convertida
    :return:
    """
    # Crie uma máscara RGB a partir da máscara em escala de cinza
    mascara_rgb = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    return mascara_rgb


def adicionar_borda_verde(imagem, espessura_borda):
    """
    Adiciona uma borda verde a uma imagem.
    :param imagem: A imagem à qual adicionar a borda.
    :param espessura_borda: A espessura da borda em pixels.
    :return: A imagem com a borda adicionada.
    """
    altura, largura, _ = imagem.shape

    # Crie uma nova imagem com a borda
    imagem_com_borda = np.copy(imagem)

    # Defina a cor da borda para verde (em BGR)
    cor_verde = (0, 255, 0)

    # Adicione a borda à imagem
    cv2.rectangle(imagem_com_borda, (0, 0), (largura - 1, altura - 1), cor_verde, espessura_borda)

    return imagem_com_borda


def estacar_imagens(original, hsv, mascara_rgb, imagem_segmentada, caminho_imagem_saida, debug):
    """
    Estaca imagens lado-a-lado.
    :param original: A imagem original.
    :param hsv: A imagem com filtro hsv.
    :param mascara_rgb: A máscara da imagem hsv.
    :param imagem_segmentada: A imagem final
    :param caminho_imagem_saida: Caminho para salvar as imagens
    :return:
    """

    if debug:
        # Salve a imagem segmentada
        imagem_resultado = np.hstack(
            (original, hsv, mascara_rgb, adicionar_borda_verde(imagem_segmentada, 2)))  # Concatene lado a lado
        cv2.imwrite(caminho_imagem_saida, imagem_resultado)
    else:
        # Salve a imagem segmentada
        imagem_resultado = np.hstack((original, imagem_segmentada))  # Concatene lado a lado
        cv2.imwrite(caminho_imagem_saida, imagem_resultado)


def remover_solo(imagem, nome_arquivo):
    """
    Remove o solo da imagem usando a técnica de selecionar pixels verdes.\n
    Possui fallbacks (modos) para detectar plantas em diversos ambientes e com luminosidade diferentes.\n
    Passos:\n
    1. Aumenta a nitidez usando o méteodo Canny.\n
    2. Encontra segmentos usando detecção de cores.\n
    3. Dilata a máscara para aumentar o tamanho dos contornos.\n
    4. Aplica fechamento morfológico para preencher buracos.\n
    5. Mescla a máscara dilatada à imagem original para obter a imagem segmentada.
    6. Crie uma máscara RGB a partir da máscara em escala de cinza
    :param imagem:
    :param nome_arquivo:
    :return: mascara_rgb, hsv, imagem_segmentada
    """
    # Chama a função para segmentar imagens usando detecção de bordas
    imagem_afiada = aumentar_nitidez(imagem)

    mascara, hsv = encontrar_segmentos(imagem_afiada, LIMITE_SUPERIOR_VERDE, LIMITE_INFERIOR_VERDE,
                                       nome_arquivo)

    # Dilata a máscara para aumentar o tamanho dos contornos
    mascara = dilatar_contornos(mascara)

    # Aplica fechamento morfológico para preencher buracos
    mascara = fechar_buracos(mascara)

    # Mescla a máscara dilatada à imagem original para obter a imagem segmentada
    imagem_segmentada = imagem.copy()
    imagem_segmentada[mascara == 0] = COR_FUNDO

    # Crie uma máscara RGB a partir da máscara em escala de cinza
    mascara_rgb = converter_mascara_para_rgb(mascara)
    return mascara_rgb, hsv, imagem_segmentada


def processar_imagem(arquivo, debug=False):
    """
    Processar uma única imagem e a salva no caminho de saída definido em PASTA_SAIDA.

    :param debug: Padrão é falso.
    :param arquivo: O caminho da imagem de entrada.
    """

    # Carregar a imagem de entrada
    imagem = cv2.imread(arquivo)

    nome_arquivo, caminho_imagem_saida = gerar_nome_e_caminho(arquivo, PASTA_SAIDA)

    mascara_rgb, hsv, imagem_segmentada = remover_solo(imagem, nome_arquivo)

    # Salve a imagem segmentada
    estacar_imagens(imagem, hsv, mascara_rgb, imagem_segmentada, caminho_imagem_saida, debug)


def processar_imagem_exemplo(arquivo, debug=False):
    """
        Processa imagens originais na pasta exemplos (apenas o lado esquerdo). Termina gerando uma pasta "exemplos_outputs"
        com as imagens geradas lado a lado com as imagens originais.\n
        Estrutura das imagens geradas:
            LADO ESQUERDO: original, \n
            MEIO: como deveria ser, \n
            LADO DIREITO: como o algorítimo fez.
        """
    # Carregar e pré-processar os dados
    imagem = cv2.imread(arquivo)
    # Dividir a imagem ao meio (esquerda e direita)
    largura = imagem.shape[1] // 2
    metade_esquerda = imagem[:, :largura, :]  # Metade esquerda (entrada)

    nome_arquivo, caminho_imagem_saida = gerar_nome_e_caminho(arquivo, PASTA_EXEMPLOS_SAIDA)

    mascara_rgb, hsv, imagem_segmentada = remover_solo(metade_esquerda, nome_arquivo)

    # Salve a imagem segmentada
    estacar_imagens(imagem, hsv, mascara_rgb, imagem_segmentada, caminho_imagem_saida, debug)
