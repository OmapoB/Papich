from pathlib import Path
import pandas as pd


class DataFrameLoader(pd.DataFrame):
    __path = ''
    __cols = ''
    __skip = ''

    def __init__(self, path, cols, skip=0):
        super().__init__()
        self.__path = Path(path)
        self.__cols = cols
        self.__skip = skip

    def load_df(self):
        df = pd.read_excel(self.__path, skiprows=self.__skip)
        df.drop(labels=self.__cols, axis=1, inplace=True)
        for col in df:
            stop = False
            for i in df[col]:
                if pd.isna(i):
                    stop = True
                    df.dropna(how='all', inplace=True)
                    break
            if stop:
                break
        return df
