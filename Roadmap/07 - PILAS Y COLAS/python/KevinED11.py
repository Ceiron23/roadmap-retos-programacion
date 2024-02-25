from collections import deque
from abc import ABC, abstractmethod
from typing import NoReturn, Collection, Optional, Callable, Iterable
from enum import StrEnum, Enum


class HistoryEmptyException(Exception):
    pass


def raise_history_empty_exception(msg: str) -> NoReturn:
    raise HistoryEmptyException(msg)


class Structure[T](ABC):
    @abstractmethod
    def push(self, element: T) -> None:
        pass

    @abstractmethod
    def pop(self) -> T:
        pass

    @property
    @abstractmethod
    def elements(self) -> Collection[T]:
        pass

    def __str__(self) -> str:
        return str(self.elements)

    @property
    def is_empty(self) -> bool:
        return len(self.elements) == 0


class Queue[T](Structure[T]):
    def __init__(self) -> None:
        self.__elements: deque[T] = deque()

    def push(self, element: T) -> None:
        self.__elements += [element]

    def pop(self) -> T:
        return self.__elements.popleft()

    @property
    def elements(self) -> deque[T]:
        return self.__elements


class Stack[T](Structure[T]):
    def __init__(self) -> None:
        self.__elements: list[T] = []

    def push(self, element: T) -> None:
        self.__elements += [element]

    def pop(self) -> T:
        return self.elements.pop()

    @property
    def elements(self) -> list[T]:
        return self.__elements


class Printable(ABC):
    @abstractmethod
    def print(self) -> None:
        pass

    @abstractmethod
    def set_document(self, document: str) -> None:
        pass

    @property
    @abstractmethod
    def document_history(self) -> Structure[str]:
        pass


def user_input(prompt: str) -> str:
    return input(prompt)


class PrinterActions(StrEnum):
    PRINT: str = "1"
    EXIT: str = "2"
    SHOW_DOCUMENT_HISTORY: str = "3"
    SET_DOCUMENT: str = "4"


class Printer(Printable):
    def __init__(self) -> None:
        self.__document_history: Queue[str] = Queue[str]()

    def print(self) -> None:
        if self.document_history.is_empty:
            raise_history_empty_exception("No documents to print")

        print("Printing...")
        print(self.document_history.pop())

    def set_document(self, document: str) -> None:
        self.document_history.push(document)

    @property
    def document_history(self) -> Queue[str]:
        return self.__document_history


class Navegable(ABC):
    @abstractmethod
    def go_to_page(self, page: str) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def redo(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass


class WebBrowserActions(StrEnum):
    EXIT: str = "exit"
    UNDO: str = "undo"
    REDO: str = "redo"
    GO_TO_PAGE: str = "go_to_page"


class WebBrowser(Navegable):
    def __init__(self) -> None:
        self.page_history: Stack[str] = Stack[str]()
        self.current_page: str = "inicio"
        self.current_page_index: int = 0

    def go_to_page(self, page: str) -> None:
        self.page_history.push(self.current_page)
        self.current_page = page
        self.current_page_index += 1

        print(f"Going to {page}")

    def undo(self) -> None:
        if self.page_history.is_empty:
            raise_history_empty_exception(msg="there are not previous pages to go back")

        self.current_page = self.page_history.elements.pop()
        print(f"Going back to {self.current_page}")

    def redo(self) -> None:
        if self.page_history.is_empty:
            raise_history_empty_exception(msg="there are not next pages to go forward")

    def run(self) -> None:
        pass

    @property
    def operations(self) -> dict[str, Callable]:
        return {"go_to_page": self.go_to_page, "undo": self.undo, "redo": self.redo}


def execute_printable(printable: Printable) -> None:
    while True:
        print("1 - Print, 2 - Exit, 3 - Show document history, 4 - Set document")
        user_option = user_input(prompt="Choose an option: ")

        match user_option:
            case PrinterActions.PRINT:
                try:
                    printable.print()
                except HistoryEmptyException as err:
                    print(err)
            case PrinterActions.EXIT:
                print("Bye!")
                break
            case PrinterActions.SHOW_DOCUMENT_HISTORY:
                if printable.document_history.is_empty:
                    print("No documents to print")
                    continue

                for document in printable.document_history.elements:
                    print(document)
            case PrinterActions.SET_DOCUMENT:
                document = user_input(prompt="Enter a document: ")
                printable.set_document(document=document)
                print(f"Document set: {document} successfully")
            case _:
                print("Invalid option")


def execute_navegable(navegable: Navegable) -> None:
    navegable.run()


def main() -> None:
    # Generic queue
    queue = Queue[int]()
    queue.push(1)
    queue.push(2)
    queue.push(3)
    print(queue.elements)
    print(queue.pop())
    print(queue)
    print(queue.is_empty)

    # Generic stack
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(stack.elements)
    print(stack)
    print(stack.pop())

    print(stack.elements)
    print(stack)
    print(stack.is_empty)

    printer = Printer()
    execute_printable(printable=printer)


if __name__ == "__main__":
    main()
