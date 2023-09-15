
# Processamento de Imagens em Lote com Interface Gráfica

Este é um utilitário em Python para processar imagens em lote usando a biblioteca OpenCV, TQDM (para barras de progresso)
e uma interface gráfica simples criada com customtkinter. O programa pode processar imagens de entrada, 
aplicando uma série de transformações para detectar plantas e remover o solo das imagens.

## Funcionalidades Principais

- Processamento de imagens de entrada em lote.
- Processamento da pasta EXEMPLOS do desafio.
- Interface gráfica simples para facilitar o uso.
- Suporte para o modo de depuração (debug mode) para visualizar máscaras de processamento.
- Opção para mostrar a pasta de saída após o processamento.

## Configuração

Antes de usar o programa, você pode configurar as seguintes constantes no código-fonte:

- `PASTA_ENTRADA`: O caminho para a pasta que contém as imagens de entrada a serem processadas.
- `PASTA_EXEMPLOS`: O caminho para a pasta que contém exemplos de imagens.
- `PASTA_SAIDA`: O caminho para a pasta onde as imagens segmentadas serão salvas.
- `PASTA_EXEMPLOS_SAIDA`: O caminho para a pasta onde as imagens de exemplos processadas serão salvas.
- `DEBUG_MODE`: Define se o modo de depuração está ativado ou desativado (True ou False).
- `MOSTRAR_PASTA_SAIDA`: Define se a pasta de saída deve ser aberta automaticamente após o processamento (True ou False).
- `NUM_PROCESSADORES`: O número de processadores a serem usados para o processamento em paralelo. Automaticamente usa 75% do total.

## Uso

**Primeiro, instale os requisitos:**
- ```bash
  pip install requirements.txt
  ```

Você pode usar o programa de diferentes maneiras:

1. **Interface Gráfica:** Execute o programa sem argumentos para iniciar a interface gráfica, onde você pode interagir com botões para processar imagens de entrada e exemplos, ativar o modo de depuração e mostrar a pasta de saída.
- ```bash
  python destacar_plantas.py
  ```

2. **Modo de Linha de Comando:** Você pode usar o programa no modo de linha de comando para processar imagens de entrada e exemplos sem a interface gráfica. Use os seguintes comandos:

- Para processar imagens de entrada:
  ```bash
  python destacar_plantas.py processar_imagens
  ```

- Para processar exemplos:
  ```bash
  python destacar_plantas.py processar_exemplos
  ```

3. **Modo de Depuração:** Você pode ativar o modo de depuração adicionando `--debug` como argumento ao iniciar o programa. Isso exibirá máscaras de processamento durante o processamento das imagens.
   ```bash
   python destacar_plantas.py --debug
   ```

Lembre-se de personalizar os caminhos das pastas de entrada e saída de acordo com suas necessidades.

## Requisitos

Certifique-se de ter as seguintes bibliotecas Python instaladas:

- OpenCV
- TQDM
- customtkinter (se necessário, pode ser substituído por tkinter padrão)


## Conclusão
Tentei alguns algorítimos:
- tentei treinar um modelo próprio (mas pelo dataset pequeno, não consegui)
- tentei achar as plantas por seus formatos (pontas)
- tentei umas bibliotecas do scitlearn mas não consegui muita coisa.

**Mas o melhor de todos, e o mais rápido, preciso e simples, foi utilizando o opencv-python (cv2)**

Nenhum outro algorítimo foi tão rápido e preciso quanto este meu último:
```text
Remove o solo da imagem usando a técnica de selecionar pixels verdes.
    Possui fallbacks (modos automáticos) para detectar plantas em diversos ambientes e com luminosidade diferentes.
    Passos:
    1. Aumenta a nitidez usando o método Canny.
    2. Encontra segmentos usando detecção de cores.
    3. Dilata a máscara para aumentar o tamanho dos contornos.
    4. Aplica fechamento morfológico para preencher buracos.
    5. Mescla a máscara dilatada à imagem original para obter a imagem segmentada.
    6. Cria uma máscara RGB a partir da máscara em escala de cinza
```

E ainda por cima, fiz uma função que faz a PROVA REAL das imagens. Como assim?
1. Pega as imagens da pasta EXEMPLO (onde o lado esquerdo é a original, e o direito como o meu algoritimo deveria deixar)
2. Separa o lado esquerdo, passa o algorítimo por ele e salva uma nova imagem na pasta "exemplo_outputs", mesclando a imagem de exemplo dada, com a minha imagem processada.
3. Assim, sendo possível comparar de perto como meu algorítimo se saiu próximo do de vocês!


Espero que esteja no padrão de vocês. Eu adorei fazer este desafio pra Cromai! :)

Foi um ótimo experimento pra testar minhas capacidades, e eu creio, que eu tenha conseguido cumprir o desafio quase perfeitamente!


## Autor

- Pedro Gabriel Ganzo

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.
