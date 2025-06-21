from aiogram.fsm.state import StatesGroup, State

class RoleSelection(StatesGroup):
    choosing_role = State()

class EvacuatorFlow(StatesGroup):
    waiting_plate = State()
    waiting_brand = State()
    waiting_reason = State()
    waiting_from = State()
    waiting_to = State()
    waiting_media = State()

class ClientFlow(StatesGroup):
    searching_plate = State()
    selecting_brand = State()
