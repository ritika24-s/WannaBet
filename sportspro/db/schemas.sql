-- sports table
CREATE TABLE IF NOT EXISTS sports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL
);

-- events table
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL,
    type VARCHAR(255) NOT NULL, --  ENUM('preplay', 'inplay') 
    sport_id INT NOT NULL,
    sport VARCHAR(255) NOT NULL,
    status ENUM('Pending', 'Started', 'Ended', 'Cancelled') DEFAULT 'Pending' NOT NULL,
    scheduled_start DATETIME NOT NULL,
    actual_start DATETIME DEFAULT NULL,
    logos VARCHAR(511) DEFAULT NULL,
    FOREIGN KEY (sport_id) REFERENCES sports(id)
);

-- selections table
CREATE TABLE IF NOT EXISTS selections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    event_id INT NOT NULL,
    event VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN NOT NULL,
    outcome ENUM('Unsettled', 'Void', 'Lose', 'Win') NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);
