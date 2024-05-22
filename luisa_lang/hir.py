from typing import List, Optional, Tuple


class Type:
    pass


class UnitType(Type):
    def __eq__(self, value: object) -> bool:
        return isinstance(value, UnitType)


class Span:
    file: str
    start: Tuple[int, int]
    end: Tuple[int, int]


class Node:
    type: Optional[Type]
    span: Optional[Span]

    def __init__(
        self, type: Optional[Type] = None, span: Optional[Span] = None
    ) -> None:
        self.type = type
        self.span = span


class Ref(Node):
    pass


class Value(Node):
    pass


class Var(Ref):
    name: str

    def __init__(self, name: str, type: Optional[Type]) -> None:
        self.name = name
        self.type = type


class Load(Value):
    ref: Ref

    def __init__(self, ref: Ref) -> None:
        self.ref = ref
        self.type = ref.type


class Stmt:
    pass


class Assign(Stmt):
    ref: Ref
    value: Value

    def __init__(self, ref: Ref, value: Value) -> None:
        self.ref = ref
        self.value = value


class Function:
    name: str
    params: List[Tuple[str, Type]]
    return_type: Type
    body: List[Stmt]

    def __init__(
        self,
        name: str,
        params: List[Tuple[str, Type]],
        return_type: Type,
        body: List[Stmt],
    ) -> None:
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body


class Context:
    def __init__(self) -> None:
        pass
