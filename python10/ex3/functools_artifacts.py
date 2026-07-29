#!/usr/bin/env python3
from functools import reduce, partial, lru_cache, singledispatch
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    if operation == "add":
        return reduce(operator.add, spells)
    elif operation == "multiply":
        return reduce(operator.mul, spells)
    elif operation == "max":
        return reduce(max, spells)
    elif operation == "min":
        return reduce(min, spells)
    else:
        raise ValueError(
                "Support operations: 'add', 'multiply', 'max', 'min'")


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return ({
        "fire": partial(base_enchantment, 50, "Fire"),
        "ice":  partial(base_enchantment, 50, "ice"),
        "earth": partial(base_enchantment, 50, "earth")}
            )


def enchant(power: int, element: str, target: str) -> str:
    return f"{element} {target} with power {power}"


@lru_cache
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n-1) + memoized_fibonacci(n-2)


def spell_dispatcher() -> Callable[[Any], str]:

    @singledispatch
    def base(value) -> str:
        return "Unknown spell type"

    @base.register
    def _(value: int) -> str:
        return f"{value} damage"

    @base.register
    def _(value: str) -> str:
        return value

    @base.register
    def _(value: list) -> str:
        return f"{len(value)} spells"
    return base


if __name__ == "__main__":
    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")
    print(f"Min {spell_reducer(spells, 'min')}")
    try:
        print(f"Error: {spell_reducer(spells, 's')}")
    except ValueError as e:
        print(e)
    print()
    print("Testing partail enchanter...")
    partail = partial_enchanter(enchant)
    print(f"Fire : {partail['fire']('sword')}")
    print(f"Ice : {partail['ice']('sword')}")
    print(f"Earth : {partail['earth']('sword')}")
    print()
    print("Testing memoized fibonacci...")
    print(f"Fib(0) : {memoized_fibonacci(0)}")
    print(f"Fib(1) : {memoized_fibonacci(1)}")
    print(f"Fib(10) : {memoized_fibonacci(10)}")
    print(f"Fib(15) : {memoized_fibonacci(15)}")
    print(memoized_fibonacci.cache_info())
    print()
    print("Testing spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(f"Damage spell: {dispatcher(42)}")
    print(f"Enchantment: {dispatcher('fireball')}")
    print(f"Multi-cast: {dispatcher([1, 2, 3])}")
    print(dispatcher((1, 2)))
