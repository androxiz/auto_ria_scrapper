import os
import subprocess
from datetime import datetime
from app.config import settings

def dump_database():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dump_file = f"dumps/autoria_{timestamp}.sql"

    command = [
        "pg_dump",
        "-h", os.getenv("POSTGRES_HOST"),
        "-U", os.getenv("POSTGRES_USER"),
        "-d", os.getenv("POSTGRES_DB"),
        "-f", dump_file
    ]

    env = os.environ.copy()
    env["PGPASSWORD"] = os.getenv("POSTGRES_PASSWORD")

    subprocess.run(command, env=env)

    print(f"[DUMP] Database dumped to {dump_file}")
