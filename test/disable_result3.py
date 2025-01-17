from cmpipe import (UnorderedWorker, Stage, Pipeline)


class Yes(UnorderedWorker):
    def doTask(self, value):
        return value


def main():
    stage = Stage(Yes, 4, disable_result=True)
    pipe = Pipeline(stage)

    for number in range(10):
        pipe.put(number)
    pipe.put(None)

    count = 0
    for _ in pipe.results():
        count += 1

    print(count)


if __name__ == '__main__':
    main()
