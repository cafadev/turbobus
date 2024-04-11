from tests.log.axioma.logger import ILogger


class Logger(ILogger):

    def print(self, text: str):
        print('from logger', text)


class Logger2(ILogger):

    def print(self, text: str):
        print('from logger2', text)
