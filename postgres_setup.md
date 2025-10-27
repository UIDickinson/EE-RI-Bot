# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo service postgresql start

# Check status
sudo service postgresql status

# Switch to postgres user
sudo -i -u postgres

# Access PostgreSQL prompt
psql

# Create database and user
CREATE DATABASE ee_research_scout;
CREATE USER ee_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE ee_research_scout TO ee_user;

# Exit
\q
exit

# Pull PostgreSQL image
docker pull postgres:15-alpine

# Run PostgreSQL container
docker run --name ee-postgres \
  -e POSTGRES_PASSWORD=your_secure_password \
  -e POSTGRES_USER=ee_user \
  -e POSTGRES_DB=ee_research_scout \
  -p 5432:5432 \
  -v ee_postgres_data:/var/lib/postgresql/data \
  -d postgres:15-alpine

# Verify it's running
docker ps

# Access PostgreSQL
docker exec -it ee-postgres psql -U ee_user -d ee_research_scout