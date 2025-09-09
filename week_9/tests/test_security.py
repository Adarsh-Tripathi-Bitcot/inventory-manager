"""Integration tests for security layer (JWT + RBAC)."""

from datetime import datetime, timedelta, timezone
import jwt


def test_access_without_token_on_protected_route(client):
    """Protected route (POST /api/products) should reject requests with no token."""
    payload = {"product_id": 10, "product_name": "NoAuth", "quantity": 1, "price": 1.0}
    resp = client.post("/api/products", json=payload)
    assert resp.status_code == 401


def test_access_with_invalid_token(client):
    """Protected route should reject invalid tokens."""
    invalid_token = "this.is.not.valid"
    payload = {"product_id": 11, "product_name": "BadToken", "quantity": 1, "price": 1.0}
    resp = client.post(
        "/api/products",
        json=payload,
        headers={"Authorization": f"Bearer {invalid_token}"},
    )
    assert resp.status_code == 401


def test_access_with_expired_token(client, app):
    """Protected route should reject expired tokens (401)."""
    with app.app_context():
        expired = jwt.encode(
            {
                "sub": "1",
                "role": "staff",
                "iat": datetime.now(timezone.utc) - timedelta(hours=2),
                "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            },
            app.config["JWT_SECRET_KEY"],
            algorithm=app.config.get("JWT_ALGORITHM", "HS256"),
        )
    payload = {"product_id": 12, "product_name": "Expired", "quantity": 1, "price": 1.0}
    resp = client.post(
        "/api/products",
        json=payload,
        headers={"Authorization": f"Bearer {expired}"},
    )
    assert resp.status_code == 401


def test_staff_cannot_post_product(client, make_auth_headers):
    """A staff user attempting to POST should get 403 Forbidden."""
    staff_headers = make_auth_headers(role="staff", username="staff1", password="pw")
    payload = {"product_id": 13, "product_name": "Nope", "quantity": 1, "price": 1.0}
    resp = client.post("/api/products", json=payload, headers=staff_headers)
    assert resp.status_code == 403


def test_admin_can_delete_product(client, make_auth_headers):
    """An admin user can DELETE a product."""
    admin_headers = make_auth_headers(role="admin", username="admin1", password="pw")
    # Create a product as admin
    payload = {"product_id": 14, "product_name": "ToRemove", "quantity": 1, "price": 1.0}
    resp_create = client.post("/api/products", json=payload, headers=admin_headers)
    assert resp_create.status_code == 201, resp_create.json

    # Delete as admin
    resp_del = client.delete("/api/products/14", headers=admin_headers)
    assert resp_del.status_code == 200
    assert "deleted successfully" in resp_del.json.get("message", "").lower()


"""Tests for authentication and security routes."""

def test_register_and_login_success(client):
    """User can register and then login successfully."""
    r = client.post("/auth/register", json={"username": "alice", "password": "pw", "role": "staff"})
    assert r.status_code == 201
    # Match the actual returned message
    assert "created successfully" in r.json["message"].lower()


def test_register_duplicate_user(client):
    """Registering a duplicate user returns 409."""
    payload = {"username": "bob", "password": "pw", "role": "staff"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 409


def test_login_success(client):
    """Registered user can login successfully."""
    client.post("/auth/register", json={"username": "carol", "password": "pw", "role": "staff"})
    r = client.post("/auth/login", json={"username": "carol", "password": "pw"})
    assert r.status_code == 200
    # Check that access_token key exists in the JSON response
    assert "access_token" in r.json
    assert r.json["role"] == "staff"



def test_login_wrong_password(client):
    """Wrong password returns 401."""
    client.post("/auth/register", json={"username": "dave", "password": "pw", "role": "staff"})
    r = client.post("/auth/login", json={"username": "dave", "password": "wrong"})
    assert r.status_code == 401
