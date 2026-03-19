import os
from collections.abc import Generator

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client: OpenAI | None = None
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client

SQL_SYSTEM_PROMPT = """\
You are a SQL expert. Given the user's question and the database schema below,
generate a single Snowflake-compatible SQL query that answers the question.

Rules:
- Return ONLY the SQL query, no explanation, no markdown fences.
- Use only the tables and columns listed in the schema.
- Always LIMIT results to 100 rows unless the user specifies otherwise.

Schema:
{schema}
"""

ANSWER_SYSTEM_PROMPT = """\
You are a helpful data analyst. The user asked a question about their data.
You ran a SQL query and got results. Summarize the results in clear, natural Japanese.
If the data contains numbers, format them readably (e.g. comma separators).
"""


def generate_sql(question: str, schema: str) -> str:
    """ユーザーの質問からSQLを生成する。"""
    response = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SQL_SYSTEM_PROMPT.format(schema=schema)},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    sql = response.choices[0].message.content.strip()
    # マークダウンのコードブロックが付いてくる場合に除去
    if sql.startswith("```"):
        sql = sql.split("\n", 1)[1]
        sql = sql.rsplit("```", 1)[0]
    return sql.strip()


def generate_answer(
    question: str, sql: str, results: list[dict]
) -> Generator[str, None, None]:
    """クエリ結果を自然言語で要約する（ストリーミング）。"""
    user_content = (
        f"質問: {question}\n\n"
        f"実行したSQL:\n{sql}\n\n"
        f"結果:\n{results}"
    )
    stream = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content
