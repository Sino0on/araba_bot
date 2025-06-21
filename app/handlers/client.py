from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.states.flow import ClientFlow
from app.database import get_evacuation_by_plate, get_all_unique_brands_by_plate, add_watcher

router = Router()

@router.message(ClientFlow.searching_plate)
async def client_enter_plate(message: Message, state: FSMContext):
    plate = message.text.upper()
    await state.update_data(plate=plate)
    add_watcher(user_id=message.from_user.id, plate=plate)

    brands = get_all_unique_brands_by_plate(plate)
    if not brands:
        await message.answer("🚫 Машина с таким номером пока не найдена.")
        await state.clear()
        return

    if len(brands) == 1:
        await show_evacuations_by_brand(message, state, plate, brands[0])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=brand, callback_data=f"brand_{brand}")] for brand in brands
        ])
        await message.answer("Найдено несколько машин с этим номером. Выберите марку:", reply_markup=kb)
        await state.set_state(ClientFlow.selecting_brand)

@router.callback_query(F.data.startswith("brand_"))
async def client_select_brand(callback: CallbackQuery, state: FSMContext):
    brand = callback.data.replace("brand_", "")
    data = await state.get_data()
    plate = data.get("plate")
    await callback.message.delete()
    await show_evacuations_by_brand(callback.message, state, plate, brand)

async def show_evacuations_by_brand(message: Message, state: FSMContext, plate: str, brand: str):
    evacs = get_evacuation_by_plate(plate)
    filtered = [e for e in evacs if e[2] == brand]  # e[2] = brand

    if not filtered:
        await message.answer("Нет записей об эвакуации этой машины.")
        await state.clear()
        return

    latest = filtered[0]
    _, _, _, reason, from_loc, to_loc, media_id, timestamp = latest


    caption = f"<b>Информация об эвакуации:</b>\n\n🚘 Номер: {plate}\n🏷 Марка: {brand}\n📍 Откуда: {from_loc}\n📦 Куда: {to_loc}\n🕰 Дата: {timestamp}\n❗ Причина: {reason}"
    if media_id.startswith("BAACAg") or media_id.startswith("AgAD"):  # Telegram file_id для фото
        await message.answer_photo(
            media_id,
            caption=caption
        )
    elif media_id.startswith("DQACAg"):  # video_note file_id
        await message.answer_video_note(media_id)
        await message.answer(caption)  # текст отдельно
    else:
        await message.answer_video(
            media_id,
            caption=caption
        )

    await state.clear()
