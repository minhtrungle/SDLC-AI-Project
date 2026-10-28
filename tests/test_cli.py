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
