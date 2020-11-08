from .forms import getTestFormset


class Settings:
    """Настройки списка вопросов, ответов, параметра data"""

    # Диапазоны значений количества вопросов и вариантов ответа
    __min_q, __max_q = 5, 30
    __min_a, __max_a = 2, 8

    def __init__(self, q: int = 14, a: int = 4):

        # Выбор значений в пределах диапазона
        self.q = max(self.__min_q, min(self.__max_q, q))
        self.a = max(self.__min_a, min(self.__max_a, a))

        # Генерируем списки вопросов и ответов
        self.questions = [{'question': i} for i in range(1, int(self.q) + 1)]
        self.answers = [{'prefix_name': str(
            chr(ord('А') + i))} for i in range(int(self.a))]

        # Параметр data
        self.data = []

    def set_data(self, answers={}):
        self.data: list = [
            dict(
                nested_extra=self.a,
                data=answers) for q_n in self.questions]


class TestManagerFormset:
    """Управление формсетом"""

    settings = Settings

    def __init__(self, q: int = 14, a: int = 4):
        self.set = self.settings(q, a)

    def create(self):
        '''Создать'''
        self.set.set_data(self.set.answers)

        return getTestFormset(
            extra=self.set.q,
            data=self.set.data)(
            initial=self.set.questions)

    def update(self, instance):
        '''Обновить'''
        self.set.set_data()

        return getTestFormset(extra=0,
                              data=self.set.data)(instance=instance)

    def post(self, request_post, instance=None):
        '''Отправить Post'''

        return getTestFormset()(request_post, instance=instance)
