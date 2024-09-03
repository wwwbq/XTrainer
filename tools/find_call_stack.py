
def who_called_me(level:int):
    import inspect
    # 获取当前调用栈
    stack = inspect.stack()
    #print(stack)
    # 获取调用者的栈帧
    caller_frame = stack[level]  # stack[0] 是 who_called_me 本身，stack[1] 是调用 who_called_me 的函数

    # 获取调用者的文件名
    caller_file = caller_frame.filename

    # 获取调用者的行号
    caller_lineno = caller_frame.lineno

    # 获取调用者的函数名
    caller_function = caller_frame.function

    return {
        'file': caller_file,
        'line': caller_lineno,
        'function': caller_function
    }