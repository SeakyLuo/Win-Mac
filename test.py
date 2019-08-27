def first(func=None, x=1, y=2, z=3):
    print('first')
    def decorator(func):
        l = [x, y, z]
        def execute_first():
            print(func.__name__)
            func(l)
            print(l)
        return execute_first
    return decorator(func) if func else decorator

def test(func=None, x=1, y=2, z=3):
    print('first')
    def decorator(func):
        l = [x, y, z]
        def execute_first():
            print(func.__name__)
            func(l)
            print(l)
        return execute_first
    return decorator

def second(func, d={'x':10,'y':20,'z':30}):
    @first(x=d['x'], y=d['y'], z=d['z'])
    def execute_second(l):
        print(func.__name__, 'in execute_second')
        func(l)
    return execute_second

@second
##@second({'x':100,'y':200,'z':300})
def third(l):
    print('third')
    l.append(1)

third()

# def f1():
#     print(1)
#     return True

# def f2():
#     print(2)
#     return False

# f1() or f2()
