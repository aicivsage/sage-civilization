-- Health Gamification Database Schema
-- Version: 1.0
-- Description: Stores health metrics, scores, achievements, and audit logs

-- Health Metrics Table
-- Stores daily measurements from various sources
CREATE TABLE IF NOT EXISTS health_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,  -- ISO 8601 format: YYYY-MM-DD
    weight_kg REAL,              -- Weight in kilograms
    systolic_bp INTEGER,         -- Systolic blood pressure (mmHg)
    diastolic_bp INTEGER,        -- Diastolic blood pressure (mmHg)
    steps INTEGER,               -- Daily step count
    weight_source TEXT,          -- Source: 'renpho', 'manual'
    bp_source TEXT,              -- Source: 'renpho', 'manual'
    steps_source TEXT,           -- Source: 'google_fit', 'manual'
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Create index for faster date lookups
CREATE INDEX IF NOT EXISTS idx_health_metrics_date ON health_metrics(date DESC);

-- Health Scores Table
-- Stores daily scoring and running balance
CREATE TABLE IF NOT EXISTS health_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,  -- ISO 8601 format: YYYY-MM-DD
    weight_score REAL DEFAULT 0,      -- Score from weight (±10 points)
    bp_score REAL DEFAULT 0,          -- Score from blood pressure (±5 points)
    steps_score REAL DEFAULT 0,       -- Score from steps (0-10 points)
    total_daily_score REAL DEFAULT 0, -- Sum of all scores
    running_balance REAL DEFAULT 0,   -- Cumulative balance
    portfolio_usd REAL DEFAULT 0,     -- Portfolio value in USD
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (date) REFERENCES health_metrics(date)
);

-- Create index for faster date lookups
CREATE INDEX IF NOT EXISTS idx_health_scores_date ON health_scores(date DESC);

-- Achievements Table
-- Tracks milestones and badges earned
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    achievement_type TEXT NOT NULL,   -- Type: 'milestone', 'streak', 'perfect_day'
    achievement_name TEXT NOT NULL,   -- e.g., '7_day_streak', 'weight_goal_105kg'
    description TEXT,                 -- Human-readable description
    earned_date TEXT NOT NULL,        -- When achievement was unlocked
    points_awarded REAL DEFAULT 0,    -- Bonus points for achievement
    metadata TEXT,                    -- JSON blob for additional data
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Create index for achievement lookups
CREATE INDEX IF NOT EXISTS idx_achievements_date ON achievements(earned_date DESC);
CREATE INDEX IF NOT EXISTS idx_achievements_type ON achievements(achievement_type);

-- Audit Log Table
-- Tracks all database operations for transparency
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    operation TEXT NOT NULL,          -- 'INSERT', 'UPDATE', 'DELETE'
    table_name TEXT NOT NULL,         -- Which table was affected
    record_id INTEGER,                -- ID of affected record
    user_agent TEXT,                  -- Which component made the change
    details TEXT,                     -- JSON blob with change details
    success INTEGER DEFAULT 1         -- 1 for success, 0 for failure
);

-- Create index for audit log queries
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_table ON audit_log(table_name);

-- Trigger: Update updated_at on health_metrics
CREATE TRIGGER IF NOT EXISTS update_health_metrics_timestamp
    AFTER UPDATE ON health_metrics
    FOR EACH ROW
BEGIN
    UPDATE health_metrics SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Initial configuration record (optional)
-- Stores system configuration and thresholds
CREATE TABLE IF NOT EXISTS system_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Insert default configuration
INSERT OR IGNORE INTO system_config (key, value, description) VALUES
    ('target_weight_kg', '105', 'Target weight in kilograms'),
    ('baseline_weight_kg', '115', 'Baseline starting weight'),
    ('target_systolic', '120', 'Target systolic blood pressure'),
    ('target_diastolic', '80', 'Target diastolic blood pressure'),
    ('daily_steps_goal', '10000', 'Daily steps goal'),
    ('portfolio_per_point', '1.00', 'USD per health point invested'),
    ('db_version', '1.0', 'Database schema version');
