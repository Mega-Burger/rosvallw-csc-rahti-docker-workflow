from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.db import get_conn
from app.db import get_conn, create_schema

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: str
    dateto: str
    addinfo: str = None


app = FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# skapa databas schema
create_schema()


# tillfällig "databas" över rum
temp_rooms = [
    {"room_number": 101, "room_type": "double", "beds": 2, "price": 100},
    {"room_number": 102, "room_type": "single", "beds": 1, "price": 80},
    {"room_number": 103, "room_type": "triple", "beds": 3, "price": 120}
]

@app.get("/")
def read_root():
# testa databasanslutning
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(""" 
                SELECT'database connection ok' AS msg
                """)
        db_status = cur.fetchone()
    return { "msg": "Välkommen till hotellets bookningssystem", "v": "0.1" }

@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms")
        rooms = cur.fetchall()
    return rooms

@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (guest_id, room_id, datefrom, dateto, addinfo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (booking.guest_id, booking.room_id, booking.datefrom, booking.dateto, booking.addinfo))
        new_id = cur.fetchone()["id"]
    return {"msg": "Bokning skapad", "booking_id": new_id}

@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT hb.id, hr.room_number, hb.datefrom, hb.dateto
            FROM hotel_bookings hb
            JOIN hotel_rooms hr ON hb.room_id = hr.id
        """)
        bookings = cur.fetchall()
    return bookings
@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    
    return {"id": id, "q": q}

@app.get("/api/ip")
async def get_ip(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host

    return {"ip": ip}

