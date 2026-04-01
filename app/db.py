import os
import psycopg 

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            # Create the schema
            cur.execute("""
                -- sample parent table
                CREATE TABLE IF NOT EXISTS foo (
                    id SERIAL PRIMARY KEY, -- primary key
                    created_at TIMESTAMP DEFAULT now()
                );
                
                -- sample child table
                CREATE TABLE IF NOT EXISTS bar (
                    id SERIAL PRIMARY KEY,
                    foo_id INT REFERENCES foo(id), -- foreign key
                    created_at TIMESTAMP DEFAULT now()
                );

                -- adding columns after the fact
                ALTER TABLE foo ADD COLUMN IF NOT EXISTS name VARCHAR;
                ALTER TABLE foo ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT now()""")
            
            # insert sample data
            cur.execute("""INSERT INTO foo (name) VALUES ('test')""")

    except Exception as e:
        print(f"Error while creating schema: {e}")