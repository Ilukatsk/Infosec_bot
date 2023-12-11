from aiogram import types
import logging

def main_keyboard():
    kb = [
        [types.KeyboardButton(text="Получить мудрый совет по ИБ")],
        [types.KeyboardButton(text="Что сегодня за день?"),
        types.KeyboardButton(text="ИБ-вендора")],
        [types.KeyboardButton(text="Типы средств защиты"),
        types.KeyboardButton(text="Дать обратную связь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
    
def single_button_keyboard(txt):
    kb = [
        [types.KeyboardButton(text=txt)]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

def companies_list_keyboard(page_num):
    if page_num == 0:
        kb = [
            [types.InlineKeyboardButton(text="Вперед", callback_data="page_up")]
        ]
    elif page_num == 7:
        kb = [
            [types.InlineKeyboardButton(text="Назад", callback_data="page_down")]
        ]
    else:
        kb = [
            [types.InlineKeyboardButton(text="Назад", callback_data="page_down"),
            types.InlineKeyboardButton(text="Вперед", callback_data="page_up")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard