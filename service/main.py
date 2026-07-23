from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from service.db import get_connection

app = FastAPI(title="Hallo Welt API", description="A simple German greeting service", version="1.0.0")

app.mount("/ui", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def read_root():
    return {"message": "Hallo Welt"}


@app.get("/greeting")
def greeting(mood: str | None = Query(None, description="Optional mood parameter (gut/schlecht/other)")):
    default_response = "Hallo Welt! Wie geht es dir?"
    if not mood:
        return {"message": default_response}
    mood_lower = mood.lower()
    if mood_lower == "gut":
        response = "Das freut mich!"
    elif mood_lower == "schlecht":
        response = "Das tut mir leid."
    else:
        response = f"Hallo Welt! Du sagtest: '{mood}'. Wie geht es dir?"
    return {"message": response}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# --- Pydantic models ---

class SellerCreate(BaseModel):
    name: str
    strasse: str
    plz: str
    ort: str
    steuernummer: str
    email: str

class SellerUpdate(BaseModel):
    name: str | None = None
    strasse: str | None = None
    plz: str | None = None
    ort: str | None = None
    steuernummer: str | None = None
    email: str | None = None

class BuyerCreate(BaseModel):
    name: str
    strasse: str
    plz: str
    ort: str
    email: str

class BuyerUpdate(BaseModel):
    name: str | None = None
    strasse: str | None = None
    plz: str | None = None
    ort: str | None = None
    email: str | None = None


# --- Seller CRUD ---

@app.get("/api/sellers")
def list_sellers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, strasse, plz, ort, steuernummer, email FROM Seller ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "strasse": r[2], "plz": r[3], "ort": r[4], "steuernummer": r[5], "email": r[6]}
        for r in rows
    ]


@app.get("/api/sellers/{seller_id}")
def get_seller(seller_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, strasse, plz, ort, steuernummer, email FROM Seller WHERE id = %s", (seller_id,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    if not r:
        raise HTTPException(status_code=404, detail="Seller not found")
    return {"id": r[0], "name": r[1], "strasse": r[2], "plz": r[3], "ort": r[4], "steuernummer": r[5], "email": r[6]}


@app.post("/api/sellers", status_code=201)
def create_seller(seller: SellerCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Seller (name, strasse, plz, ort, steuernummer, email) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
        (seller.name, seller.strasse, seller.plz, seller.ort, seller.steuernummer, seller.email),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, **seller.model_dump()}


@app.put("/api/sellers/{seller_id}")
def update_seller(seller_id: int, seller: SellerUpdate):
    fields = seller.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    values = list(fields.values()) + [seller_id]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE Seller SET {set_clause} WHERE id = %s RETURNING id", values)
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Seller not found")
    return get_seller(seller_id)


@app.delete("/api/sellers/{seller_id}", status_code=204)
def delete_seller(seller_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Seller WHERE id = %s", (seller_id,))
    conn.commit()
    deleted = cur.rowcount
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Seller not found")


# --- Buyer CRUD ---

BUYER_COLUMNS = "id, name, strasse, plz, ort, email, geloescht, geloescht_am"

def _buyer_from_row(r):
    return {
        "id": r[0], "name": r[1], "strasse": r[2], "plz": r[3], "ort": r[4],
        "email": r[5], "geloescht": r[6],
        "geloescht_am": r[7].isoformat() if r[7] else None,
    }


@app.get("/api/buyers")
def list_buyers(geloescht: int = Query(0, description="0=aktive, 1=alle inkl. gelöschte")):
    conn = get_connection()
    cur = conn.cursor()
    if geloescht:
        cur.execute(f"SELECT {BUYER_COLUMNS} FROM Buyer ORDER BY id")
    else:
        cur.execute(f"SELECT {BUYER_COLUMNS} FROM Buyer WHERE geloescht = FALSE ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_buyer_from_row(r) for r in rows]


@app.get("/api/buyers/{buyer_id}")
def get_buyer(buyer_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT {BUYER_COLUMNS} FROM Buyer WHERE id = %s", (buyer_id,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    if not r:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return _buyer_from_row(r)


@app.post("/api/buyers", status_code=201)
def create_buyer(buyer: BuyerCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Buyer (name, strasse, plz, ort, email) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (buyer.name, buyer.strasse, buyer.plz, buyer.ort, buyer.email),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {**buyer.model_dump(), "id": new_id, "geloescht": False, "geloescht_am": None}


@app.put("/api/buyers/{buyer_id}")
def update_buyer(buyer_id: int, buyer: BuyerUpdate):
    fields = buyer.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    values = list(fields.values()) + [buyer_id]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE Buyer SET {set_clause} WHERE id = %s RETURNING id", values)
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return get_buyer(buyer_id)


@app.delete("/api/buyers/{buyer_id}")
def delete_buyer(buyer_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Buyer SET geloescht = TRUE, geloescht_am = NOW() WHERE id = %s RETURNING id",
        (buyer_id,),
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return get_buyer(buyer_id)


@app.put("/api/buyers/{buyer_id}/restore")
def restore_buyer(buyer_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Buyer SET geloescht = FALSE, geloescht_am = NULL WHERE id = %s RETURNING id",
        (buyer_id,),
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return get_buyer(buyer_id)


class RestoreBatch(BaseModel):
    ids: list[int]


@app.put("/api/buyers/restore")
def restore_buyers_batch(data: RestoreBatch):
    if not data.ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    conn = get_connection()
    cur = conn.cursor()
    placeholders = ", ".join("%s" for _ in data.ids)
    cur.execute(
        f"UPDATE Buyer SET geloescht = FALSE, geloescht_am = NULL WHERE id IN ({placeholders}) RETURNING id",
        data.ids,
    )
    restored = [r[0] for r in cur.fetchall()]
    conn.commit()
    cur.close()
    conn.close()
    return {"restored": restored}
