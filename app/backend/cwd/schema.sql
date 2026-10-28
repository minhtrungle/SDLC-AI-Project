-- Chat với tài liệu — SQLite schema (data model: docs/04-design/data/model.md)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY,
    username      TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'manager')),
    created_at    TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token_hash   TEXT    PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    csrf_token   TEXT    NOT NULL,
    created_at   TEXT    NOT NULL,
    last_seen_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_sessions_user ON sessions(user_id);

CREATE TABLE IF NOT EXISTS documents (
    id            TEXT    PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename      TEXT    NOT NULL,
    size_bytes    INTEGER NOT NULL CHECK (size_bytes > 0),
    page_count    INTEGER,
    status        TEXT    NOT NULL CHECK (status IN ('processing', 'ready', 'failed', 'no_text')),
    error_code    TEXT,
    created_at    TEXT    NOT NULL,
    processed_at  TEXT
);
CREATE INDEX IF NOT EXISTS ix_documents_user_status ON documents(user_id, status);

CREATE TABLE IF NOT EXISTS chunks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- never reuse ids: citations keep chunk_id (DF-01)
    document_id TEXT    NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page        INTEGER NOT NULL CHECK (page >= 1),
    ord         INTEGER NOT NULL,
    text        TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_chunks_document ON chunks(document_id);

-- Full-text index over diacritic-folded chunk text; rowid = chunks.id (ADR-004).
-- `owner` ('u<user_id>') partitions the index so MATCH only scans one workspace (CR-09).
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    folded,
    owner,
    tokenize = 'unicode61 remove_diacritics 0'
);

CREATE TRIGGER IF NOT EXISTS trg_chunks_delete AFTER DELETE ON chunks BEGIN
    DELETE FROM chunks_fts WHERE rowid = old.id;
END;

CREATE TABLE IF NOT EXISTS conversations (
    id         TEXT    PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_conversations_user ON conversations(user_id);

CREATE TABLE IF NOT EXISTS turns (
    id              TEXT    PRIMARY KEY,
    conversation_id TEXT    NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    question        TEXT    NOT NULL,
    answer          TEXT    NOT NULL,
    outcome         TEXT    NOT NULL CHECK (outcome IN ('answered', 'not_found')),
    citations_json  TEXT    NOT NULL DEFAULT '[]',
    scope_json      TEXT,
    latency_ms      INTEGER NOT NULL,
    created_at      TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_turns_conversation ON turns(conversation_id, created_at);
CREATE INDEX IF NOT EXISTS ix_turns_created ON turns(created_at);

CREATE TABLE IF NOT EXISTS feedback (
    turn_id    TEXT    NOT NULL REFERENCES turns(id) ON DELETE CASCADE,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating     TEXT    NOT NULL CHECK (rating IN ('up', 'down')),
    reason     TEXT    CHECK (reason IS NULL OR length(reason) <= 500),
    created_at TEXT    NOT NULL,
    PRIMARY KEY (turn_id, user_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY,
    user_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    username   TEXT,
    action     TEXT    NOT NULL,
    target     TEXT,
    created_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_audit_created ON audit_log(created_at);
