CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE conversation_turns (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    user_text TEXT,
    intent TEXT,
    result_text TEXT
);

CREATE TABLE daily_summaries (
    date DATE PRIMARY KEY,
    emotions JSONB,
    needs JSONB,
    complaints JSONB,
    recommendations JSONB
);

CREATE TABLE memory_chunks (
    id SERIAL PRIMARY KEY,
    kind TEXT,
    content TEXT,
    embedding vector(1536),
    meta JSONB
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    severity TEXT,
    message TEXT,
    meta JSONB
);
