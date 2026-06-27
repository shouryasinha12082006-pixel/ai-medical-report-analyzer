CREATE DATABASE IF NOT EXISTS medical_analyzer;
USE medical_analyzer;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_pic VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_text LONGTEXT,
    summary TEXT,
    key_findings JSON,
    severity VARCHAR(50),
    alerts JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS settings (
    user_id INT PRIMARY KEY,
    theme VARCHAR(50) DEFAULT 'light',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
