
def call_counter(func):
    def wrapper(*args, **kwarg):
        wrapper.calls += 1
        return wrapper
    wrapper.__dict__.update(func.__dict__)
    wrapper.calls = 0
    return wrapper
