import psycopg2
from app.database import engine, Base, SQLALCHEMY_DATABASE_URL

def create_all_tables():
    print("Executing SQLAlchemy Base.metadata.create_all...")
    Base.metadata.create_all(bind=engine)
    print("Tables created via SQLAlchemy ORM!")

    # Connect to PostgreSQL or SQLite based on database URL
    if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print("\n=== Created PostgreSQL Tables ===")
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
            count = cursor.fetchone()[0]
            print(f"  [✓] {table:<30} ({count} rows)")

        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_all_tables()

