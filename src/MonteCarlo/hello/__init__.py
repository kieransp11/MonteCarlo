from .hello import *
__all__ = [hello]


def _compile():
    pass


def template():
    print("template2")


def main():
    """Initialise the module upon import"""
    print("importing")


main()
