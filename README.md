# CallCenter AI

AI-powered call center recording analysis application built with Django and Gemini 2.5.

## Live Demo

https://call-center-analysis-1n74.onrender.com/

> Note: The application is deployed on Render. If the server has been inactive, it may take a few minutes to start. Please wait for a few minutes and refresh the page if it does not load immediately.

## Features

* Upload call recordings
* Supports MP4, MP3, WAV, M4A, OGG, AAC and FLAC
* AI-powered call analysis
* Automatic call summary
* Customer issue detection
* Resolution extraction
* Customer sentiment analysis
* Agent performance analysis
* Key topics extraction
* Action item extraction
* PDF report generation
* Call recording history
* Django admin panel
* PostgreSQL database
* Supabase Storage

## Tech Stack

* Python
* Django
* PostgreSQL
* Gemini 2.5
* Supabase Storage
* HTML
* CSS
* JavaScript

## Project Structure

```text
callcenter-ai/
├── calls/
├── callcenter_ai/
├── static/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## How It Works

1. Upload a call recording.
2. The recording is stored using Supabase Storage.
3. Gemini 2.5 analyzes the call.
4. The application extracts the summary, issue, resolution, sentiment, agent performance, topics and action items.
5. The analysis can be viewed and downloaded as a PDF report.

## Download and Run Locally

You can download the project by clicking **Code → Download ZIP** on the GitHub repository.

After downloading, extract the ZIP file and open the project folder in a terminal.

```bash
cd callcenter-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

Create a `.env` file using `.env.example` and add your Django, Gemini, PostgreSQL and Supabase credentials before running the application.

## Deployment

The application is deployed on Render:

https://call-center-analysis-1n74.onrender.com/

The first request may take a few minutes if the server is waking up. Please wait and refresh the page.
