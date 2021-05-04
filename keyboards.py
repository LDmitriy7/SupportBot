from aiogram.types import ReplyKeyboardMarkup


class AdminPanel(ReplyKeyboardMarkup):
    CREATE_LINK = 'Создать ссылку'

    def __init__(self):
        super().__init__(resize_keyboard=True, row_width=2)
        self.add(self.CREATE_LINK)


admin_panel = AdminPanel()
