import cmpipe


def echo(value):
    print(value)


def main():
    stage = cmpipe.OrderedStage(echo)
    pipe = cmpipe.Pipeline(stage)

    for val in (0, 1, 2, 3):
        pipe.put(val)

    pipe.put(None)  # Stop the pipeline.


if __name__ == '__main__':
    main()
