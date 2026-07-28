#!/usr/bin/env python3
from collections.abc import Callable


def mage_counter() -> Callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable:
    def accumulator(amount: int) -> int:
        nonlocal initial_power
        initial_power += amount
        return initial_power
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable:
    def factory(spell: str) -> str:
        return f"{enchantment_type} {spell}"
    return factory


def memory_vault() -> dict[str, Callable]:
    memory = {}

    def store(key, value):
        memory[key] = value

    def recall(key):
        try:
            return memory[key]
        except KeyError:
            return "Memory not found"
    return {"store": store, "recall": recall}


if __name__ == "__main__":
    counter_a = mage_counter()
    counter_b = mage_counter()
    print("Testing mage counter...")
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")
    print()
    print("Testing spell accumulator...")
    accumulator = spell_accumulator(100)
    print(f"Bass 100, add 20 {accumulator(20)}")
    print(f"Bass 100, add 30 {accumulator(30)}")
    print()
    factory_1 = enchantment_factory("Flaming")
    factory_2 = enchantment_factory("Frozen")
    print("Testing enchantment factory...")
    print(factory_1("Sword"))
    print(factory_2("Shield"))
    print()
    print("Testing memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknow')}")
