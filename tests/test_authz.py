def test_authorize_endpoint(client):
    # Simulate a GET request to the authorize endpoint
    response = client.get("/authz/oauth/authorize")
    assert response.status_code == 200
    assert b'<form method="post" action="/authz/oauth/authorize">' in response.data

    # Simulate a POST request to the authorize endpoint
    response = client.post("/authz/oauth/authorize")
    assert (
        response.status_code == 200 or response.status_code == 302
    )  # Depending on your redirect logic


def test_token_endpoint(client):
    # Simulate a POST request to the token endpoint
    response = client.post(
        "/authz/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": "test_code",
            "redirect_uri": "http://localhost/callback",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json
