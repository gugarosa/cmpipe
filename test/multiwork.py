import sys
import cmpipe
from builtins import range


def for_loop(amount):
    for ii in range(amount):
        pass


def main():
    stage = cmpipe.UnorderedStage(for_loop, 2)
    pipe = cmpipe.Pipeline(stage)

    for foobar in range(5):
        pipe.put(int(sys.argv[1]) if len(sys.argv) >= 2 else 10)

    pipe.put(None)


if __name__ == '__main__':
    main()
