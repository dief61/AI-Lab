from service.db import get_connection


def test_delete_buyer_does_not_physically_delete(client, created_buyer):
    buyer_id = created_buyer["id"]
    resp = client.delete(f"/api/buyers/{buyer_id}")
    assert resp.status_code == 200

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM Buyer WHERE id = %s", (buyer_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    assert row is not None, "Buyer wurde physikalisch gelöscht – soll aber nur soft-deleted werden"


def test_deleted_buyer_not_in_default_list(client, created_buyer):
    buyer_id = created_buyer["id"]
    client.delete(f"/api/buyers/{buyer_id}")

    resp = client.get("/api/buyers")
    assert resp.status_code == 200
    ids = [b["id"] for b in resp.json()]
    assert buyer_id not in ids, "Gelöschter Buyer ist in der Standard-Liste sichtbar"


def test_deleted_buyer_visible_with_parameter(client, created_buyer):
    buyer_id = created_buyer["id"]
    client.delete(f"/api/buyers/{buyer_id}")

    resp = client.get("/api/buyers?geloescht=1")
    assert resp.status_code == 200
    ids = [b["id"] for b in resp.json()]
    assert buyer_id in ids, "Gelöschter Buyer ist nicht sichtbar mit ?geloescht=1"


def test_deleted_buyer_has_geloescht_flag(client, created_buyer):
    buyer_id = created_buyer["id"]
    client.delete(f"/api/buyers/{buyer_id}")

    resp = client.get(f"/api/buyers/{buyer_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("geloescht") is True, "geloescht-Flag fehlt oder ist nicht True"


def test_deleted_buyer_has_geloescht_am_timestamp(client, created_buyer):
    buyer_id = created_buyer["id"]
    client.delete(f"/api/buyers/{buyer_id}")

    resp = client.get(f"/api/buyers/{buyer_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("geloescht_am") is not None, "geloescht_am-Timestamp fehlt"


def test_list_deleted_buyers_shows_timestamp(client, created_buyer):
    buyer_id = created_buyer["id"]
    client.delete(f"/api/buyers/{buyer_id}")

    resp = client.get("/api/buyers?geloescht=1")
    assert resp.status_code == 200
    buyer = next((b for b in resp.json() if b["id"] == buyer_id), None)
    assert buyer is not None
    assert buyer.get("geloescht") is True
    assert buyer.get("geloescht_am") is not None


def test_create_buyer_has_geloescht_false(client, test_buyer_data):
    resp = client.post("/api/buyers", json=test_buyer_data)
    assert resp.status_code == 201
    data = resp.json()
    assert data.get("geloescht") is False


def test_double_delete_returns_ok(client, created_buyer):
    buyer_id = created_buyer["id"]
    resp1 = client.delete(f"/api/buyers/{buyer_id}")
    assert resp1.status_code == 200

    resp2 = client.delete(f"/api/buyers/{buyer_id}")
    assert resp2.status_code == 200


def test_get_deleted_buyer_by_id_returns_full_data(client, created_buyer):
    buyer_id = created_buyer["id"]
    client.delete(f"/api/buyers/{buyer_id}")

    resp = client.get(f"/api/buyers/{buyer_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == created_buyer["name"]
    assert data["email"] == created_buyer["email"]
