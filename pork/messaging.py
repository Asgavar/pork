import abc
from collections import defaultdict
from typing import Any


class Router(abc.ABC):

    @abc.abstractmethod
    def route(event_command_query):
        pass


class OnlyOneFunctionRouter():

    def __init__(self):
        self._route_map = {}

    def route_class_to_func(self, clsname, handler_func) -> None:
        self._route_map[clsname] = handler_func

    def route(self, event_command_query) -> Any:
        handler_to_invoke = self._route_map[type(event_command_query)]
        return handler_to_invoke(event_command_query)


class AllWhichMatchFunctionRouter():

    def __init__(self):
        self._route_map = defaultdict(lambda: [])

    def route_class_to_func(self, clsname, handler_func) -> None:
        self._route_map[clsname.__qualname__].append(handler_func)

    def route(self, event_command_query):
        for handler in self._route_map[type(event_command_query).__qualname__]:
            handler(event_command_query)


class ServiceBus:

    def __init__(self):
        self._routers = []

    def attach_router(self, router: Router) -> None:
        self._routers.append(router)

    def dispatch(self, command_event_query):
        pass


class CommandBus(ServiceBus):

    def dispatch(self, command) -> None:
        self._routers[-1].route(command)


class EventBus(ServiceBus):

    def dispatch(self, event) -> None:
        for router in self._routers:
            router.route(event)


class QueryBus(ServiceBus):

    def dispatch(self, query) -> Any:
        return self._routers[-1].route(query)
