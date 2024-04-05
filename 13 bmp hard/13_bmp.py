import numpy as np
from skimage import io, util, measure
import matplotlib.pyplot as plt
from PIL import Image 

"""
tolerance - означает допустимое отклонение при сравнении блоков изображения в процессе сжатия и декомпрессии. 
Значение tolerance определяет, насколько похожи блоки должны быть, 
чтобы считаться одинаковыми и заменяться друг другом в процессе сжатия и декомпрессии. 
Уменьшение значения tolerance приведет к более точному сжатию изображения, 
но может увеличить размер результирующего файла. Увеличение значения tolerance, 
наоборот, может уменьшить размер результирующего файла, 
но может привести к некоторой потере качества изображения.
"""

def fractal_compress(image, tolerance):
    # Сконвертировать изображение в черно-белое
    image_gray = util.img_as_float(image)
    if len(image_gray.shape) > 2:
        image_gray = util.img_as_float(image_gray[:,:,0])

    # Получить количество блоков и их размер
    block_size = 4
    width, height = image_gray.shape
    num_blocks = (width // block_size) * (height // block_size)

    # Разбить изображение на блоки
    blocks = image_gray[:width - width % block_size, :height - height % block_size].reshape(width // block_size, height // block_size, block_size, block_size)

    # Найти среднее значение каждого блока
    # Заполняем массив нулями
    block_means = np.zeros((width // block_size, height // block_size))

    for i in range(width // block_size):
        for j in range(height // block_size):
            block_means[i, j] = np.mean(blocks[i, j]) # Среднее арифметическое блока

    # Найти наиболее схожие блоки
    similar_blocks = np.zeros((width // block_size, height // block_size), dtype = object) # Узнать что такое object

    for i in range(width // block_size):
        for j in range(height // block_size):
            block_diff = np.abs(block_means - block_means[i, j]) # Поэлементное взятие модуля
            similar_blocks[i, j] = np.argwhere(block_diff <= tolerance).tolist()

    compressed_image = np.zeros_like(image_gray)

    for i in range(width // block_size):
        for j in range(height // block_size):
            block_indices = similar_blocks[i, j]
            for index in block_indices:
                x, y = index
                compressed_image[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size] = blocks[x, y]

    return compressed_image

def fractal_decompress(compressed_image, original_image, tolerance):
    # Декомпрессия изображения
    compressed_image_gray = util.img_as_float(compressed_image)
    if len(compressed_image_gray.shape) > 2:
        compressed_image_gray = util.img_as_float(compressed_image_gray[:,:,0])

    original_image_gray = util.img_as_float(original_image)

    if len(original_image_gray.shape) > 2:
        original_image_gray = util.img_as_float(original_image_gray[:,:,0])

    compressed_image = np.zeros_like(original_image_gray)
    block_size = 4
    width, height = compressed_image_gray.shape

    for i in range(0, width, block_size):
        for j in range(0, height, block_size):
            block = compressed_image_gray[i:i + block_size, j:j + block_size]
            diff = np.abs(original_image_gray[i:i + block_size, j:j + block_size] - block)
            if np.mean(diff) <= tolerance:
                compressed_image[i:i + block_size, j:j + block_size] = block
            else:
                compressed_image[i:i + block_size, j:j + block_size] = original_image_gray[i:i + block_size, j:j + block_size]

    return compressed_image

# Загрузить изображение
image = io.imread('input.bmp')

# Сжать изображение
compressed_image = fractal_compress(image, tolerance = 0.2)

# Восстановить изображение
reconstructed_image = fractal_decompress(compressed_image, image, tolerance = 0.2)

# Отобразить изображения
io.imshow(image)

io.imshow(compressed_image)
plt.imsave('compress.bmp', compressed_image, cmap='gray')

io.imshow(reconstructed_image)
plt.imsave('result.bmp', reconstructed_image, cmap='gray')
