# Image Alignment and Cropping Tool

Этот инструмент позволяет автоматически выравнивать и обрезать сканированные изображения, удаляя темные границы и корректируя угол наклона. Программа обрабатывает изображения в папке и сохраняет результаты в указанную директорию.

## 🛠️ Функциональность
- **Выравнивание изображений**: автоматическое определение угла наклона и поворот изображения для выравнивания.
- **Обрезка темных границ**: удаление ненужных темных областей по краям изображения.
- **Пакетная обработка**: поддержка обработки всех изображений в выбранной папке.
- **Сохранение в PNG**: результаты сохраняются в формате PNG для сохранения качества.

## 🚀 Как использовать
1. Запустите программу.
2. Нажмите кнопку **"Выбрать папку с изображениями"** и укажите папку с изображениями для обработки.
3. Выберите папку для сохранения обработанных изображений.
4. Дождитесь завершения обработки. Программа уведомит вас о завершении.

## 📦 Зависимости
Для работы программы необходимы следующие библиотеки:
- `opencv-python` (`cv2`)
- `Pillow` (`PIL`)
- `numpy`
- `tkinter` (входит в стандартную библиотеку Python)

Установите зависимости с помощью команды:
```bash
pip install opencv-python pillow numpy
```

## 📂 Поддерживаемые форматы
Программа поддерживает изображения в форматах:
- PNG
- JPEG/JPG
- BMP
- GIF


## 📄 Лицензия
Этот проект распространяется под лицензией MIT.
