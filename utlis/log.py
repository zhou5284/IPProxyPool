# coding:utf-8
import sys
from setting import  *


class Logger(object):

    def __init__(self):
        self._logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=LOG_FMT,datefmt=LOG_DATEFMT)
        # 设置文件模式
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        # 设置端口日志模式
        self._logger.addHandler(self._get_console_handler())
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self,filename):
        '''返回一个handler'''
        filehandler = logging.FileHandler(filename=filename,encoding='utf-8')
        filehandler.setFormatter(self.formatter)
        return filehandler

    def _get_console_handler(self):
        '''返回到终端'''
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler


    @property
    def logger(self):
        return self._logger

logger = Logger().logger


if __name__ == '__main__':
    logger.debug('调试信息')
    logger.info('状态信息')
    logger.warning('警告信息')
    logger.error('错误信息')
    logger.critical('严重错误信息')