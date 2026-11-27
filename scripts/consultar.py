"""Roda uma consulta SQL no banco do projeto e mostra o resultado na tela."""

import os
import sys

import duckdb

BANCO = os.getenv("DUCKDB_PATH", "dataops.duckdb")


def main() -> None:
    con = duckdb.connect(BANCO, read_only=True)
    con.sql(sys.argv[1]).show()
    con.close()


if __name__ == "__main__":
    main()
