import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from fastapi.testclient import TestClient
from service.main import app
from service.db import get_connection


@pytest.fixture(autouse=True)
def clean_buyers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Buyer")
    conn.commit()
    cur.close()
    conn.close()


@pytest.fixture
def test_buyer_data():
    return {
        "name": "KEGON AG",
        "strasse": "Kirchgasse 6",
        "plz": "65185",
        "ort": "Wiesbaden",
        "email": "rechnungseingang@kegon.de",
    }


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_buyer(client, test_buyer_data):
    resp = client.post("/api/buyers", json=test_buyer_data)
    assert resp.status_code == 201
    return resp.json()
