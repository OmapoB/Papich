from pathlib import Path

from pandas import DataFrame, read_excel, isna


class DataFrameLoader(DataFrame):
    def __init__(self, path=None, cols=None, skip=0):
        super().__init__()
        self.path = path
        self.my_cols = cols
        self.skip = skip

    def get_path(self):
        return self.path

    def set_path(self, path: str):
        self.path = Path(path)

    def get_cols(self):
        return self.my_cols

    def set_cols(self, new_cols: list):
        self.my_cols = new_cols

    def get_skip(self):
        return self.skip

    def set_skip(self, new_skip: int):
        self.skip = new_skip

    def load_df(self):
        df = read_excel(self.path, skiprows=self.skip)
        df.drop(labels=self.my_cols, axis=1, inplace=True)
        for col in df:
            stop = False
            for i in df[col]:
                if isna(i):
                    stop = True
                    df.dropna(how='all', inplace=True)
                    break
            if stop:
                break
        return df
