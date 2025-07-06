# RideMate - Ride Sharing Application

## Features
- Post ride offers with detailed information
- View available rides
- Auto-cancel rides that aren't booked after a set time

## Installation

1. Install the required package for cron jobs:
```
pip install django-crontab
```

2. Apply migrations:
```
python manage.py migrate
```

3. Set up scheduled tasks for auto-cancellation:
```
python manage.py crontab add
```

4. Check that the cron jobs are installed:
```
python manage.py crontab show
```

## Usage

The RideMate app allows users to:

1. Post rides with detailed information including:
   - Ride date and time
   - Pickup and drop-off locations
   - Price per seat
   - Vehicle information
   - Gender preferences
   - Additional notes

2. Browse available rides and contact ride offerers

3. Rides will automatically expire after the time specified by the ride offerer (by default 2 hours if not booked)

## Management Commands

To manually expire rides that have passed their expiration time, run:
```
python manage.py expire_rides
``` 