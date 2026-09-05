-- ==============================================================================
-- Portfolio Website Database Schema
-- Dharam Jai Vardhan Reddy | CSE Portfolio
-- Compatible with SQLite3 and easily adaptable to PostgreSQL
-- ==============================================================================

-- 1. Contact Messages Table
-- Stores user inquiries submitted through the contact form
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Use 'SERIAL PRIMARY KEY' in PostgreSQL
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast sorting and searching by date and email
CREATE INDEX IF NOT EXISTS idx_contact_created_at ON contact_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_contact_email ON contact_messages(email);

-- 2. Projects Table
-- Stores featured portfolio projects for dynamic rendering
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Use 'SERIAL PRIMARY KEY' in PostgreSQL
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    tags VARCHAR(200) NOT NULL,
    live_url VARCHAR(255),
    github_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Initial Seed Data for Projects (Dharam Jai Vardhan Reddy)
DELETE FROM projects;

INSERT INTO projects (title, description, tags, live_url, github_url)
VALUES 
(
    'Smart Parking System (Academic)',
    'An IoT-based web application featuring real-time slot monitoring, an analytics dashboard, and automated QR code ticket generation to prevent urban parking constraints.',
    'Flask,React,IoT/Sensors,Real-time Analytics',
    'https://jaivardhan.lovable.app/#projects',
    'https://github.com/sakuke123893-ai'
),
(
    'Procurement Intelligence System',
    'An AI-powered system designed to analyze supply options, streamline purchase flows, and optimize data handling processes within commercial software pipelines.',
    'Python,AI Integration,Flask,Data Pipelines',
    'https://jaivardhan.lovable.app/#projects',
    'https://github.com/sakuke123893-ai'
),
(
    'AWS Resume Analyzer',
    'A cloud-powered resume analysis tool that parses uploaded resumes, extracts key skills and insights, and scores them against role requirements using AWS services.',
    'AWS,Python,Cloud,Resume Parsing,NLP',
    'https://jaivardhan.lovable.app/#projects',
    'https://github.com/sakuke123893-ai'
);
