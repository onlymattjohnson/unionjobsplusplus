CREATE TABLE employer (
    id INTEGER PRIMARY KEY,
    employer_name TEXT NOT NULL,
    employer_subname TEXT,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    date_modified DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TRIGGER employer_date_modified AFTER UPDATE ON employer
    BEGIN
        update employer SET date_modified = datetime('now');
    END;

CREATE TABLE job (
    id INTEGER PRIMARY KEY,
    union_jobs_id INTEGER,
    employer_id INTEGER,
    job_title TEXT NOT NULL,
    job_location TEXT,
    job_based_in TEXT,
    is_remote_eligible INTEGER NOT NULL DEFAULT 0,
    remote_text TEXT,
    job_summary TEXT NOT NULL,
    job_link TEXT,
    job_page BLOB,
    job_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (employer_id) REFERENCES employer(id)
);