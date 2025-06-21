from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states.flow import EvacuatorFlow, ClientFlow

router = Router()

# Пример списка эвакуаторов, в будущем можно сделать отдельную таблицу в БД
EVACUATOR_IDS = [795677145,]  # Заменить на реальные user_id

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id in EVACUATOR_IDS:
        await message.answer(
            "Здравствуйте, эвакуатор!\n\nПожалуйста, введите номер машины для создания новой заявки."
        )
        await state.set_state(EvacuatorFlow.waiting_plate)
    else:
        await message.answer(
            "Добро пожаловать в <b>Araba</b> — эвакуация авто!\n\nВведите номер вашей машины, чтобы найти её."
        )
        await state.set_state(ClientFlow.searching_plate)
