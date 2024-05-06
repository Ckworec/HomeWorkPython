import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import ndimage
import numpy as np
from PIL import Image
import multiprocessing as mp
import datetime

# Manipulate channels

def get_greyscale_image(img):
    return np.mean(img[:,:,:2], 2)

# Transformations

def scale_image(input_file, output_file, scale):
    try:
        img = Image.open(input_file)
        width, height = img.size
        new_width = width * scale
        new_height = height * scale
        new_img = Image.new('RGB',(new_width, new_height))

        for k in range(new_width):
            for l in range(new_height):
                i = k // scale
                j = l // scale
                pixel_sum = [0,0,0]
                for x in range(2):
                    for y in range(2):
                        if i + x < width and j + y < height:
                            pixel = img.getpixel((i + x, j + y))
                            pixel_sum[0] += pixel[0]
                            pixel_sum[1] += pixel[1]
                            pixel_sum[2] += pixel[2]
                pixel_avg=(pixel_sum[0] // 4, pixel_sum[1] // 4, pixel_sum[2] // 4)
                new_img.putpixel((k, l), pixel_avg)
        new_img.save(output_file)
    except Exception as e:
        print(f"An error occurred: {e}")

# Функция для перехода от блоков 8 на 8 к блокам 4 на 4
def reduce(img, factor):
    result = np.zeros((img.shape[0] // factor, img.shape[1] // factor))
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = np.mean(img[i * factor:(i + 1) * factor,j * factor:(j + 1) * factor])

    return result

def rotate(img, angle):
    return ndimage.rotate(img, angle, reshape = False)

def flip(img, direction): # Отражает изображение зеркально, если direction равно -1 и не отражает, если значение равно 1
    return img[::direction,:]

def apply_transformation(img, direction, angle, contrast = 1.0, brightness = 0.0): # сжимающее отображение
    return contrast * rotate(flip(img, direction), angle) + brightness

# Contrast and brightness

# Подбираем подходящие яркость и контрастность методом наименьших квадратов https://colab.research.google.com/drive/1MhWrDx0RsNrt4DWsk583Xb-CAm6z27s8?usp=sharing
def find_contrast_and_brightness2(D, S):
    A = np.concatenate((np.ones((S.size, 1)), np.reshape(S, (S.size, 1))), axis = 1) # Объединение массивов вдоль оси
    b = np.reshape(D, (D.size,))
    x, _, _, _ = np.linalg.lstsq(A, b, rcond=None) # Решение матричного уравнения методом наименьших квадратов

    return x[1], x[0]

# Compress / decompress

def generate_all_transformed_blocks(img, source_size_block, destination_size_block, step):
    factor = source_size_block // destination_size_block
    transformed_blocks = []
    for k in range((img.shape[0] - source_size_block) // step + 1):
        for l in range((img.shape[1] - source_size_block) // step + 1):
            # Преобразуем исходный блок в конечный (доменный -> ранговый)
            S = reduce(img[k * step:k * step + source_size_block,l * step:l * step + source_size_block], factor)
            # Всевозможные преобразования при помощи найшего сжимающего изображения
            for direction, angle in candidates:
                transformed_blocks.append((k, l, direction, angle, apply_transformation(S, direction, angle)))
    
    return transformed_blocks

def compress(img, source_size_block, destination_size_block, step, transformations, transformations_no_fratal, number):
    transformations = []
    transformations_no_fratal = []
    transformed_blocks = generate_all_transformed_blocks(img, source_size_block, destination_size_block, step) # Генерируем всевозможные преобразования
    i_count = img.shape[0] // destination_size_block
    j_count = img.shape[1] // destination_size_block
    for i in range(i_count):
        transformations.append([])
        transformations_no_fratal.append([])
        for j in range(j_count):
            transformations[i].append(None)
            transformations_no_fratal[i].append(None)
            min_d = float('inf')
            # Берем доменный блок
            D = img[i * destination_size_block:(i + 1) * destination_size_block,j * destination_size_block:(j + 1) * destination_size_block]
            # Выбираем самый похожий блок
            for k, l, direction, angle, S in transformed_blocks:
                contrast, brightness = find_contrast_and_brightness2(D, S)
                S = contrast * S + brightness
                d = np.sum(np.square(D - S)) # Сумма квадратов D - S (типа square это поэлементый квадрат)
                # Ищем самый похожий блок
                if d < min_d:
                    min_d = d
                    transformations[i][j] = (k, l, direction, angle, contrast, brightness)
                    transformations_no_fratal[i][j] = S
    
    np.save('save_data_{}'.format(number), transformations_no_fratal)
    np.save('save_data_fractal_{}'.format(number), transformations)
    
    return transformations

def decompress(transformations, source_size_block, destination_size_block, step, nb_iter):
    factor = source_size_block // destination_size_block
    height = len(transformations) * destination_size_block
    width = len(transformations[0]) * destination_size_block
    iterations = [np.random.randint(0, 256, (height, width))]
    cur_img = np.zeros((height, width))
    for i_iter in range(nb_iter):
        for i in range(len(transformations)):
            for j in range(len(transformations[i])):
                # Применяем отображение
                k, l, flip, angle, contrast, brightness = transformations[i][j]
                k = int(k)
                l = int(l)
                flip = int(flip)
                S = reduce(iterations[-1][k * step:k * step + source_size_block,l * step:l * step + source_size_block], factor)
                D = apply_transformation(S, flip, angle, contrast, brightness)
                cur_img[i * destination_size_block:(i + 1) * destination_size_block,j * destination_size_block:(j + 1) * destination_size_block] = D
        iterations.append(cur_img)
        cur_img = np.zeros((height, width))
    
    return iterations

def decompress_ultra_mega_sposob(transformations, source_size_block, destination_size_block):
    height = len(transformations) * destination_size_block
    width = len(transformations[0]) * destination_size_block
    cur_img = np.zeros((height, width))

    for i in range(len(transformations)):
            for j in range(len(transformations[i])):
                cur_img[i * destination_size_block:(i + 1) * destination_size_block,j * destination_size_block:(j + 1) * destination_size_block] = transformations[i][j]
    
    return cur_img
  
# Parameters

directions = [1, -1]
angles = [0, 90, 180, 270] # Для сохранения формы изображения угол может принимать только такие значения
candidates = [[direction, angle] for direction in directions for angle in angles]
number = 0
number1 = 0
size_block_r = 4 # размер блока в который перейдет
size_block_d = 8 # размер блока который переходит
step = size_block_d
nb_iter = 50 # сколько раз применится отображение

if __name__ == '__main__':
    print( "Commands: \n 1. Compress image \n 2. Decompress image from fractal \n 3. Decompress image from mega ultra sposob \n 0. Exit \n\n Enter command: ", end = '')

    command = int(input())

    while command != 0:
        if command == 1:
            print(" Enter name of image: ", end = '')
            img_name = input()

            print("\n How do you want to compress the image:\n 1. Maximum compression with severe quality loss\n 2. Maximum preservation of image quality with a large investment of time\n 3. Optimal choice of coefficients\n")

            command = int(input("Enter command: "))

            img = mpimg.imread(img_name)

            if command == 1:
                size_block_d = 10
                size_block_r = 5
                step = size_block_d
                skip_transformation = 0
            elif command == 2:
                size_block_d = 4
                size_block_r = 2
                step = size_block_d
                skip_transformation = 10
            elif command == 3:
                if img.shape[0] > 500 or img.shape[1] > 500:
                    size_block_d = 8
                    size_block_r = 4
                    step = size_block_d
                    skip_transformation = 50
                else:
                    size_block_d = 6
                    size_block_r = 3
                    step = size_block_d
                    skip_transformation = 0

            img = get_greyscale_image(img)
            img = reduce(img, size_block_r)
            number = img_name[-5]

            i_count = img.shape[0] // size_block_r
            j_count = img.shape[1] // size_block_r
            transformations = []
            transformations_no_fractal = []
            for i in range(i_count):
                transformations.append([])
                transformations_no_fractal.append([])
                for j in range(j_count):
                    transformations[i].append([])
                    transformations_no_fractal[i].append([])

            start = datetime.datetime.now()
            p = mp.Process(target=compress, args=(img, size_block_d, size_block_r, step, transformations, transformations_no_fractal, number))
            p.start()
            p.join()
            end = datetime.datetime.now()

            print(" Time compression: ", end - start)

            print("\n")

        elif command == 2:
            print(" Enter number file with compressed cofficient: ", end = '')
            file_name = 'save_data_fractal_' + input() + '.npy'
            transform = np.load(file_name)

            number1 = file_name[-5]
            
            iterations = decompress(transform, size_block_d, size_block_r, step, nb_iter)
            plt.imsave('result_{}.bmp'.format(number1), iterations[nb_iter - 1], cmap='gray')
            scale_image('result_{}.bmp'.format(number1), 'result_{}.bmp'.format(number1), size_block_r)

            print("\n")

        elif command == 3:
            print(" Enter number file with compressed cofficient: ", end = '')
            file_name = 'save_data_' + input() + '.npy'
            transform = np.load(file_name)

            number1 = file_name[-5]

            iterations = decompress_ultra_mega_sposob(transform, size_block_d, size_block_r)
            plt.imsave('result_ultra_mega_sposob_{}.bmp'.format(number1), iterations, cmap='gray')
            scale_image('result_ultra_mega_sposob_{}.bmp'.format(number1), 'result_ultra_mega_sposob_{}.bmp'.format(number1), size_block_r)

            print("\n")

        print(" Enter command: ", end = '')
        command = int(input())
