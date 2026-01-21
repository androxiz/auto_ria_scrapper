# Auto RIA Scraper

A high-performance asynchronous web scraper for auto.ria.com that collects used and new car listings data and stores it in a PostgreSQL database.

## Overview

This application automatically scrapes car listings from auto.ria.com at scheduled times, extracts detailed information about each vehicle (price, odometer, seller info, VIN, images, etc.), stores the data in a PostgreSQL database, and creates database dumps for backup purposes.

## Features

- **Asynchronous Scraping**: Uses `aiohttp` for concurrent requests to handle multiple car listings efficiently
- **Scheduled Tasks**: APScheduler runs scraping and database dump operations at configurable times
- **Dual Scraper Support**: Handles both new auto and used auto listings with different XPath selectors
- **Data Extraction**: Extracts comprehensive car information including:
  - Title and price (in USD)
  - Odometer reading
  - Seller information and phone number
  - Car images and count
  - Car number and VIN
  - Direct URL to the listing
- **Database Persistence**: SQLAlchemy ORM with PostgreSQL backend for reliable data storage
- **Automated Backups**: Creates SQL dumps of the database at scheduled intervals
- **Docker Support**: Easy deployment using Docker and Docker Compose

## Project Structure

```
auto_ria_scrapper/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuration and settings management
│   ├── database.py               # Database engine and session setup
│   ├── main.py                   # Application entry point
│   ├── scheduler.py              # Task scheduling logic
│   ├── utils.py                  # Utility functions (parsing, regex)
│   ├── models/
│   │   ├── __init__.py
│   │   └── car.py                # Car database model
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── car_repository.py     # Database access layer for cars
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── detail.py             # Car detail page scraper
│   │   └── listing.py            # Car listing page scraper
│   └── services/
│       ├── __init__.py
│       ├── scraper_service.py    # Main scraping orchestration
│       └── dump_service.py       # Database dump functionality
├── docker/
│   └── Dockerfile                # Docker image definition
├── dumps/                        # Directory for SQL backup files
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
├── .env-example                  # Environment variables example
└── README.md                    
```

## Prerequisites

- **Python 3.11+** (if running locally without Docker)
- **Docker** and **Docker Compose** (recommended for easy setup)
- **PostgreSQL 15+** (included in Docker setup)
- Internet connection for scraping auto.ria.com

## Installation

### Option 1: Using Docker (Recommended)

1. **Clone or download the project**
   ```bash
   cd auto_ria_scrapper
   ```

2. **Ensure .env file is configured**
   ```bash
   cat .env  # Should contain database and app settings
   ```

3. **Build and start the application**
   ```bash
   docker-compose up --build
   ```

   The application will:
   - Build the Docker image
   - Start the PostgreSQL database
   - Initialize the database schema
   - Start the scraper with scheduled tasks

4. **Verify it's running**
   ```bash
   docker-compose ps
   ```

### Option 2: Local Python Installation

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL**
   - Ensure PostgreSQL is running locally
   - Create database and user or update .env with your credentials

4. **Configure environment variables**
   - Copy or create `.env` file with:
     ```env
     POSTGRES_DB=autoria
     POSTGRES_USER=autoria_user
     POSTGRES_PASSWORD=autoria_pass
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     
     START_URL=https://auto.ria.com/uk/car/used/
     SCRAPER_TIME=14:55
     DUMP_TIME=15:00
     ```

5. **Run the application**
   ```bash
   python -m app.main
   ```

## Configuration

### Environment Variables (.env file)

```env
# Database Configuration
POSTGRES_DB=autoria           # Database name
POSTGRES_USER=autoria_user    # Database user
POSTGRES_PASSWORD=autoria_pass # Database password
POSTGRES_HOST=db              # Host (use 'db' in Docker, 'localhost' locally)
POSTGRES_PORT=5432            # Database port

# Application Configuration
START_URL=https://auto.ria.com/uk/car/used/  # Starting URL for scraping
SCRAPER_TIME=14:55            # Time to run scraper (HH:MM format, Europe/Kyiv)
DUMP_TIME=15:00               # Time to dump database (HH:MM format, Europe/Kyiv)
```

### Key Components

- **config.py**: Loads environment variables and provides settings object
- **database.py**: Initializes SQLAlchemy engine and session factory
- **scheduler.py**: Configures APScheduler with two jobs:
  - Daily scraping at `SCRAPER_TIME`
  - Database dump at `DUMP_TIME`

## Running the Application

### With Docker Compose

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Remove all data (including database)
docker-compose down -v
```

### Locally

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the application
python -m app.main
```

The application will:
1. Initialize database tables (if they don't exist)
2. Start the APScheduler
3. Run scheduled tasks at configured times
4. Keep running and waiting for next scheduled execution

## Scheduled Tasks

The application uses APScheduler with cron triggers (timezone: Europe/Kyiv):

1. **Daily Scraper** (at `SCRAPER_TIME`)
   - Fetches car listings from auto.ria.com
   - Extracts detailed information for each car
   - Stores data in PostgreSQL database

2. **Database Dump** (at `DUMP_TIME`)
   - Creates SQL backup file in `dumps/` directory
   - Filename format: `autoria_YYYY-MM-DD_HH-MM-SS.sql`

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `aiohttp` | Asynchronous HTTP client for web scraping |
| `lxml` | HTML parsing and XPath queries |
| `SQLAlchemy` | ORM for database operations |
| `asyncpg` | Async PostgreSQL driver |
| `APScheduler` | Task scheduling |
| `python-dotenv` | Environment variable management |
