#!/usr/bin/env python3


class DataCollection:
    def __init__(self):
        self.raw_data = []
        self.series = {}
        self.functions = {}

    @property
    def num_series(self) -> int:
        return len(self.series)

    def add_raw_data(self, data: float):
        self.raw_data.append(data)

    def add_series(self, name: str):
        self.series[name] = []
        self.functions[name] = None

    def add_series_data(self, series_name: str, data: float):
        self.series[series_name].append(data)

    def set_series_function(self, series_name: str, function: str):
        self.functions[series_name] = function


def load_data_from_files(data_file: str, functions_file: str) -> DataCollection:
    import csv
    collection = DataCollection()
    with open(data_file, 'r') as df:
        csvf = csv.reader(df, delimiter=',')
        headers = next(csvf)
        num_cols = len(headers)
        assert num_cols >= 2
        assert headers[0].lower() == 'size'
        assert headers[1].lower() == 'raw'
        size_col = 0
        raw_col = 1
        for series in headers[2:]:
            collection.add_series(series)
        for row in csvf:
            for c in range(num_cols):
                if c == size_col:
                    continue
                elif c == raw_col:
                    collection.add_raw_data(row[c])
                else:
                    collection.add_series_data(headers[c], row[c])
    with open(functions_file, 'r') as ff:
        csvf = csv.reader(ff, delimiter=',')
        headers = next(csvf)
        num_cols = len(headers)
        assert num_cols == collection.num_series
        functions = next(csvf)
        for c in range(num_cols):
            collection.set_series_function(headers[c], functions[c])
    return collection


def plot_data(collection: DataCollection):
    import matplotlib.pyplot as plt
    xs = list(range(1, len(collection.raw_data) + 1))
    plt.plot(xs, collection.raw_data, label='raw')
    for series, data in collection.series.items():
        plt.plot(xs, data, label=series)
    plt.xlabel('Input Size')
    plt.ylabel('Cost')
    plt.title('Data')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    parser.add_argument('functions_file')
    args = parser.parse_args()

    data_collection = load_data_from_files(
        data_file=args.data_file,
        functions_file=args.functions_file)
    plot_data(data_collection)
