from PIL import Image
import numpy as np
from pathlib import Path

def image_to_ascii(
    image_path: str,
    output_width: int = 100,
    charset: str = "@%#*+=-:. ",
    contrast: float = 1.0,
    brightness: float = 1.0
) -> str:
    """
    Конвертирует изображение в ASCII-арт.
    
    :param image_path: путь к изображению.
    :param output_width: ширина выходного ASCII-арта (в символах).
    :param charset: набор символов для градаций яркости (от темного к светлому).
    :param contrast: Коэффициент контрастности (по умолчанию 1.0).
    :param brightness: Коэффициент яркости (по умолчанию 1.0).
    :return: строка с ASCII-артом.
    :raises FileNotFoundError: Если файл изображения не найден.
    :raises ValueError: Если charset пуст или параметры некорректны.
    """
    if not Path(image_path).exists():
        raise FileNotFoundError(f'Файл "{image_path}" не найден.')
    
    if not charset:
        raise ValueError("Charset не может быть пустым.")
    
    if contrast <= 0 or brightness <= 0:
        raise ValueError("Контрастность и яркость должны быть положительными числами.")
    
    try:
        img = Image.open(image_path).convert('L')
    except Exception as e:
        raise ValueError(f"Ошибка при открытии изображения: {e}")
    
    width, height = img.size
    aspect_ratio = height / width
    output_height = int(output_width * aspect_ratio * 0.55) # 0.55 - поправка на пропорции символов
    
    img = img.resize((output_width, output_height))
    pixels = np.array(img)
    
    pixels = np.clip((pixels - 128) * contrast + 128 * brightness, 0, 255)
    
    pixels = (pixels / 255 * (len(charset) - 1)).astype(int)
    
    ascii_art = "\n".join(
        "".join(charset[pixel] for pixel in row)
        for row in pixels
    )
    
    return ascii_art

if __name__ == "__main__":
    try:
        image_path = input(r'Введите путь к изображению (например, D:\1.jpg): ')
        output_width = int(input('Введите ширину ASCII-арта (например, 100): '))
        charset = input('Введите кодировку от темного к светлому (например, @%#*+=-:. )')
        ascii_art = image_to_ascii(image_path, output_width, charset)
        print(ascii_art)
    except Exception as e:
        print(f"Ошибка: {e}")
    input("Нажмите Enter для выхода...")