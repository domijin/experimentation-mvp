# Flask + GrowthBook E-Commerce MVP

A lightweight e-commerce demo showcasing self-hosted GrowthBook's A/B testing capabilities with two live experiments:
1. UI Color Scheme (light vs dark)
2. Item Link Behavior (same-tab vs new-tab)

## 🎯 Project Goals

- Demonstrate GrowthBook's feature flag capabilities in a self-hosted environment
- Show how to implement A/B testing in a Flask application
- Provide a simple, self-contained example that can be run locally
- No external dependencies or services required

## 🚀 Quick Start

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the self-hosted GrowthBook instance:
   ```bash
   docker-compose up -d growthbook
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Visit http://127.0.0.1:5000 in your browser

## 📋 Features

- Home page with:
  - Search bar (static input)
  - Spotlight gallery
  - Promotion banner
  - Featured item grid
- Item detail pages
- Two live experiments:
  - UI Color Scheme (light/dark)
  - Item Link Behavior (same-tab/new-tab)
- Simple event logging
- No database required (in-memory product data)
- Self-hosted GrowthBook instance

## 🛠️ Technical Stack

- Flask (Python web framework)
- Self-hosted GrowthBook (Feature flag & A/B testing)
- Jinja2 templates
- CSS variables for theming
- Docker (for GrowthBook instance)

## 📝 Implementation Plan

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for a detailed step-by-step guide on how to build this project.

## 🔍 Testing the Experiments

1. Open the site in two different incognito windows
2. You should see different combinations of:
   - Color scheme (light/dark)
   - Link behavior (same-tab/new-tab)
3. Check the console logs to see the experiment variations being applied

## 📊 Event Logging

The application logs events to the console and/or CSV file, including:
- Page views
- Experiment variations
- User interactions

## 🔮 Future Enhancements

- Add SQLite database for product storage
- Add more experiment variations
- Docker containerization for the entire stack
- Enhanced event logging and analytics 