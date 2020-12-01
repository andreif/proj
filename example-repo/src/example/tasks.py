import sys
sys.path.append('src')

import django
django.setup()


def task(func):
    def decorator():
        try:
            print('Running task:', func.__name__)
            return func()
        except Exception:
            raise
    return decorator


@task
def example():
    from example import api
    print("example", api.example())


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Provide task name(s) as command arguments')
        exit()
    for t in sys.argv[1:]:
        if t in locals():
            locals()[t]()
        else:
            print(f'Unknown task: {t}')
