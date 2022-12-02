import sys
import numpy as np
import cv2
import os
import face_recognition
from datetime import datetime

haar_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # Загрузка каскадного классификатора

org_date = (430, 475)  # Координаты нижнего левого угла даты
font_date = cv2.FONT_HERSHEY_SIMPLEX  # Шрифт даты
font_scale_date = 0.5  # Коэффициент масштабирования шрифта даты
color_date = (255, 255, 255)  # Цвет шрифа даты
thickness_date = 1  # Толщина линни в пикселях даты
line_type_date = cv2.LINE_AA  # Тип линии шрифта

start_point_rectangle = (10, 10)  # Начальные координаты прямоугольника
end_point_rectangle = (630, 470)  # Конечные координаты прямоугольника
color_rectangle = (0, 0, 0)  # Цвет шрифа прямоугольника
thickness_rectangle = 22  # Толщина линни в пикселях прямоугольника

text_rec = "Rec"
org_text_rec = (558, 15)  # Координаты нижнего левого угла Rec
font_text_rec = cv2.FONT_HERSHEY_SIMPLEX  # Шрифт Rec
font_scale_text_rec = 0.5  # Коэффициент масштабирования шрифта Rec
color_text_rec = (0, 0, 255)  # Цвет шрифа Rec
thickness_text_rec = 1  # Толщина линни в пикселях Rec
line_type_text_rec = cv2.LINE_AA  # Тип линии Rec

center_coordinates_circle_rec = (550, 10)  # Центр круга Rec
radius_circle_rec = 6  # Радиус круга Rec
color_circle_rec = (0, 0, 255)  # Цвет круга Rec
thickness_circle_rec = -1  # Толщина линии границы круга Rec

capture = cv2.VideoCapture(0)  # Захват видеопотока с web камеры

filename_out = 'output.avi'  # Имя выходного видеофайла
fps_out = 8  # Частота кадров выходного видеопотока
frame_size_out = (640, 480)  # Разрешение выходного потока
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Кодек записи
out = cv2.VideoWriter(filename_out, fourcc, fps_out, frame_size_out)  # Объект записи видео


def find_encoding(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

images = []
class_name = []
path = 'db/identify'
mylist = os.listdir(path)
for cls in mylist:
    cur_img = cv2.imread(f'{path}/{cls}')
    images.append(cur_img)
    class_name.append(os.path.splitext(cls)[0])
encode_list_know = find_encoding(images)




def face_control(img, count):
    scale_factor = 1.1  # коэфицент увеличения размера окна поиска на каждой итерации
    min_neighbords = 6  # размер окна
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bgra_ing = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    bgra_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = haar_face_cascade.detectMultiScale(gray_img, scale_factor, min_neighbords)  # Поиск всех лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #f = cv2.resize(gray_img[y:y + h, x:x + w], (200, 200))  # Создание кадра для идентицикатора
    face_cur_frame = face_recognition.face_locations(bgra_img)
    encode_cur_frame = face_recognition.face_encodings(bgra_img, face_cur_frame)
    for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
        mathces = face_recognition.compare_faces(encode_list_know, encode_face)
        face_dis = face_recognition.face_distance(encode_list_know, encode_face)
        match_index = np.argmin(face_dis)
        if mathces[match_index]:
            name = class_name[match_index]
            print(name)
    return img, count


kol = 0  # Костыль для мигания кружочка индикации записи видеопотока
count = 0  # Нумерация файлов идентификации одного человека
while True:
    ret, img = capture.read()
    date_time = str(datetime.now())
    date_time = date_time[0:19]  # Время без миллисекунд
    # img = cv2.rectangle(img, start_point_rectangle, end_point_rectangle, color_rectangle,
    #                    thickness_rectangle)  # Добавление прямоугольника на изображение
    img = cv2.putText(img, date_time, org_date, font_date, font_scale_date, color_date,
                      thickness_date, line_type_date)  # Добавление даты на изображение
    img = cv2.putText(img, text_rec, org_text_rec, font_text_rec, font_scale_text_rec, color_text_rec,
                      thickness_text_rec, line_type_text_rec)  # Добавление надписи Rec на изображение
    if kol % 12 == 0:
        img = cv2.circle(img, center_coordinates_circle_rec, radius_circle_rec,
                         color_circle_rec, thickness_circle_rec)  # Кружок для индикации записи видеопотока
        kol = 0
    kol += 1
    img, count = face_control(img, count)  # Распознование лиц
    out.write(img)  # Запись
    cv2.imshow("From Camera", img)  # Отображение изображения

    k = cv2.waitKey(30)  # Считывания клавишы Esc для прекращения трансляции изображения
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
