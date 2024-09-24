# utils/decorators.py

import allure
from functools import wraps


def step_with_screenshot(step_description=None):
    """
    Декоратор для оборачивания методов в Allure шаг с автоматическим прикреплением скриншота после выполнения.

    :param step_description: Описание шага. Если не указано, будет использовано имя метода.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            desc = step_description or func.__name__
            with allure.step(desc):
                result = func(self, *args, **kwargs)
                self.attach_screenshot(name=f"После шага: {desc}")
                return result

        return wrapper

    return decorator


def apply_decorator_to_methods(decorator, method_prefix='step_'):
    """
    Метакласс, который применяет заданный декоратор ко всем методам, начинающимся с определённого префикса.

    :param decorator: Декоратор для применения.
    :param method_prefix: Префикс методов, к которым будет применён декоратор.
    """

    class Meta(type):
        def __new__(cls, name, bases, dct):
            for attr, value in dct.items():
                if callable(value) and attr.startswith(method_prefix):
                    dct[attr] = decorator(attr)(value)
            return super(Meta, cls).__new__(cls, name, bases, dct)

    return Meta