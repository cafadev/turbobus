from turbobus.injection import injectable_of
from log.axioma.log import ILogger


@injectable_of(ILogger)
class Logger:

    def logger(self, text: str):
        print('from logger', text)
