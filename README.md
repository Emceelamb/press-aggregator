# Press aggregator

## Setup

1. Clone repository
2. Create virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `python install -r requirements.txt`
4. Switch to project directory: `cd pressAggregator`
5. Apply migrations: `python manage.py migrate`
6. Load database: `python manage.py scrape`
7. Start server: `python manage.py runserver`
