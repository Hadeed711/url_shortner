import json


def test_home_page_loads(client):
    """GET / should return 200 and show the HTML form."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"URL Shortener" in response.data


def test_shorten_returns_short_url(client):
    """POST /shorten with a valid URL must return a short_url."""
    response = client.post(
        "/shorten",
        data=json.dumps({"url": "https://example.com"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "short_url" in data
    assert "code" in data
    assert len(data["code"]) == 6


def test_shorten_adds_https_if_missing(client):
    """URLs without a scheme should get https:// prepended."""
    response = client.post(
        "/shorten",
        data=json.dumps({"url": "example.com"}),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_shorten_empty_url_returns_400(client):
    """POST /shorten with no URL must return 400 bad request."""
    response = client.post(
        "/shorten",
        data=json.dumps({"url": ""}),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_redirect_follows_short_code(client):
    """GET /<code> should redirect to the original long URL."""
    # First shorten a URL
    post_res = client.post(
        "/shorten",
        data=json.dumps({"url": "https://github.com"}),
        content_type="application/json"
    )
    code = post_res.get_json()["code"]

    # Now follow the short link
    get_res = client.get(f"/{code}")
    assert get_res.status_code == 302
    assert get_res.headers["Location"] == "https://github.com"


def test_redirect_unknown_code_returns_404(client):
    """GET /<code> with a code that doesn't exist must return 404."""
    response = client.get("/zzzzzz")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_same_url_returns_same_code(client):
    """Shortening the same URL twice must return the same code."""
    url = "https://example.com/same"
    res1 = client.post("/shorten", data=json.dumps({"url": url}),
                       content_type="application/json")
    res2 = client.post("/shorten", data=json.dumps({"url": url}),
                       content_type="application/json")
    assert res1.get_json()["code"] == res2.get_json()["code"]