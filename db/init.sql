CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    name_variations TEXT[] NOT NULL
);

CREATE TABLE stock_price (
    stock_id INTEGER NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE TABLE submission (
    submission_id TEXT PRIMARY KEY NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    selftext TEXT,
    title TEXT NOT NULL
);

CREATE TABLE comment (
    comment_id TEXT PRIMARY KEY NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    body TEXT NOT NULL,
    score INTEGER NOT NULL,
    submission_id TEXT NOT NULL,
    CONSTRAINT fk_comment_submission_stock FOREIGN KEY (submission_id) REFERENCES submission (submission_id)
);

CREATE TABLE mention (
    mention_id SERIAL PRIMARY KEY,
    stock_id INTEGER,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    comment_id TEXT,
    submission_id TEXT,
    from_comment BOOLEAN,
    CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES stock (id),
    CONSTRAINT fk_mention_comment FOREIGN KEY (comment_id) REFERENCES comment (comment_id),
    CONSTRAINT fk_mention_submission FOREIGN KEY (submission_id) REFERENCES submission (submission_id)
);
