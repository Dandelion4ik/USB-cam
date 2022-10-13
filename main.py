import sys

import cv2
import os
# import face_recognition as fr
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
fps_out = 6  # Частота кадров выходного видеопотока
frame_size_out = (640, 480)  # Разрешение выходного потока
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Кодек записи
out = cv2.VideoWriter(filename_out, fourcc, fps_out, frame_size_out)  # Объект записи видео

count = 0


def face_control(img, count=count):
    scale_factor = 1.1  # коэфицент увеличения размера окна поиска на каждой итерации
    min_neighbords = 6  # размер окна
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray_img, scale_factor, min_neighbords)  # Поиск всех лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        f = cv2.resize(gray_img[y:y + h, x:x + w], (200, 200))  # Создание кадра для идентицикатора
        cv2.imwrite('jm1/%s.pgm' % str(count), f)  # Запись этого кадра
        count += 1  # Итерация для записываемых кадров
    return img


kol = 0  # Костыль для мигания кружочка индикации записи видеопотока
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
    img = face_control(img)  # Распознование лиц
    out.write(img)
    cv2.imshow("From Camera", img)  # Отображение изображения

    k = cv2.waitKey(30)  # Считывания клавишы Esc для прекращения трансляции изображения
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
