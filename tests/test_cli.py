from app.cli import main
from app.config import Settings
from app.db import connect
from app.security import verify_password


def test_create_user_and_duplicate(tmp_path, capsys):
    s = Settings(data_dir=tmp_path / "d")
    assert (
        main(["create-user", "--username", "mai", "--role", "manager", "--password", "matkhau-123"], s) == 0
    )
    with connect(s) as conn:
        row = conn.execute("SELECT role, password_hash FROM users WHERE username='mai'").fetchone()
    assert row["role"] == "manager" and verify_password("matkhau-123", row["password_hash"])
    assert main(["create-user", "--username", "mai", "--password", "matkhau-123"], s) == 1
    assert "đã tồn tại" in capsys.readouterr().err


def test_create_user_rejects_short_password(tmp_path):
    s = Settings(data_dir=tmp_path / "d")
    assert main(["create-user", "--username", "mai", "--password", "ngan"], s) == 2


def test_seed_demo_is_idempotent(tmp_path, capsys):
    s = Settings(data_dir=tmp_path / "d")
    assert main(["seed-demo"], s) == 0
    out = capsys.readouterr().out
    assert "linh (user)" in out and "hung (manager)" in out
    assert main(["seed-demo"], s) == 0
    assert "đã tồn tại" in capsys.readouterr().out
    with connect(s) as conn:
        assert conn.execute("SELECT count(*) FROM users").fetchone()[0] == 2


def test_backup_and_restore_roundtrip(tmp_path, capsys):
    """NFR-006 / AC-025: restore from backup brings back users, documents and files."""
    from app.db import now_iso

    s = Settings(data_dir=tmp_path / "live")
    main(["create-user", "--username", "mai", "--password", "matkhau-123"], s)
    with connect(s) as conn:
        uid = conn.execute("SELECT id FROM users").fetchone()[0]
        conn.execute(
            "INSERT INTO documents (id, user_id, filename, size_bytes, status, created_at) "
            "VALUES ('d1', ?, 'a.pdf', 3, 'ready', ?)",
            (uid, now_iso()),
        )
    (s.files_dir / "d1.pdf").write_bytes(b"%PDF")
    assert main(["backup", str(tmp_path / "bk")], s) == 0

    restored = Settings(data_dir=tmp_path / "new")
    assert main(["restore", str(tmp_path / "bk")], restored) == 0
    with connect(restored) as conn:
        assert conn.execute("SELECT filename FROM documents").fetchone()[0] == "a.pdf"
        assert conn.execute("SELECT username FROM users").fetchone()[0] == "mai"
    assert (restored.files_dir / "d1.pdf").read_bytes() == b"%PDF"


def test_restore_missing_backup(tmp_path):
    assert main(["restore", str(tmp_path / "khong-co")], Settings(data_dir=tmp_path / "d")) == 1


def test_prune_audit_keeps_minimum_retention(tmp_path, capsys):
    """NFR-007: never fewer than 90 days; only older records are removed."""
    s = Settings(data_dir=tmp_path / "d")
    main(["seed-demo"], s)
    with connect(s) as conn:
        conn.execute(
            "INSERT INTO audit_log (action, created_at) VALUES ('auth.login_success', '2000-01-01T00:00:00Z')"
        )
        conn.execute(
            "INSERT INTO audit_log (action, created_at) VALUES ('auth.login_success', '2999-01-01T00:00:00Z')"
        )
    assert main(["prune-audit", "--days", "30"], s) == 2
    assert main(["prune-audit"], s) == 0
    with connect(s) as conn:
        assert [r[0] for r in conn.execute("SELECT created_at FROM audit_log")] == ["2999-01-01T00:00:00Z"]
