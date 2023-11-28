from analyze import analyze
from table import generate
from read import get
from write import write


def main():
    StreamingHistory = get()

    write(StreamingHistory)

    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

