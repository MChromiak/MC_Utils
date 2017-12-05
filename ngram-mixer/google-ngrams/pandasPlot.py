import sys
from pandas import read_csv
import matplotlib.pyplot as plt


def plotPandas(filename):
    df = read_csv(filename,  index_col=0, parse_dates=True)
    for col in df.columns:
        df[col] = [i * 100 for i in df[col]]
    df.plot(title=' '.join(df.columns.values.tolist()))
    plt.show()

if __name__ == '__main__':

    plotPandas(sys.argv[1])