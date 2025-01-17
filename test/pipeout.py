from cmpipe import (OrderedStage, Pipeline)


def increment(value):
    return value + 1


def double(value):
    return value * 2


def main():
    stage1 = OrderedStage(increment)
    stage2 = OrderedStage(double)
    stage1.link(stage2)
    pipe = Pipeline(stage1)

    for number in range(10):
        pipe.put(number)

    pipe.put(None)

    for result in pipe.results():
        print(result)


if __name__ == '__main__':
    main()
