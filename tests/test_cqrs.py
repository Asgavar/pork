import pytest
import pork.messaging


class SpyEventHandler:

    def __init__(self):
        self.calls = 0

    def __call__(self, event):
        self.calls += 1


class DummyEvent:
    pass


def test_only_one_func_router(route_def_repetitions):
    router = pork.messaging.OnlyOneFunctionRouter()
    handler = SpyEventHandler()
    repeat_n_times(
        lambda: router.route_class_to_func(DummyEvent, handler),
        route_def_repetitions
    )

    router.route(DummyEvent())

    assert handler.calls == 1


def test_many_func_router(route_def_repetitions):
    router = pork.messaging.AllWhichMatchFunctionRouter()
    handler = SpyEventHandler()
    repeat_n_times(
        lambda: router.route_class_to_func(DummyEvent, handler),
        route_def_repetitions
    )

    router.route(DummyEvent())

    assert handler.calls == route_def_repetitions


def repeat_n_times(func, n):
    for _ in range(n):
        func()


@pytest.fixture(params=[1, 5, 99])
def route_def_repetitions(request):
    return request.param
