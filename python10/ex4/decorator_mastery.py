#!/usr/bin/env python3
from functools import wraps
import time
from collections.abc import Callable


def spell_timer(func: Callable) -> Callable:
    
    @wraps(func)
    def wrapper(*args):
        print(f"Casting {func.__name__}...")
        start = time.time()
        res = func(*args)
        end = time.time()
        dur = end - start
        print(f"Spell completed in {dur:.3f} seconds")
        return res
    return wrapper



@spell_timer
def fireball():
    time.sleep(0.101)
    return "Fireball cast!"


def power_validator(min_power: int) -> Callable:
    def decorator(func : Callable) -> Callable:
        @wraps(func)
        def wrapper(*args) -> str:
            length = len(args)
            if length > 2:
                power = args[2]
            else:
                power = args[0]
            if power >= min_power:
                return func(*args)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


@power_validator(10)
def heal(power: int, target: str) -> str:
    return f"heal {target} with amount {power}"


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args) -> str: 
            for att in range (1,max_attempts + 1 ):
                try:
                    return func(*args)
                except Exception:
                    if att < max_attempts:
                        print(
                                f"Spell failed, retrying..." 
                                f" (attempt {att}/{max_attempts})")
                    elif att == max_attempts:
                        return (
                                f"Spell casting failed after " 
                                f"{max_attempts} attempts")
        return wrapper
    return decorator


@retry_spell(3)
def cast_spell_fail():
    raise Exception("error")


@retry_spell(3)
def cast_spell_success() -> str:
    return "Waaaaaaagh spelled !"
    

class MageGuild():
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) >= 3:
            name = name.replace(" ","")
            if name.isalpha():
                return True
        return False

    @power_validator(10)    
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":
    print("Testing spell timer...")
    print(f"Result : {fireball()}")
    print()
    print("Testing power validator..")
    print(f"Power = 10: {heal(10, 'Dragon')}")
    print(f"Power = 9: {heal(9, 'Dragon')}")
    print()
    print("Testing retrying spell...")
    print(cast_spell_fail())
    print(cast_spell_success())
    print()
    print("Testing MageGuild..")
    print(MageGuild.validate_mage_name("adam"))
    print(MageGuild.validate_mage_name("adam 123"))
    mage = MageGuild()
    print(mage.cast_spell("Lightning", 15))
    print(mage.cast_spell("lightning", 9))
