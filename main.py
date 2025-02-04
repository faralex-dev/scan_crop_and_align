import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import os
from PIL import Image

def align_and_trim_image(image_path, threshold=25, max_angle=15):
    # Открытие изображения с помощью Pillow
    image = Image.open(image_path)

    # Если изображение в формате RGBA, конвертируем его в RGB
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Конвертация изображения в массив numpy
    image_array = np.array(image)

    # Конвертация изображения в оттенки серого
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # Пороговое значение для определения темных пикселей
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Нахождение контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Находим наибольший контур
    max_contour = max(contours, key=cv2.contourArea)

    # Выравнивание изображения
    rect = cv2.minAreaRect(max_contour)
    angle = rect[2]
    if angle < -45:
        angle += 90

    # Ограничение угла выравнивания
    if abs(angle) > max_angle:
        angle = angle - 90

    # Центрирование и поворот изображения
    center = (image_array.shape[1] // 2, image_array.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    aligned = cv2.warpAffine(image_array, rotation_matrix, (image_array.shape[1], image_array.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Конвертация выровненного изображения в оттенки серого
    gray_aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)

    # Пороговое значение для определения темных пикселей на выровненном изображении
    _, binary_aligned = cv2.threshold(gray_aligned, threshold, 255, cv2.THRESH_BINARY)

    # Нахождение контуров на выровненном изображении
    contours_aligned, _ = cv2.findContours(binary_aligned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Находим наибольший контур на выровненном изображении
    max_contour_aligned = max(contours_aligned, key=cv2.contourArea)

    # Получаем прямоугольник, охватывающий наибольший контур
    x, y, w, h = cv2.boundingRect(max_contour_aligned)

    # Обрезка выровненного изображения по найденным границам
    trimmed = aligned[y:y + h, x:x + w]

    return trimmed

def save_image(image, save_path):
    image_pil = Image.fromarray(image)
    image_pil.save(save_path, 'PNG')

def process_folder(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        print('Загружено файлов: ' + str(len(files)))
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                file_path = os.path.join(root, file)
                try:
                    image = align_and_trim_image(file_path)
                    relative_path = os.path.relpath(root, input_folder)
                    save_dir = os.path.join(output_folder, relative_path)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    save_path = os.path.join(save_dir, os.path.splitext(file)[0] + ".png")
                    save_image(image, save_path)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при обработке файла {file_path}: {e}")
                    print("Ошибка", f"Ошибка при обработке файла {file_path}: {e}")
    messagebox.showinfo("Готово", "Темные границы успешно обрезаны, изображение выровнено!")

def browse_folder():
    input_folder = filedialog.askdirectory(initialdir="/", title="Выбрать папку с изображениями")
    if input_folder:
        save_folder = filedialog.askdirectory(initialdir="/", title="Выбрать папку для сохранения")
        if save_folder:
            process_folder(input_folder, save_folder)

if __name__ == '__main__':
    # Создание главного окна
    root = tk.Tk()
    root.title("Обрезка темных границ и выравнивание изображения")

    # Метка с названием программы
    label = tk.Label(root, text="Обрезка темных границ и выравнивание изображения", font=("Helvetica", 16))
    label.pack(pady=10)

    # Кнопка для выбора папки с изображениями
    browse_button = tk.Button(root, text="Выбрать папку с изображениями", command=browse_folder)
    browse_button.pack(pady=10)

    # Запуск основного цикла приложения
    root.mainloop()
