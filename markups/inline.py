import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
from database import *


def menus_kb(page_idx):
    builder = InlineKeyboardBuilder()
    menus = Menu.get_all(is_active=True)
    if not menus:
        builder.row(InlineKeyboardButton(text="➕Add menu", callback_data="add_menu"))
        builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
        return builder.as_markup()
    page_size = 5
    pages = [menus[i:i + page_size] for i in range(0, len(menus), page_size)]
    page = pages[page_idx]
    for menu in page:
        menu: Menu
        builder.row(InlineKeyboardButton(text=menu.name,
                                         callback_data=f"view_menu {menu.menu_id}"))
    if len(pages) > 1:
        if page_idx == len(pages) - 1:
            back = InlineKeyboardButton(text=f"◀️Back", callback_data=f"menus_page {page_idx - 1}")
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            builder.row(back, page_of)
        elif page_idx > 0:
            back = InlineKeyboardButton(text=f"◀️Back", callback_data=f"menus_page {page_idx - 1}")
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            forward = InlineKeyboardButton(text=f"▶️Forward", callback_data=f"menus_page {page_idx + 1}")
            builder.row(back, page_of, forward)
        elif page_idx == 0:
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            forward = InlineKeyboardButton(text=f"▶️Forward", callback_data=f"menus_page {page_idx + 1}")
            builder.row(page_of, forward)
    builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
    return builder.as_markup()


def meals_kb(page_idx):
    builder = InlineKeyboardBuilder()
    meals = Meal.get_all(is_active=True)
    if not meals:
        builder.row(InlineKeyboardButton(text="➕Add meal", callback_data="add_meal"))
        builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
        return builder.as_markup()
    page_size = 5
    pages = [meals[i:i + page_size] for i in range(0, len(meals), page_size)]
    page = pages[page_idx]
    for meal in page:
        meal: Meal
        builder.row(InlineKeyboardButton(text=meal.name,
                                         callback_data=f"view_meal {meal.meal_id}"))
    if len(pages) > 1:
        if page_idx == len(pages) - 1:
            back = InlineKeyboardButton(text=f"◀️Back", callback_data=f"meals_page {page_idx - 1}")
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            builder.row(back, page_of)
        elif page_idx > 0:
            back = InlineKeyboardButton(text=f"◀️Back", callback_data=f"meals_page {page_idx - 1}")
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            forward = InlineKeyboardButton(text=f"▶️Forward", callback_data=f"meals_page {page_idx + 1}")
            builder.row(back, page_of, forward)
        elif page_idx == 0:
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            forward = InlineKeyboardButton(text=f"▶️Forward", callback_data=f"meals_page {page_idx + 1}")
            builder.row(page_of, forward)
    builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
    return builder.as_markup()


def meal_choice(page_idx):
    builder = InlineKeyboardBuilder()
    meals = Meal.get_all(is_active=True)
    if not meals:
        builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
        return builder.as_markup()
    page_size = 5
    pages = [meals[i:i + page_size] for i in range(0, len(meals), page_size)]
    page = pages[page_idx]
    for meal in page:
        meal: Meal
        builder.row(InlineKeyboardButton(text=meal.name,
                                         callback_data=f"choose_meal {meal.meal_id}"))
    if len(pages) > 1:
        if page_idx == len(pages) - 1:
            back = InlineKeyboardButton(text=f"◀️Back", callback_data=f"meal_choice_page {page_idx - 1}")
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            builder.row(back, page_of)
        elif page_idx > 0:
            back = InlineKeyboardButton(text=f"◀️Back", callback_data=f"meal_choice_page {page_idx - 1}")
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            forward = InlineKeyboardButton(text=f"▶️Forward", callback_data=f"meal_choice_page {page_idx + 1}")
            builder.row(back, page_of, forward)
        elif page_idx == 0:
            page_of = InlineKeyboardButton(text=f"{page_idx + 1}/{len(pages)}", callback_data=f"123")
            forward = InlineKeyboardButton(text=f"▶️Forward", callback_data=f"meal_choice_page {page_idx + 1}")
            builder.row(page_of, forward)
    builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
    return builder.as_markup()


back_to_start = InlineKeyboardBuilder().add(
    InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start")).as_markup()


def meal_kb(meal_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🗑Delete meal", callback_data=f"delete_meal {meal_id}"))
    builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
    return builder.as_markup()


def menu_kb(menu_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🗑Delete menu", callback_data=f"delete_menu {menu_id}"))
    builder.row(InlineKeyboardButton(text="⏪Back to start", callback_data="back_to_start"))
    return builder.as_markup()
