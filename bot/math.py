from turtledemo.rosette import mn_eck
import matplotlib
matplotlib.use('Agg')  # Используем бэкенд без GUI
import matplotlib.pyplot as plt
import telebot
from telebot import types
import json
import os
import shutil
import math
from io import BytesIO
import numpy as np
from .defs import *


# Median_Arithmetic_Mean

class Median:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot
        # self.data = arr
        # self.median_value = np.median(self.data)

    def calculations(self, message):
        dict_js = get_response_json(json_name="user_states", json_key=message.chat.id)
        self.data = dict_js["numbers"]
        self.median_value = np.median(self.data)
        # mean_value = np.mean(self.data)  # Среднее арифметическое

        dict_js["tipe"] = "Median"
        dict_js["states"] = "Computation"
        dict_js["Median"] = self.median_value
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=dict_js)

        answer = get_response_json("speech_patterns", "math")["median"].format(median=self.median_value)
        self.bot.send_message(message.chat.id, answer, parse_mode="HTML")




    def create_graf(self,message, title='График с медианой', xlabel='Индекс', ylabel='Значение'):
        """
        Создает график из массива данных

        Parameters:
        - data: массив данных
        - plot_type: тип графика ('line', 'bar', 'scatter')
        - title: заголовок графика
        - xlabel: подпись оси X
        - ylabel: подпись оси Y
        """
        dict_js = get_response_json(json_name="user_states", json_key=message.chat.id)
        self.data = dict_js["numbers"]
        self.median_value = dict_js["Median"]
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=None)

        mn = min(self.data)
        mx = max(self.data)
        ln = len(self.data)

        # Определяем ширину (X) на основе количества точек
        if ln > 500:
            X = 16  # Для очень больших наборов данных
        elif ln > 200:
            X = 14  # Для больших наборов данных
        elif ln > 50:
            X = 12  # Для средних наборов
        elif ln > 20:
            X = 10  # Стандартный размер
        elif ln > 10:
            X = 8  # Для маленьких наборов
        else:
            X = 6  # Для очень маленьких наборов

        # Определяем высоту (Y) на основе диапазона данных
        data_range = mx - mn

        if data_range > 10000:
            Y = 14  # Для очень больших диапазонов
        elif data_range > 1000:
            Y = 12  # Для больших диапазонов
        elif data_range > 100:
            Y = 10  # Для средних диапазонов
        elif data_range > 10:
            Y = 8  # Стандартная высота
        elif data_range > 1:
            Y = 6  # Для маленьких диапазонов
        else:
            Y = 5  # Для очень маленьких диапазонов

        # Корректируем для очень маленьких наборов данных
        if ln <= 5:
            X = max(X, 6)  # Минимальная ширина для читаемости

        plt.figure(figsize=(X, Y))

        # Строим основной график данных
        x = np.arange(len(self.data))
        plt.plot(x, self.data, 'b-', linewidth=2, marker='o', markersize=4, alpha=0.7, label='Данные')

        # Добавляем красную полосу медианы
        plt.axhline(y=self.median_value, color='red', linewidth=3, alpha=0.8,
                    label=f'Медиана: {self.median_value:.2f}')

        # Заливаем область вокруг медианы для лучшей видимости
        plt.axhspan(self.median_value * 0.99, self.median_value * 1.01, alpha=0.2, color='red')

        # Настраиваем внешний вид
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best')

        # # Добавляем аннотацию с значением медианы
        # plt.annotate(f'Медиана: {self.median_value:.2f}',
        #              xy=(len(self.data) * 0.7, self.median_value),
        #              xytext=(len(self.data) * 0.5, self.median_value + (max(self.data) - min(self.data)) * 0.1),
        #              arrowprops=dict(facecolor='red', shrink=0.05, alpha=0.7),
        #              fontsize=12,
        #              bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

        # Сохраняем в буфер
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        try:
            self.bot.send_photo(message.chat.id, buffer, caption="Вот ваш график!")

        except Exception as e:
            self.bot.reply_to(message, f"Ошибка при создании графика: {e}")



class ArithmeticMean:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def calculations(self, message):
        dict_js = get_response_json(json_name="user_states", json_key=message.chat.id)
        self.data = dict_js["numbers"]
        # self.median_value = np.median(self.data)
        self.mean_value = np.mean(self.data)  # Среднее арифметическое

        dict_js["tipe"] = "ArithmeticMean"
        dict_js["states"] = "Computation"
        dict_js["Mean"] = self.mean_value
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=dict_js)

        answer = get_response_json("speech_patterns", "math")["arithmetic_mean"].format(arithmetic_mean=self.mean_value)
        self.bot.send_message(message.chat.id, answer, parse_mode="HTML")

    def create_graf(self, message, title='График с медианой', xlabel='Индекс', ylabel='Значение'):
        """
        Создает график из массива данных

        Parameters:
        - data: массив данных
        - plot_type: тип графика ('line', 'bar', 'scatter')
        - title: заголовок графика
        - xlabel: подпись оси X
        - ylabel: подпись оси Y
        """
        dict_js = get_response_json(json_name="user_states", json_key=message.chat.id)
        self.data = dict_js["numbers"]
        self.mean_value = dict_js["Mean"]  # Среднее арифметическое
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=None)

        mn = min(self.data)
        mx = max(self.data)
        ln = len(self.data)

        # Определяем ширину (X) на основе количества точек
        if ln > 500:
            X = 16  # Для очень больших наборов данных
        elif ln > 200:
            X = 14  # Для больших наборов данных
        elif ln > 50:
            X = 12  # Для средних наборов
        elif ln > 20:
            X = 10  # Стандартный размер
        elif ln > 10:
            X = 8  # Для маленьких наборов
        else:
            X = 6  # Для очень маленьких наборов

        # Определяем высоту (Y) на основе диапазона данных
        data_range = mx - mn

        if data_range > 10000:
            Y = 14  # Для очень больших диапазонов
        elif data_range > 1000:
            Y = 12  # Для больших диапазонов
        elif data_range > 100:
            Y = 10  # Для средних диапазонов
        elif data_range > 10:
            Y = 8  # Стандартная высота
        elif data_range > 1:
            Y = 6  # Для маленьких диапазонов
        else:
            Y = 5  # Для очень маленьких диапазонов

        # Корректируем для очень маленьких наборов данных
        if ln <= 5:
            X = max(X, 6)  # Минимальная ширина для читаемости

        plt.figure(figsize=(X, Y))

        # Строим основной график данных
        x = np.arange(len(self.data))
        plt.plot(x, self.data, 'b-', linewidth=2, marker='o', markersize=4, alpha=0.7, label='Данные')

        # Добавляем зеленую полосу среднего арифметического
        plt.axhline(y=self.mean_value, color='green', linewidth=3, alpha=0.8,
                    label=f'Среднее: {self.mean_value:.2f}')

        # Заливаем область вокруг среднего арифметического для лучшей видимости
        plt.axhspan(self.mean_value * 0.99, self.mean_value * 1.01, alpha=0.2, color='green')

        # Настраиваем внешний вид
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best')

        # # Добавляем аннотацию с значением медианы
        # plt.annotate(f'Среднее Арифметическое: {self.mean_value:.2f}',
        #              xy=(len(self.data) * 0.7, self.mean_value),
        #              xytext=(len(self.data) * 0.5, self.mean_value + (max(self.data) - min(self.data)) * 0.1),
        #              arrowprops=dict(facecolor='red', shrink=0.05, alpha=0.7),
        #              fontsize=12,
        #              bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

        # Сохраняем в буфер
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        try:
            self.bot.send_photo(message.chat.id, buffer, caption="Вот ваш график!")

        except Exception as e:
            self.bot.reply_to(message, f"Ошибка при создании графика: {e}")


class MedianAndArithmeticMean:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def calculations(self, message):
        dict_js = get_response_json(json_name="user_states", json_key=message.chat.id)
        self.data = dict_js["numbers"]
        self.median_value = np.median(self.data)
        self.mean_value = np.mean(self.data)  # Среднее арифметическое

        dict_js["tipe"] = "MedianAndArithmeticMea"
        dict_js["states"] = "Computation"
        dict_js["Median"] = self.median_value
        dict_js["Mean"] = self.mean_value
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=dict_js)

        answer = get_response_json("speech_patterns", "math")["together_mean_median"].format(median=self.median_value, arithmetic_mean=self.mean_value)
        self.bot.send_message(message.chat.id, answer, parse_mode="HTML")

    def create_graf(self, message, title='График с медианой', xlabel='Индекс', ylabel='Значение'):
        """
        Создает график из массива данных

        Parameters:
        - data: массив данных
        - plot_type: тип графика ('line', 'bar', 'scatter')
        - title: заголовок графика
        - xlabel: подпись оси X
        - ylabel: подпись оси Y
        """

        dict_js = get_response_json(json_name="user_states", json_key=message.chat.id)
        self.data = dict_js["numbers"]
        self.median_value = dict_js["Median"]
        self.mean_value = dict_js["Mean"]  # Среднее арифметическое
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=None)

        mn = min(self.data)
        mx = max(self.data)
        ln = len(self.data)

        # Определяем ширину (X) на основе количества точек
        if ln > 500:
            X = 16  # Для очень больших наборов данных
        elif ln > 200:
            X = 14  # Для больших наборов данных
        elif ln > 50:
            X = 12  # Для средних наборов
        elif ln > 20:
            X = 10  # Стандартный размер
        elif ln > 10:
            X = 8  # Для маленьких наборов
        else:
            X = 6  # Для очень маленьких наборов

        # Определяем высоту (Y) на основе диапазона данных
        data_range = mx - mn

        if data_range > 10000:
            Y = 14  # Для очень больших диапазонов
        elif data_range > 1000:
            Y = 12  # Для больших диапазонов
        elif data_range > 100:
            Y = 10  # Для средних диапазонов
        elif data_range > 10:
            Y = 8  # Стандартная высота
        elif data_range > 1:
            Y = 6  # Для маленьких диапазонов
        else:
            Y = 5  # Для очень маленьких диапазонов

        # Корректируем для очень маленьких наборов данных
        if ln <= 5:
            X = max(X, 6)  # Минимальная ширина для читаемости

        plt.figure(figsize=(X, Y))

        # Строим основной график данных
        x = np.arange(len(self.data))
        plt.plot(x, self.data, 'b-', linewidth=2, marker='o', markersize=4, alpha=0.7, label='Данные')

        # Добавляем красную полосу медианы
        plt.axhline(y=self.median_value, color='red', linewidth=3, alpha=0.8,
                    label=f'Медиана: {self.median_value:.2f}')

        # Заливаем область вокруг медианы для лучшей видимости
        plt.axhspan(self.median_value * 0.99, self.median_value * 1.01, alpha=0.2, color='red')

        # Добавляем зеленую полосу среднего арифметического
        plt.axhline(y=self.mean_value, color='green', linewidth=3, alpha=0.8,
                    label=f'Среднее: {self.mean_value:.2f}')

        # Заливаем область вокруг среднего арифметического для лучшей видимости
        plt.axhspan(self.mean_value * 0.99, self.mean_value * 1.01, alpha=0.2, color='green')


        # Настраиваем внешний вид
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best')

        # # Добавляем аннотацию с значением медианы
        # plt.annotate(f'Медиана: {self.median_value:.2f}',
        #              xy=(len(self.data) * 0.7, self.median_value),
        #              xytext=(len(self.data) * 0.5, self.median_value + (max(self.data) - min(self.data)) * 0.1),
        #              arrowprops=dict(facecolor='red', shrink=0.05, alpha=0.7),
        #              fontsize=10,
        #              bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
        #
        # # Добавляем аннотацию с значением среднего
        # plt.annotate(f'Среднее: {self.mean_value:.2f}',
        #              xy=(len(self.data) * 0.7, self.mean_value),
        #              xytext=(len(self.data) * 0.5, self.mean_value - (max(self.data) - min(self.data)) * 0.1),
        #              arrowprops=dict(facecolor='green', shrink=0.05, alpha=0.7),
        #              fontsize=10,
        #              bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))

        # Сохраняем в буфер
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        try:
            self.bot.send_photo(message.chat.id, buffer, caption="Вот ваш график!")

        except Exception as e:
            self.bot.reply_to(message, f"Ошибка при создании графика: {e}")
