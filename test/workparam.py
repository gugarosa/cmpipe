from cmpipe import (OrderedWorker, Stage, Pipeline)


class Adder(OrderedWorker):
    def __init__(self, number):
        super(Adder, self).__init__()
        self.number = number

    def doTask(self, value):
        return value + self.number


def main():
    stage1 = Stage(Adder, 1, number=5)
    pipe = Pipeline(stage1)

    for number in range(10):
        pipe.put(number)

    pipe.put(None)

    for result in pipe.results():
        print(result)


if __name__ == '__main__':
    main()
