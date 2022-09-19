from time import time


def timer_func(func):
    """
    This function shows the execution time of the function object passed
    """
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        
        delta = t2-t1   #duration in seconds
        minutes = int(delta//60)
        seconds = round(delta%60)
        print(f"Function {func.__name__}() executed in {minutes} minutes {seconds} seconds.")

        # print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s.")
        return result
    return wrap_func