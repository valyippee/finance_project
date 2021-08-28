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
    submission_id INTEGER PRIMARY KEY NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    selftext TEXT,
    title TEXT NOT NULL,
    stock_id INTEGER,
    CONSTRAINT fk_submission_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE TABLE comment (
    comment_id INTEGER PRIMARY KEY NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    body TEXT NOT NULL,
    score INTEGER NOT NULL,
    stock_id_body INTEGER,
    submission_id INTEGER,
    CONSTRAINT fk_comment_body_stock FOREIGN KEY (stock_id_body) REFERENCES stock (id),
    CONSTRAINT fk_comment_submission_stock FOREIGN KEY (submission_id) REFERENCES submission (submission_id)
);

CREATE TABLE mention (
    stock_id INTEGER,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);
