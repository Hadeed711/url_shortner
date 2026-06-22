from flask import Flask, request, redirect, render_template, jsonify
import redis
from shortener import generate_code
from config import REDIS_HOST, REDIS_PORT, URL_EXPIRY, BASE_URL

app = Flask(__name__)

# Redis connection — created once when app starts
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/")
def index():
    """Home page — renders the form."""
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    """Receive a long URL, store it in Redis, return the short URL."""
    long_url = request.form.get("url") or request.json.get("url", "")

    if not long_url:
        return jsonify({"error": "No URL provided"}), 400

    # Make sure URL has a scheme
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url

    code = generate_code(long_url)

    # Store: code → long_url, with expiry
    r.setex(code, URL_EXPIRY, long_url)

    short_url = f"{BASE_URL}/{code}"
    return jsonify({"short_url": short_url, "code": code})


@app.route("/<code>")
def redirect_url(code):
    """Look up the code in Redis and redirect to the original URL."""
    long_url = r.get(code)

    if long_url is None:
        return jsonify({"error": "Short URL not found or expired"}), 404

    return redirect(long_url, code=302)


if __name__ == "__main__":
    app.run(debug=True)