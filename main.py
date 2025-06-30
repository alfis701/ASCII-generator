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
        # Конвертирует изображение в оттенки серого ('L' - luminance)
        img = Image.open(image_path).convert('L')
    except Exception as e:
        raise ValueError(f"Ошибка при открытии изображения: {e}")
    
    width, height = img.size
    # Рассчитывает высоту ASCII-арта с учетом пропорций изображения и соотношения высоты/ширины символов
    aspect_ratio = height / width
    CHAR_HEIGHT_TO_WIDTH_RATIO = 0.55  # Эмпирическое соотношение высоты/ширины символа в консоли
    output_height = int(output_width * aspect_ratio * CHAR_HEIGHT_TO_WIDTH_RATIO)
    
    # Изменяет размер изображения до нужных размеров ASCII-арта
    img = img.resize((output_width, output_height))
    
    # Преобразует изображение в numpy массив для обработки
    pixels = np.array(img)
    
    # Применяет контраст и яркость:
    # 1. Сначала центрирует значения вокруг 128 (вычитает 128)
    # 2. Умножает на коэффициент контраста (растягивает/сжимает диапазон)
    # 3. Добавляет 128 * brightness (сдвигает среднюю яркость)
    # 4. Ограничивает значения в диапазоне 0-255 с помощью np.clip
    pixels = np.clip((pixels - 128) * contrast + 128 * brightness, 0, 255)
    
    # Нормализует значения пикселей к индексам charset (от 0 до len(charset) - 1)
    pixels = (pixels / 255 * (len(charset) - 1)).astype(int)
    
    # Собирает ASCII-арт: ля каждого пикселя выбирает соответствующий символ из charset
    # и объединяет строки через символ новой строки
    ascii_art = "\n".join(
        "".join(charset[pixel] for pixel in row)
        for row in pixels
    )
    
    img.close()
    return ascii_art

if __name__ == "__main__":
    try:
        image_path = input(r'Введите путь к изображению (например, D:\1.jpg): ')
        custom_settings = int(input('Настроить самому (1) или настройка по умолчанию (0)?'))
        settings = {}
        
        if custom_settings not in (0, 1):
            raise ValueError('Введите 0 или 1.')
        
        # Запрашивает у пользователя настройки, если выбран режим кастомизации
        if custom_settings == 1:
            settings['output_width'] = int(input('Введите ширину ASCII-арта (например, 100): '))
            settings['charset'] = input('Введите кодировку от темного к светлому (например, @%#*+=-:. )')
            settings['contrast'] = float(input('Настройте контраст (например, 1.0)'))
            settings['brightness'] = float(input('Настройте яркость (например, 1.0)'))
            
            
        ascii_art = image_to_ascii(image_path, **settings)
        print(ascii_art)
    except KeyboardInterrupt:
        # Ловит аварийную ошибку, если нажать Ctrl + C
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Ошибка: {e}")
    input("Нажмите Enter для выхода...")
