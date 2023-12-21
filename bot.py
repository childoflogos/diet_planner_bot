import asyncio
from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import F
import config
from markups import reply, inline
from database import *

storage = MemoryStorage()

bot = Bot(token=config.telegram_token, parse_mode='HTML')

dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await bot.send_message(message.from_user.id, f'<b>☀️Welcome to diet planning assistant</b>',
                           reply_markup=reply.start_kb())


@dp.callback_query(F.data == 'back_to_start')
async def back_to_start(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, f'<b>☀️Welcome to diet planning assistant</b>',
                           reply_markup=reply.start_kb())


@dp.message(F.text == '🥦Menus')
async def view_menus(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await bot.send_message(message.from_user.id,
                           "<b>🥦Menus</b>",
                           reply_markup=inline.menus_kb(page_idx=0))


@dp.callback_query(F.data.startswith('menus_page '))
async def menus_page(callback_query: CallbackQuery):
    page_idx = int(callback_query.data.split(' ')[1])
    await callback_query.message.edit_reply_markup(reply_markup=inline.menus_kb(page_idx=page_idx))


class AddMenuFSM(StatesGroup):
    name = State()
    breakfast = State()
    lunch = State()
    dinner = State()


@dp.message(F.text == '➕Create menu')
async def view_menus(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    meals = Meal.get_all(is_active=True)
    if not meals:
        await bot.send_message(message.from_user.id, '<b>❗️Please add at least one meal</b>')
        return
    await bot.send_message(message.from_user.id, "<b>Enter menu name</b>",
                           reply_markup=inline.back_to_start)
    await state.set_state(AddMenuFSM.name)


@dp.callback_query(F.data == 'add_menu')
async def add_menu(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    meals = Meal.get_all(is_active=True)
    if not meals:
        await callback_query.answer('❗️Please add at least one meal')
        return
    await callback_query.message.edit_text("<b>Enter menu name</b>",
                                           reply_markup=inline.back_to_start)
    await state.set_state(AddMenuFSM.name)


@dp.message(AddMenuFSM.name, lambda message: message.text)
async def add_menu_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, '<b>Choose meal for breakfast</b>',
                           reply_markup=inline.meal_choice(page_idx=0))
    await state.set_state(AddMenuFSM.breakfast)


@dp.callback_query(F.data.startswith('meal_choice_page '))
async def meal_choice_page(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return
    page_idx = int(callback_query.data.split(' ')[1])
    await callback_query.message.edit_reply_markup(reply_markup=inline.meal_choice(page_idx=page_idx))


@dp.callback_query(F.data.startswith('choose_meal '))
async def choose_meal(callback_query: CallbackQuery, state: FSMContext):
    meal_id = int(callback_query.data.split(' ')[1])
    current_state = await state.get_state()
    if not current_state:
        return
    if current_state == AddMenuFSM.breakfast:
        await state.update_data(breakfast_meal_id=meal_id)
        await callback_query.message.edit_text('<b>Choose meal for lunch</b>')
        await callback_query.message.edit_reply_markup(reply_markup=inline.meal_choice(page_idx=0))
        await state.set_state(AddMenuFSM.lunch)
    elif current_state == AddMenuFSM.lunch:
        await state.update_data(lunch_meal_id=meal_id)
        await callback_query.message.edit_text('<b>Choose meal for dinner</b>')
        await callback_query.message.edit_reply_markup(reply_markup=inline.meal_choice(page_idx=0))
        await state.set_state(AddMenuFSM.dinner)
    elif current_state == AddMenuFSM.dinner:
        data = await state.get_data()
        menu = Menu(name=data['name'], breakfast_meal_id=data['breakfast_meal_id'], lunch_meal_id=data['lunch_meal_id'],
                    dinner_meal_id=meal_id).save()
        await callback_query.message.edit_text('✅Menu added')
        breakfast = Meal.get(meal_id=menu.breakfast_meal_id)
        lunch = Meal.get(meal_id=menu.lunch_meal_id)
        dinner = Meal.get(meal_id=menu.dinner_meal_id)
        await bot.send_message(callback_query.from_user.id,
                               f'<b>🥦Menu №{menu.menu_id}</b>\n'
                               f'Name: {menu.name}\n\n'
                               f'Breakfast: {breakfast.name} (Calories amount: {breakfast.calories})\n\n'
                               f'Lunch: {lunch.name} (Calories amount: {lunch.calories})\n\n'
                               f'Dinner: {dinner.name} (Calories amount: {dinner.calories})\n\n'
                               f'Total calories amount: {breakfast.calories + lunch.calories + dinner.calories}',
                               reply_markup=inline.menu_kb(menu.menu_id))


@dp.callback_query(F.data.startswith('view_menu '))
async def view_menu(callback_query: CallbackQuery):
    menu_id = int(callback_query.data.split(' ')[1])
    menu = Menu.get(menu_id=menu_id)
    breakfast = Meal.get(meal_id=menu.breakfast_meal_id)
    lunch = Meal.get(meal_id=menu.lunch_meal_id)
    dinner = Meal.get(meal_id=menu.dinner_meal_id)
    await callback_query.message.edit_text(
        f'<b>🥦Menu №{menu.menu_id}</b>\n'
        f'Name: {menu.name}\n\n'
        f'Breakfast: {breakfast.name} (Calories amount: {breakfast.calories})\n\n'
        f'Lunch: {lunch.name} (Calories amount: {lunch.calories})\n\n'
        f'Dinner: {dinner.name} (Calories amount: {dinner.calories})\n\n'
        f'Total calories amount: {breakfast.calories + lunch.calories + dinner.calories}',
        reply_markup=inline.menu_kb(menu.menu_id))


@dp.callback_query(F.data.startswith('delete_menu '))
async def delete_menu(callback_query: CallbackQuery):
    menu_id = int(callback_query.data.split(' ')[1])
    menu = Menu.get(menu_id=menu_id)
    menu.delete()
    await bot.send_message(callback_query.from_user.id, '<b>✅Menu deleted</b>',
                           reply_markup=inline.back_to_start)


@dp.message(F.text == '🍽Meals')
async def meals(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await bot.send_message(message.from_user.id,
                           "<b>🍽Meals</b>",
                           reply_markup=inline.meals_kb(page_idx=0))


@dp.callback_query(F.data.startswith('meals_page '))
async def meals_page(callback_query: CallbackQuery):
    page_idx = int(callback_query.data.split(' ')[1])
    await callback_query.message.edit_reply_markup(reply_markup=inline.meals_kb(page_idx=page_idx))


class AddMealFSM(StatesGroup):
    name = State()
    ingredients = State()
    calories = State()


@dp.callback_query(F.data == 'add_meal')
async def add_meal(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await callback_query.message.edit_text("<b>Enter meal name</b>",
                                           reply_markup=inline.back_to_start)
    await state.set_state(AddMealFSM.name)


@dp.message(AddMealFSM.name, lambda message: message.text)
async def add_meal_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, '<b>Enter meal ingredients list</b>',
                           reply_markup=inline.back_to_start)
    await state.set_state(AddMealFSM.ingredients)


@dp.message(AddMealFSM.ingredients, lambda message: message.text)
async def add_meal_ingredients(message: Message, state: FSMContext):
    await state.update_data(ingredients=message.text)
    await bot.send_message(message.from_user.id, '<b>Enter meal calories amount</b>',
                           reply_markup=inline.back_to_start)
    await state.set_state(AddMealFSM.calories)


@dp.message(AddMealFSM.calories, lambda message: message.text)
async def add_meal_calories(message: Message, state: FSMContext):
    try:
        calories = int(message.text)
    except:
        await bot.send_message(message.from_user.id, '<b>Enter integer</b>',
                               reply_markup=inline.back_to_start)
        return
    data = await state.get_data()
    await state.clear()
    meal = Meal(name=data['name'], ingredients=data['ingredients'], calories=calories).save()
    await bot.send_message(message.from_user.id, '<b>✅Meal added</b>')
    await bot.send_message(message.from_user.id, f'<b>🍽Meal №{meal.meal_id}</b>\n'
                                                 f'Name: {meal.name}\n'
                                                 f'Ingredients: {meal.ingredients}\n'
                                                 f'Calories amount: {meal.calories}',
                           reply_markup=inline.meal_kb(meal.meal_id))


@dp.callback_query(F.data.startswith('view_meal '))
async def view_meal(callback_query: CallbackQuery):
    meal_id = int(callback_query.data.split(' ')[1])
    meal = Meal.get(meal_id=meal_id)
    await callback_query.message.edit_text(f'<b>🍽Meal №{meal.meal_id}</b>\n'
                                           f'Name: {meal.name}\n'
                                           f'Ingredients: {meal.ingredients}\n'
                                           f'Calories amount: {meal.calories}',
                                           reply_markup=inline.meal_kb(meal.meal_id))


@dp.callback_query(F.data.startswith('delete_meal '))
async def delete_meal(callback_query: CallbackQuery):
    meal_id = int(callback_query.data.split(' ')[1])
    meal = Meal.get(meal_id=meal_id)
    meal.delete()
    await bot.send_message(callback_query.from_user.id, '<b>✅Meal deleted</b>',
                           reply_markup=inline.back_to_start)


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


basicConfig(level=INFO)
asyncio.run(main())
