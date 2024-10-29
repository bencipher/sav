import os
import pandas as pd
from dotenv import load_dotenv

from config import llm
from graph_lib import setup_graph_schema, write_to_graph

load_dotenv()


def setup_graph_kb():
    df = pd.read_csv(os.environ['DATA_FILE_PATH'])
    setup_graph_schema(llm)
    write_to_graph(df)


if __name__ == "__main__":
    setup_graph_kb()
