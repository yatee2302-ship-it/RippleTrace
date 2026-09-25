from pathlib import Path
import json
import shutil
from datetime import datetime

ROOT = Path.cwd()

PACKAGE = ROOT / "package.json"
CDSRC = ROOT / ".cdsrc.json"
DB_SQLITE = ROOT / "db" / "rippletrace.sqlite"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path):
    if path.exists():
        backup_path = path.with_suffix(
            path.suffix + f".backup_{timestamp}"
        )
        shutil.copy2(path, backup_path)
        print(f"Backup: {backup_path}")


print("=" * 60)
print("RippleTrace CAP Database Fix")
print("=" * 60)


# ------------------------------------------------------------
# BACKUP
# ------------------------------------------------------------

backup(PACKAGE)

if CDSRC.exists():
    backup(CDSRC)


# ------------------------------------------------------------
# PACKAGE.JSON
# ------------------------------------------------------------

if not PACKAGE.exists():
    print("ERROR: package.json not found.")
    raise SystemExit(1)


with PACKAGE.open("r", encoding="utf-8") as f:
    package = json.load(f)


cds_config = package.setdefault("cds", {})

requires = cds_config.setdefault("requires", {})

db = requires.setdefault("db", {})

db["kind"] = "sqlite"

# Persistent development database
db["credentials"] = {
    "database": "db/rippletrace.sqlite"
}


with PACKAGE.open("w", encoding="utf-8") as f:
    json.dump(
        package,
        f,
        indent=2
    )
    f.write("\n")


print("Updated package.json")
print("Database: db/rippletrace.sqlite")


# ------------------------------------------------------------
# .CDSRC.JSON
# ------------------------------------------------------------

cdsrc_data = {}

if CDSRC.exists():

    try:

        with CDSRC.open(
            "r",
            encoding="utf-8"
        ) as f:
            cdsrc_data = json.load(f)

    except Exception:

        print(
            "WARNING: Existing .cdsrc.json could not be parsed."
        )

        cdsrc_data = {}


requires = cdsrc_data.setdefault(
    "requires",
    {}
)

requires["db"] = {
    "kind": "sqlite",
    "credentials": {
        "database": "db/rippletrace.sqlite"
    }
}


with CDSRC.open(
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        cdsrc_data,
        f,
        indent=2
    )

    f.write("\n")


print("Updated .cdsrc.json")


# ------------------------------------------------------------
# CREATE DB DIRECTORY
# ------------------------------------------------------------

(ROOT / "db").mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# REMOVE OLD SQLITE DATABASE
# ------------------------------------------------------------

if DB_SQLITE.exists():

    print()
    print(
        f"Removing old database: {DB_SQLITE}"
    )

    DB_SQLITE.unlink()


# ------------------------------------------------------------
# COMPLETE
# ------------------------------------------------------------

print()
print("=" * 60)
print("DATABASE CONFIGURATION FIXED")
print("=" * 60)

print()
print("CAP will now use:")
print("  db/rippletrace.sqlite")

print()
print("IMPORTANT:")
print("The database must be initialized by cds watch.")

print()
print("Next commands:")
print("  cds watch")

print()
print("Then open:")
print("  http://localhost:4004/control-tower/")

print("=" * 60)
