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
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL,
    type ENUM('preplay', 'inplay') DEFAULT "preplay" NOT NULL,
    sport VARCHAR(255) NOT NULL,
    status ENUM("PENDING", "STARTED", "ENDED", "CANCELLED") DEFAULT 'PENDING' NOT NULL,
    scheduled_start DATETIME NOT NULL,
    actual_start DATETIME DEFAULT NULL,
    logos VARCHAR(511) DEFAULT NULL,
    FOREIGN KEY (sport) REFERENCES sports(name)
);

-- selections table
CREATE TABLE IF NOT EXISTS selections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    event VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN DEFAULT False,
    outcome ENUM('UNSETTLED', 'VOID', 'LOSE', 'WIN') NOT NULL,
    FOREIGN KEY (event) REFERENCES events(name)
);
