import sqlite3


class WorkWithDB:
    def __init__(self):
        self.data = ""

    def create_database():
        query = """CREATE TABLE Progress(
                username TEXT PRIMARY KEY,
                score INTEGER,
                shooting_ranges INTEGER,
                spread INTEGER,
                magazine INTEGER,
                price INTEGER
            )
        """

        with sqlite3.connect(f"data\progress.db") as con:
            con.executescript(query)

    def add_elem(username, info):
        # формирование запроса для добавления в БД
        add_query = f"""
            INSERT INTO
            Progress
            VALUES
            (?, ?, ?, ?, ?, ?),
            (
            "{username}", {info[0]}, {info[1]},
            {info[2]}, {info[3]}, {info[4]}
            )
        """

        with sqlite3.connect(f"data\progress.db") as con:
            con.executescript(add_query)

    # замена данных на дату
    def overwrite(username, info):
        info = (username, info[0], info[1], info[2], info[3], info[4])
        overwrite_query = f"""
            UPDATE Progress
            SET (username, score, shooting_ranges, spread, magazine, price) = {info}
            WHERE username = "{username}"
        """
        with sqlite3.connect(f"data\progress.db") as con:
            con.executescript(overwrite_query)

    def load_info(username):
        load_query = f"""
            SELECT score, shooting_ranges, spread, magazine, price
            FROM Progress
            WHERE username = "{username}"
        """

        res = sqlite3.connect(f"data\progress.db").execute(load_query)
        return res
