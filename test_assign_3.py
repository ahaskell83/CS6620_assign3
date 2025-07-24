import pytest
from assign_3 import app

print("i made it here")

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
    

#if __name__ == '__main__':
