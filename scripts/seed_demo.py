"""Inject additional synthetic data into the Postgres source for the demo.

Reads current max IDs, then appends N new customers / factures / ventes using
Faker with French locale. Books and categories are reused from the base seed.

Usage:
    python scripts/seed_demo.py --customers 50 --factures 200
"""
from __future__ import annotations

import argparse
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from faker import Faker

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

fake = Faker("fr_FR")
Faker.seed(42)
random.seed(42)


def conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        dbname=os.getenv("POSTGRES_DB", "bookshop_source"),
        user=os.getenv("POSTGRES_USER", "bookshop"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )


def max_id(cur, table: str) -> int:
    cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table}")
    return cur.fetchone()[0]


def random_date(start: datetime, end: datetime) -> str:
    delta = end - start
    d = start + timedelta(days=random.randint(0, delta.days))
    return d.strftime("%Y%m%d")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", type=int, default=50)
    parser.add_argument("--factures", type=int, default=200)
    args = parser.parse_args()

    start = datetime(2025, 1, 1)
    end = datetime(2026, 4, 30)

    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT id, prix_catalogue FROM books")
        books = cur.fetchall()
        if not books:
            raise SystemExit("No books found. Run the base seed first.")

        cust_offset = max_id(cur, "customers")
        fac_offset = max_id(cur, "factures")
        vente_offset = max_id(cur, "ventes")

        new_customers = []
        for i in range(1, args.customers + 1):
            cid = cust_offset + i
            new_customers.append((
                cid,
                f"CUST-{cid:04d}",
                fake.first_name(),
                fake.last_name(),
                fake.unique.email(),
                fake.city(),
                random.choice(["France", "Cameroun", "Senegal", "Cote d'Ivoire", "Belgique"]),
            ))
        cur.executemany(
            "INSERT INTO customers (id, code, first_name, last_name, email, city, country) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            new_customers,
        )

        customer_ids = [row[0] for row in new_customers]
        ventes_rows = []
        factures_rows = []

        for i in range(1, args.factures + 1):
            fid = fac_offset + i
            cust = random.choice(customer_ids)
            n_lines = random.randint(1, 4)
            date = random_date(start, end)
            total_qte = 0
            total_amount = 0.0
            lines = []
            for _ in range(n_lines):
                book_id, prix = random.choice(books)
                qte = random.randint(1, 3)
                pu = float(prix) * random.uniform(0.9, 1.0)
                total_qte += qte
                total_amount += pu * qte
                lines.append((book_id, round(pu, 2), qte))
            total_amount = round(total_amount, 2)
            paid_ratio = random.choices([1.0, 1.0, 1.0, 0.5, 0.0], k=1)[0]
            total_paid = round(total_amount * paid_ratio, 2)
            factures_rows.append((
                fid, cust, f"FAC-{fid:05d}", total_qte, total_amount, total_paid, date,
            ))
            for book_id, pu, qte in lines:
                vente_offset += 1
                ventes_rows.append((vente_offset, fid, book_id, pu, qte, date))

        cur.executemany(
            "INSERT INTO factures (id, customer_id, code, qte_totale, total_amount, total_paid, date_edit) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            factures_rows,
        )
        cur.executemany(
            "INSERT INTO ventes (id, facture_id, book_id, pu, qte, date_edit) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            ventes_rows,
        )
        c.commit()

    print(f"Inserted: {args.customers} customers, {args.factures} factures, {len(ventes_rows)} ventes.")


if __name__ == "__main__":
    main()
