from production_config import production_issues


def test_development_requires_no_production_flags():
    assert production_issues({}) == []
    assert production_issues({"EDUCYBER_ENV": "development"}) == []


def test_production_rejects_unsafe_defaults():
    issues = production_issues({"EDUCYBER_ENV": "production"})
    assert len(issues) >= 4
    assert any("CORS" in issue for issue in issues)
    assert any("TLS" in issue for issue in issues)
    assert any("backup" in issue for issue in issues)


def test_production_rejects_http_wildcards_and_localhost():
    for origin in ("http://example.com", "https://*.example.com",
                   "https://localhost:3000", "https://example.com/path"):
        issues = production_issues({
            "EDUCYBER_ENV": "production",
            "EDUCYBER_CORS_ORIGINS": origin,
            "DATABASE_URL": "postgresql+psycopg://user:pass@db.example.com/db?sslmode=require",
            "EDUCYBER_EDGE_RATE_LIMITING": "enabled",
            "EDUCYBER_BACKUP_VERIFIED": "yes",
        })
        assert any("CORS" in issue for issue in issues)


def test_production_accepts_explicit_minimum_configuration():
    assert production_issues({
        "EDUCYBER_ENV": "production",
        "EDUCYBER_CORS_ORIGINS": "https://educyber.example.org",
        "DATABASE_URL": "postgresql+psycopg://user:pass@db.example.org/db?sslmode=verify-full",
        "EDUCYBER_EDGE_RATE_LIMITING": "enabled",
        "EDUCYBER_BACKUP_VERIFIED": "yes",
    }) == []
