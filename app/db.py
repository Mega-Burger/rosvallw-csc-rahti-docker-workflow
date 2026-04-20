import os
import psycopg 

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                -- lägg till 
                   CREATE EXTENSION IF NOT EXISTS pgcrypto;
                        
                        
                CREATE TABLE IF NOT EXISTS hotel_guests (
                    id SERIAL PRIMARY KEY,
                    firstname VARCHAR NOT NULL,
                    lastname VARCHAR NOT NULL,
                    address VARCHAR
                );

                CREATE TABLE IF NOT EXISTS hotel_rooms (
                    id SERIAL PRIMARY KEY,
                    room_number INT NOT NULL,
                    type VARCHAR NOT NULL,
                    price NUMERIC NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS hotel_bookings (
                    id SERIAL PRIMARY KEY,
                    guest_id INT REFERENCES hotel_guests(id),
                    room_id INT REFERENCES hotel_rooms(id),
                    datefrom DATE NOT NULL,
                    dateto DATE NOT NULL,
                    addinfo VARCHAR
                );

            """)

            # Sample data — INSERT only if tables are empty
            cur.execute("SELECT COUNT(*) as c FROM hotel_rooms")
            if cur.fetchone()["c"] == 0:
                cur.execute("""
                    INSERT INTO hotel_rooms (room_number, type, price) VALUES
                    (101, 'single', 80),
                    (102, 'double', 120),
                    (103, 'suite', 200);
                """)

            cur.execute("SELECT COUNT(*) as c FROM hotel_guests")
            if cur.fetchone()["c"] == 0:
                cur.execute("""
                    INSERT INTO hotel_guests (firstname, lastname, address) VALUES
                    ('Anna', 'Korhonen', 'Helsinki'),
                    ('Mikael', 'Berg', 'Espoo');
                """)

    except Exception as e:
        print(f"Error while creating schema: {e}")