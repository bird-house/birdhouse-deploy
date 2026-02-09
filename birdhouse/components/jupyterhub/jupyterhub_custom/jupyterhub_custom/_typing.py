from typing import Literal, NotRequired, TypedDict


class LimitDict(TypedDict):
    mem_limit: NotRequired[str | int]
    cpu_limit: NotRequired[str | float | int]
    gpu_ids: NotRequired[list[int | str]]
    gpu_count: NotRequired[int]


class LimitRule(TypedDict):
    type: Literal["user", "group"]
    name: str
    limits: LimitDict
