import os

import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


def _connect() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
    )


def get_schema_info() -> str:
    """TPCH_SF1 スキーマのテーブル定義を取得し、LLM 用のテキストにする。"""
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = %s
            ORDER BY table_name, ordinal_position
            """,
            (os.environ["SNOWFLAKE_SCHEMA"],),
        )
        rows = cur.fetchall()
    finally:
        conn.close()

    tables: dict[str, list[str]] = {}
    for table_name, column_name, data_type in rows:
        tables.setdefault(table_name, []).append(f"  {column_name} {data_type}")

    parts: list[str] = []
    for table_name, columns in tables.items():
        cols = "\n".join(columns)
        parts.append(f"TABLE {table_name}:\n{cols}")

    return "\n\n".join(parts)


def execute_query(sql: str) -> list[dict]:
    """SQL を実行して結果を辞書のリストで返す。"""
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchmany(100)  # 最大100行に制限
        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()
