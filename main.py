from PIL import Image
import numpy as np

def image_to_ascii(image_path, output_width=100, charset="@%#*+=-:. "):
    """
    Конвертирует изображение в ASCII-арт
    
    :param image_path: путь к изображению
    :param output_width: ширина выходного ASCII-арта (в символах)
    :param charset: набор символов для градаций яркости (от темного к светлому)
    :return: строка с ASCII-артом
    """
    
    # Открываем изображение и конвертируем в grayscale
    img = Image.open(image_path).convert('L')
    
    # Вычисляем высоту, сохраняя пропорции
    width, height = img.size
    aspect_ratio = height / width
    output_height = int(output_width * aspect_ratio * 0.55) # 0.55 - поправка на пропорции символов
    
    # масштабируем изображение
    img = img.resize((output_width, output_height))
    
    # конвертируем в numpy массив
    pixels = np.array(img)
    
    # Нормализуем пиксели к индексам charset
    pixels = (pixels / 255 * (len(charset) - 1)).astype(int)
    
    # СОбираем ASCII-арт
    ascii_art = []
    for row in pixels:
        ascii_art.append("".join([charset[pixel] for pixel in row]))
    
    return "\n".join(ascii_art)

if __name__ == "__main__":
    ascii_art = image_to_ascii("your_image.jpg", output_width=100)
    print(ascii_art)
    input()