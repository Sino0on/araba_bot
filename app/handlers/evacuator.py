from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states.flow import EvacuatorFlow
from app.database import add_evacuation
from app.services.notify import delayed_notification

router = Router()

@router.message(EvacuatorFlow.waiting_plate)
async def get_plate(message: Message, state: FSMContext):
    await state.update_data(plate=message.text.upper())
    await message.answer("Введите марку машины:")
    await state.set_state(EvacuatorFlow.waiting_brand)

@router.message(EvacuatorFlow.waiting_brand)
async def get_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await message.answer("Выберите причину эвакуации:\nНапример: Неправильная парковка")
    await state.set_state(EvacuatorFlow.waiting_reason)

@router.message(EvacuatorFlow.waiting_reason)
async def get_reason(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("Откуда была забрана машина?")
    await state.set_state(EvacuatorFlow.waiting_from)

@router.message(EvacuatorFlow.waiting_from)
async def get_from(message: Message, state: FSMContext):
    await state.update_data(from_location=message.text)
    await message.answer("Куда была доставлена машина?")
    await state.set_state(EvacuatorFlow.waiting_to)

@router.message(EvacuatorFlow.waiting_to)
async def get_to(message: Message, state: FSMContext):
    await state.update_data(to_location=message.text)
    await message.answer("Отправьте видео, кружок или фото машины:")
    await state.set_state(EvacuatorFlow.waiting_media)

@router.message(EvacuatorFlow.waiting_media, F.video | F.video_note | F.photo)
async def get_media(message: Message, state: FSMContext):
    data = await state.get_data()
    media_id = (
        message.video.file_id if message.video else
        message.video_note.file_id if message.video_note else
        message.photo[-1].file_id if message.photo else
        None
    )
    if not media_id:
        await message.answer("Ошибка: не удалось получить файл. Попробуйте снова.")
        return

    add_evacuation(
        plate=data['plate'],
        brand=data['brand'],
        reason=data['reason'],
        from_loc=data['from_location'],
        to_loc=data['to_location'],
        media_id=media_id
    )

    await message.answer("✅ Заявка сохранена! Спасибо.")

    # ⏳ Уведомим клиентов через 30 минут
    await delayed_notification(message.bot, data['plate'], data['brand'])

    await state.clear()
