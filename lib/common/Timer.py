# coding:utf-8
from functools import wraps
import time

def func_timer(function):
    '''
    用装饰器实现函数计时
    :param function: 需要计时的函数
    :return: None
    '''
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name = function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name = function.__name__,time = t1 - t0))
        return result
    return function_timer

# @func_timer
# def test(x,y):
#     s = x + y
#     time.sleep(2)
#     print ('the sum is: {0}'.format(s))
#
# if __name__ == '__main__':
#     test(1,2)
    # 输出结果
    # '''
    # [Function: test start...]
    # the sum is: 3
    # [Function: test finished, spent time: 1.50s]
    # '''