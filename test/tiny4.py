import cmpipe


class Incrementor(cmpipe.UnorderedWorker):
    def doTask(self, value):
        result = value + 1
        self.putResult(result)


class Doubler(cmpipe.UnorderedWorker):
    def doTask(self, value):
        result = value * 2
        self.putResult(result)


def main():
    stage1 = cmpipe.Stage(Incrementor, 3)
    stage2 = cmpipe.Stage(Doubler, 3)
    stage1.link(stage2)
    pipe = cmpipe.Pipeline(stage1)

    for number in range(10):
        pipe.put(number)
    pipe.put(None)

    for result in pipe.results():
        print(result)


if __name__ == '__main__':
    main()
