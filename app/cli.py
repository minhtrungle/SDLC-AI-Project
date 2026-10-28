"""CMP-12 Admin CLI — accounts, demo data, backup/restore, audit retention.

Usage:
    python -m app.cli create-user --username linh [--role user|manager] [--password ...]
    python -m app.cli seed-demo
    python -m app.cli backup <dir>
    python -m app.cli restore <dir>
    python -m app.cli prune-audit [--days 90]
"""

import argparse
import getpass
import secrets
import shutil
import sqlite3
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.auth import create_user
from app.config import Settings
from app.db import connect, init_schema

MIN_AUDIT_RETENTION_DAYS = 90  # NFR-007


def cmd_create_user(settings: Settings, args) -> int:
    password = args.password or getpass.getpass("Mật khẩu: ")
    if len(password) < 8:
        print("Mật khẩu phải có ít nhất 8 ký tự.", file=sys.stderr)
        return 2
    try:
        with connect(settings) as conn:
            create_user(conn, args.username, password, args.role)
    except sqlite3.IntegrityError:
        print(f"Tên đăng nhập '{args.username}' đã tồn tại.", file=sys.stderr)
        return 1
    print(f"Đã tạo người dùng '{args.username}' (vai trò {args.role}).")
    return 0


def cmd_seed_demo(settings: Settings, _args) -> int:
    created = []
    with connect(settings) as conn:
        for username, role in (("linh", "user"), ("hung", "manager")):
            if conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone():
                continue
            password = secrets.token_urlsafe(9)
            create_user(conn, username, password, role)
            created.append((username, role, password))
    for username, role, password in created:
        print(f"{username} ({role}) — mật khẩu: {password}")
    if not created:
        print("Người dùng demo đã tồn tại.")
    return 0


def cmd_backup(settings: Settings, args) -> int:
    target = Path(args.dir)
    target.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(settings.db_path)
    dst = sqlite3.connect(target / "cwd.db")
    try:
        src.backup(dst)  # consistent online copy even while the app is running
    finally:
        dst.close()
        src.close()
    files_target = target / "files"
    if files_target.exists():
        shutil.rmtree(files_target)
    shutil.copytree(settings.files_dir, files_target)
    print(f"Đã sao lưu vào {target}")
    return 0


def cmd_restore(settings: Settings, args) -> int:
    source = Path(args.dir)
    if not (source / "cwd.db").exists():
        print(f"Không tìm thấy {source / 'cwd.db'}", file=sys.stderr)
        return 1
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(source / "cwd.db")
    dst = sqlite3.connect(settings.db_path)
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    if settings.files_dir.exists():
        shutil.rmtree(settings.files_dir)
    shutil.copytree(source / "files", settings.files_dir)
    print(f"Đã khôi phục từ {source}")
    return 0


def cmd_prune_audit(settings: Settings, args) -> int:
    if args.days < MIN_AUDIT_RETENTION_DAYS:
        print(f"Phải giữ nhật ký tối thiểu {MIN_AUDIT_RETENTION_DAYS} ngày (NFR-007).", file=sys.stderr)
        return 2
    cutoff = (datetime.now(UTC) - timedelta(days=args.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect(settings) as conn:
        deleted = conn.execute("DELETE FROM audit_log WHERE created_at < ?", (cutoff,)).rowcount
    print(f"Đã xóa {deleted} bản ghi nhật ký cũ hơn {args.days} ngày.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m app.cli", description="Quản trị Chat với tài liệu")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create-user", help="Tạo tài khoản")
    p.add_argument("--username", required=True)
    p.add_argument("--role", choices=["user", "manager"], default="user")
    p.add_argument("--password", help="Bỏ trống để nhập ẩn")
    p.set_defaults(func=cmd_create_user)
    sub.add_parser("seed-demo", help="Tạo tài khoản demo linh/hung").set_defaults(func=cmd_seed_demo)
    p = sub.add_parser("backup", help="Sao lưu CSDL và file PDF")
    p.add_argument("dir")
    p.set_defaults(func=cmd_backup)
    p = sub.add_parser("restore", help="Khôi phục từ bản sao lưu")
    p.add_argument("dir")
    p.set_defaults(func=cmd_restore)
    p = sub.add_parser("prune-audit", help="Xóa nhật ký kiểm toán cũ")
    p.add_argument("--days", type=int, default=MIN_AUDIT_RETENTION_DAYS)
    p.set_defaults(func=cmd_prune_audit)
    return parser


def main(argv=None, settings: Settings | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = settings or Settings.from_env()
    if args.command != "restore":
        init_schema(settings)
    return args.func(settings, args)


if __name__ == "__main__":
    sys.exit(main())
