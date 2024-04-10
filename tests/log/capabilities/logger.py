from tests.log.axioma.logger import ILogger


class Logger(ILogger):

    def print(self, text: str):
        print('from logger', text)
