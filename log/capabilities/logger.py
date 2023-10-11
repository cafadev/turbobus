from bus.decorators import injectable
from log.axioma.log import ILogger


@injectable(ILogger)
class Logger:

    def logger(self, text: str):
        print('from logger', text)
