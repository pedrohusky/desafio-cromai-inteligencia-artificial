import os
import cv2
import numpy as np
from keras.applications import MobileNetV2
from keras.layers import Conv2DTranspose
from keras.models import Model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Carregar e pré-processar os dados
input_dir = "./case_segmentacao/exemplos"  # Pasta com as imagens originais de drone
output_dir = "./outputs"  # Pasta onde você salvará as imagens segmentadas

# Carregar nomes de arquivos de entrada
input_files = os.listdir(input_dir)

# Inicializar listas para os conjuntos de treinamento e validação
X_train = []
y_train = []  # Renomeado para y_train para indicar que são os alvos reais

# Carregar imagens de entrada (exemplos)
for file in input_files:
    image = cv2.imread(os.path.join(input_dir, file))
    # Dividir a imagem ao meio (esquerda e direita)
    width = image.shape[1] // 2
    left_half = image[:, :width, :]  # Metade esquerda (entrada)
    right_half = image[:, width:, :]  # Metade direita (saída)

    # Pré-processamento das metades
    left_half = cv2.resize(left_half, (224, 224))  # Redimensionar para o tamanho esperado
    left_half = left_half / 255.0  # Normalizar
    right_half = cv2.resize(right_half, (224, 224))  # Redimensionar para o tamanho esperado
    right_half = right_half / 255.0  # Normalizar

    X_train.append(left_half)
    y_train.append(right_half)  # Adicionar as imagens redimensionadas como alvos reais

# Converter para arrays numpy
X_train = np.array(X_train)
y_train = np.array(y_train)

# Dividir os dados em treinamento e validação
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Carregar modelo pré-treinado MobileNetV2
base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False)

# Adicionar camadas de saída personalizadas para segmentação
x = base_model.layers[-1].output
x = Conv2DTranspose(3, (3, 3), activation='sigmoid', padding='same')(x)  # Alterado para 3 canais de saída

# Criar modelo de segmentação
model = Model(inputs=base_model.input, outputs=x)

# Compilar o modelo
model.compile(optimizer=Adam(lr=0.001), loss='mse', metrics=['accuracy'])  # Usando 'mse' para saída de imagem

# Treinar o modelo usando as imagens de treinamento e os alvos reais redimensionados
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=16)

# Salvar o modelo treinado
model.save('modelo_de_segmentacao.h5')

# Usar o modelo para segmentar novas imagens
new_images = [...]  # Carregue e pré-processe as novas imagens
segmented_images = model.predict(new_images)

# Salvar as imagens segmentadas
for i, seg_img in enumerate(segmented_images):
    cv2.imwrite(os.path.join(output_dir, f'segmented_{i}.png'), (seg_img * 255).astype(np.uint8))
