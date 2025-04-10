import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def get_names():
    # df1 = pd.read_csv("backend/data/femalenames.csv")
    # df2 = pd.read_csv("backend/data/malenames.csv")

    # names: list[str] = list(
    #     set(df1["name"].dropna().tolist() + df2["name"].dropna().tolist()))
    processed_names = []
    # for name in names:
    #     parts = name.split()
    #     if len(parts) > 1:
    #         for part in parts:
    #             if part != "" and part.isalpha():
    #                 processed_names.append(part.lower())
    #     processed_names.append(name.lower())

    employee_names = get_employees_names()
    processed_names.extend(employee_names)
    return processed_names


def get_employees_names():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name from employees")).fetchall()
        names = set()
        for tup in result:
            fullname = tup[0].lower()
            names.add(fullname)
        print(names)
        return list(names)


def get_project_codes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT code from projects")).fetchall()
        codes = set()
        for tup in result:
            code = tup[0].lower()
            codes.add(code)
        print(codes)
        return list(codes)
