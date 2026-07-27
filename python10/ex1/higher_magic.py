#!/usr/bin/env python3
from collections.abc import Callable


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combiner(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)
    return combiner


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplifier(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplifier


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list[str]:
        res = []
        for spell in spells:
            res.append(spell(target, power))
        return res
    return sequence


if __name__ == "__main__":
    combined = spell_combiner(fireball, heal)
    print(combined("Dragon", 10))
    print()
    amplifier = power_amplifier(fireball, 10)
    print(amplifier("Dragon", 3))
    print()
    caster = conditional_caster(
            lambda target, power: power >= 10,
            fireball)
    print(caster("Dragon", 9))
    print()
    sequence = spell_sequence([fireball, heal, fireball])
    print(sequence("Dragon", 10))
