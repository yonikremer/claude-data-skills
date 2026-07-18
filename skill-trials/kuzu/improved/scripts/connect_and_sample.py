"""Smoke test for the Kùzu skill: creates a temp DB, loads CSVs, and queries."""

import os
import shutil
import tempfile

import kuzu


def main():
    db_dir = tempfile.mkdtemp(prefix="kuzu_skill_smoke_")
    db_path = os.path.join(db_dir, "demo.db")
    csv_dir = os.path.join(db_dir, "csv")
    os.makedirs(csv_dir, exist_ok=True)

    try:
        with open(os.path.join(csv_dir, "user.csv"), "w") as f:
            f.write("name,age\nAlice,30\nBob,25\nCarol,35\n")
        with open(os.path.join(csv_dir, "city.csv"), "w") as f:
            f.write("name\nNYC\nLA\n")
        with open(os.path.join(csv_dir, "follows.csv"), "w") as f:
            f.write("from,to,since\nAlice,Bob,2020\nBob,Carol,2021\n")
        with open(os.path.join(csv_dir, "lives_in.csv"), "w") as f:
            f.write("from,to\nAlice,NYC\nCarol,LA\n")

        db = kuzu.Database(db_path)
        conn = kuzu.Connection(db)

        conn.execute("CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64)")
        conn.execute("CREATE NODE TABLE City(name STRING PRIMARY KEY)")
        conn.execute("CREATE REL TABLE Follows(FROM User TO User, since INT64)")
        conn.execute("CREATE REL TABLE LivesIn(FROM User TO City)")

        def csv(name: str) -> str:
            return os.path.join(csv_dir, name).replace("\\", "/")

        conn.execute(f'COPY User FROM "{csv("user.csv")}" (header=true)')
        conn.execute(f'COPY City FROM "{csv("city.csv")}" (header=true)')
        conn.execute(f'COPY Follows FROM "{csv("follows.csv")}" (header=true)')
        conn.execute(f'COPY LivesIn FROM "{csv("lives_in.csv")}" (header=true)')

        # Introspection
        tables = []
        result = conn.execute("CALL show_tables() RETURN *")
        while result.has_next():
            tables.append(result.get_next())
        assert any(t[1] == "User" and t[2] == "NODE" for t in tables)
        assert any(t[1] == "Follows" and t[2] == "REL" for t in tables)
        print(f"tables ok: {len(tables)} tables")

        # Recursive query
        names = []
        result = conn.execute(
            "MATCH (a:User)-[:Follows*1..3]->(b:User) WHERE a.name = 'Alice' RETURN b.name"
        )
        while result.has_next():
            names.append(result.get_next()[0])
        assert set(names) == {"Bob", "Carol"}, names
        print(f"recursive query ok: {names}")

        # Parameterized query
        result = conn.execute(
            "MATCH (u:User) WHERE u.name = $name RETURN u.age",
            {"name": "Bob"},
        )
        assert result.has_next()
        assert result.get_next()[0] == 25
        print("parameterized query ok")

        print("all Kùzu smoke tests passed")
    finally:
        del db, conn
        shutil.rmtree(db_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
