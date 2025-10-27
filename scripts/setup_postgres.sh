#!/bin/bash

echo "🐘 Setting up PostgreSQL for EE Research Scout..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL not found. Installing..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
fi

# Start PostgreSQL
echo "Starting PostgreSQL..."
sudo service postgresql start

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql << EOF
CREATE DATABASE ee_research_scout;
CREATE USER anonui WITH PASSWORD 'double007';
GRANT ALL PRIVILEGES ON DATABASE ee_research_scout TO anonui;
\q
EOF

echo "✅ PostgreSQL setup complete!"
echo ""
echo "Connection details:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: ee_research_scout"
echo "  User: ee_user"
echo "  Password: your_secure_password"
echo ""
echo "Add to .env file:"
echo "POSTGRES_USER=ee_user"
echo "POSTGRES_PASSWORD=your_secure_password"
echo "POSTGRES_HOST=localhost"
echo "POSTGRES_PORT=5432"
echo "POSTGRES_DB=ee_research_scout"
