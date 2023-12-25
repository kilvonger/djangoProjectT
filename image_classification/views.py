import os
from django.conf import settings
from tensorflow.keras.preprocessing import image
from django.shortcuts import render
import numpy as np
from keras.models import load_model
import shutil


def index(request):
    return render(request,'headerPage.html')

def predict(request):
    return render(request,'upload_image.html')

def predict_image(request):
    # Путь к сохраненной модели
    model_path = './models/image_recognition_model.h5'

    # Загрузка модели
    model = load_model(model_path)

    input_shape = (150, 150, 3)

    # Словарь с метками классов
    class_labels = {0: 'Мяч для американского футбола', 1: 'Бейсбольный мяч', 2: 'Мяч для баскетбола', 3: 'бильярдный шар', 4: 'Шар для боулинга', 5: 'Мяч для игры в крикет', 6: 'Футбольный мяч', 7: 'Шар для гольфа', 8: 'Шар для настольного тенниса', 9: 'Шар для тенниса', 10: 'Волейбольный мяч'}

    # Проверка метода запроса
    if request.method == 'POST':
        # Получение загруженного изображения из запроса
        uploaded_image = request.FILES.get('image')

        # Создание временного пути для сохранения файла
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp.jpg')

        # Сохранение файла на диск
        with open(temp_path, 'wb') as file:
            for chunk in uploaded_image.chunks():
                file.write(chunk)

        # Загрузка изображения и его предобработка для использования в модели
        img = image.load_img(temp_path, target_size=(input_shape[0], input_shape[1]))
        img_array = image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        img_preprocessed = img_batch / 255.0

        # Предсказание класса изображения
        prediction = model.predict(img_preprocessed)
        predicted_class_index = np.argmax(prediction)
        predicted_class_label = class_labels[predicted_class_index]

        # Сохранение изображения в папке media
        media_path = os.path.join(settings.MEDIA_ROOT, 'predicted_image.jpg')
        shutil.move(temp_path, media_path)

        return render(request, 'upload_image.html', {'predicted_class_label': predicted_class_label, 'predicted_image_path': '/media/predicted_image.jpg'})

    return render(request, 'upload_image.html')
