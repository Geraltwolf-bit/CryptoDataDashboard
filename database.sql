CREATE TABLE dash(
    date DATE PRIMARY KEY,
    fear_greed_value VARCHAR(20) NOT NULL,
    fear_greed_index INT NOT NULL CHECK (value >= 0 AND value <= 100),
    inflation VARCHAR(20) NOT NULL,
    stockmarket VARCHAR(20) NOT NULL,
    timestamp_updated TIMESTAMPZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dash (date, fear_greed_value, fear_greed_index, inflation, stockmarket)
VALUES
    ('2025-10-02', 'Fear', 33, 'Moderate', 'Falling')
    ('2025-10-01', 'Greed', 75, 'Moderate', 'Fising')