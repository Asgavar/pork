import abc
from collections import defaultdict


class Command:
    pass


class Event:
    pass


class Query:
    pass


class QueryResponse:
    pass


class Router(abc.ABC):

    @abc.abstractmethod
    def route(event_command_query):
        pass


class OnlyOneFunctionRouter():

    def __init__(self):
        self.route_map = {}

    def route_class_to_func(self, clsname, handler_func) -> None:
        self.route_map[clsname] = handler_func

    def route(self, event_command_query) -> None:
        self.route_map[type(event_command_query)](event_command_query)


class AllWhichMatchFunctionRouter():

    def __init__(self):
        self.route_map = defaultdict(lambda: [])

    def route_class_to_func(self, clsname, handler_func) -> None:
        self.route_map[clsname].append(handler_func)

    def route(self, event_command_query):
        for handler in self.route_map[type(event_command_query)]:
            handler(event_command_query)


class ServiceBus:

    def __init__(self):
        self.routers = []

    def attach_router(self, router: Router) -> None:
        self.routers.append(router)

    def dispatch(self, command_event_query):
        pass


class CommandBus(ServiceBus):

    def dispatch(command: Command) -> None:
        pass


class EventBus(ServiceBus):

    def dispatch(event: Event) -> None:
        pass


class QueryBus(ServiceBus):

    def dispatch(query: Query) -> QueryResponse:
        pass
