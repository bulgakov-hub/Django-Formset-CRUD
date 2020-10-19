from .forms import getTestFormset


class Settings:
    """Генерация списка вопросов и ответов"""

    __min_q, __max_q = 5, 30
    __min_a, __max_a = 2, 8

    def __init__(self, q: int = 14, a: int = 4):
        self.q = max(self.__min_q, min(self.__max_q, q))
        self.a = max(self.__min_a, min(self.__max_a, a))
        self.set_generic()

    def set_generic(self):
        self.questions = [{'question': i} for i in range(1, int(self.q) + 1)]
        self.answers = [{'prefix_name': str(
            chr(ord('А') + i))} for i in range(int(self.a))]


class TestInitialData:
    """Управление инициализацией параметра data"""

    def __init__(self, settings: Settings):
        self.set = settings
        self.answers_data = {}
        self.data = []

    def set_answers(self):
        self.answers_data = [{'prefix_name': t['prefix_name']}
                             for t in self.set.answers]

    def set_data(self):
        self.data: list = [
            dict(
                nested_extra=self.set.a,
                data=self.answers_data) for q_n in self.set.questions]


class TestManagerFormset:
    """Менеджер формсета"""

    settings = Settings
    initial_data = TestInitialData

    def __init__(self, q: int = 14, a: int = 4):
        self.data = self.initial_data(self.settings(q, a))

    def create(self):
        self.data.set_answers()
        self.data.set_data()
        return getTestFormset(
            extra=self.data.set.q,
            data=self.data.data)(
            initial=self.data.set.questions)

    def update(self, instance):
        self.data.set_data()
        return getTestFormset(extra=0,
                              data=self.data.data)(instance=instance)

    def post(self, request_post, instance=None):
        return getTestFormset()(request_post, instance=instance)
