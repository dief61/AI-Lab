CREATE TABLE Seller (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    strasse TEXT NOT NULL,
    plz TEXT NOT NULL,
    ort TEXT NOT NULL,
    steuernummer TEXT NOT NULL,
    email TEXT NOT NULL
);

INSERT INTO Seller (name, strasse, plz, ort, steuernummer, email)
VALUES (
    'Dr. Michael Diefenbach',
    'Bad Sodener Straße 20',
    '65843',
    'Sulzbach',
    '046/812/01925',
    'mc.diefenbach@t-online.de'
);

CREATE TABLE Buyer (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    strasse TEXT NOT NULL,
    plz TEXT NOT NULL,
    ort TEXT NOT NULL,
    email TEXT NOT NULL,
    geloescht BOOLEAN NOT NULL DEFAULT FALSE,
    geloescht_am TIMESTAMP
);

INSERT INTO Buyer (name, strasse, plz, ort, email)
VALUES (
    'KEGON AG',
    'Kirchgasse 6',
    '65185',
    'Wiesbaden',
    'rechnungseingang@kegon.de'
);
