-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- User table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT,
    qualification TEXT,
    dob DATE
);

-- Subject table
CREATE TABLE IF NOT EXISTS subject (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- Chapter table
CREATE TABLE IF NOT EXISTS chapter (
    id INTEGER PRIMARY KEY,
    subject_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (subject_id) REFERENCES subject (id)
);

-- Quiz table
CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY,
    chapter_id INTEGER,
    date_of_quiz DATE,
    time_duration TIME,
    remarks TEXT,
    FOREIGN KEY (chapter_id) REFERENCES chapter (id)
);

-- Question table
CREATE TABLE IF NOT EXISTS question (
    id INTEGER PRIMARY KEY,
    quiz_id INTEGER,
    question_statement TEXT NOT NULL,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_option INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id)
);

-- Scores table
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    quiz_id INTEGER,
    user_id INTEGER,
    time_stamp_of_attempt TIMESTAMP,
    total_scored INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);
