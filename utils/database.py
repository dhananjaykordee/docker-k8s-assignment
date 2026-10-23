import os
from pathlib import Path

import empressia_sqlalchemy_h2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL

JAVA_HOME = os.getenv("JAVA_HOME")
if JAVA_HOME:
    java_home_path = Path(JAVA_HOME).expanduser().resolve()
    if not java_home_path.is_dir():
        raise ValueError(f"JAVA_HOME does not exist: {java_home_path}")

    os.environ["JAVA_HOME"] = str(java_home_path)
    java_bin_path = str(java_home_path / "bin")
    os.environ["PATH"] = os.pathsep.join(
        [java_bin_path, os.environ.get("PATH", "")]
    )

H2_JAR_PATH = (
    Path(__file__).resolve().parent.parent / "libs" / "h2-2.2.224.jar"
).resolve()

engine = create_engine(DATABASE_URL, jars=[str(H2_JAR_PATH)])

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
