from shortener import generate_code


def test_generate_code_returns_6_chars():
    """Short code must always be exactly 6 characters."""
    code = generate_code("https://example.com")
    assert len(code) == 6


def test_generate_code_is_consistent():
    """Same URL must always produce the same code (deterministic)."""
    url = "https://example.com/page"
    assert generate_code(url) == generate_code(url)


def test_generate_code_different_urls_differ():
    """Different URLs must produce different codes."""
    code1 = generate_code("https://google.com")
    code2 = generate_code("https://github.com")
    assert code1 != code2


def test_generate_code_alphanumeric():
    """Code must only contain valid alphanumeric hex characters."""
    code = generate_code("https://example.com")
    assert code.isalnum()


def test_generate_code_handles_long_url():
    """Even very long URLs must produce a valid 6-char code."""
    long_url = "https://example.com/" + "a" * 2000
    code = generate_code(long_url)
    assert len(code) == 6