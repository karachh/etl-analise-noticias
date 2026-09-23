import sqlite3

def criar_conexao(landing):
    conn = None
    try:
        conn = sqlite3.connect(landing)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def criar_tabela(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        author TEXT,
        title TEXT,
        description TEXT,
        url TEXT UNIQUE,
        published_at TEXT,
        fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def inserir_artigo(conn, article):
    sql = """
    INSERT OR IGNORE INTO articles (source, author, title, description, url, published_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(sql, (
        article["source"]["name"],
        article["author"],
        article["title"],
        article["description"],
        article["url"],
        article["publishedAt"],
    ))
    conn.commit()