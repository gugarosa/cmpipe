from sys import stdout
from threading import Thread
from time import sleep
from cmpipe.Pipeline import Pipeline
from cmpipe.UnorderedStage import UnorderedStage


def write(value):
    stdout.write(str(value))
    stdout.flush()


def inc(x):
    sleep(0.1)
    write('+')
    return x+1


def dec(x):
    sleep(0.2)
    write('-')
    return x-1


def print_results(pipeline):
    for result in pipeline.results():
        write(result)


def main():
    stage1 = UnorderedStage(inc, 3, max_backlog=3)
    stage2 = UnorderedStage(dec, 1, max_backlog=1)
    stage1.link(stage2)
    pipeline = Pipeline(stage1)

    print_thread = Thread(target=print_results, args=(pipeline,))
    print_thread.start()

    for i in range(10):
        sleep(0.01)
        pipeline.put(i)
        write('i')

    pipeline.put(None)
    print_thread.join()
    write('\n')


if __name__ == '__main__':
    main()
