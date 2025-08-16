# Shopify Insights

Shopify Insights is a full-stack application for extracting, analyzing, and presenting e-commerce website insights such as catalog details, contact information, and key links.

## Features

* Input any website URL and generate structured insights.
* Catalog visualization with clean, responsive UI.
* Contact and metadata extraction (phones, emails, links).
* Backend API (FastAPI) for scraping and serving insights.
* Frontend (React + Vite + Tailwind + shadcn/ui) for displaying insights.

## Tech Stack

* **Backend:** FastAPI (Python), BeautifulSoup, Requests
* **Frontend:** React, Vite, TailwindCSS, shadcn/ui
* **Package Manager:** npm / yarn
* **Version Control:** Git + GitHub

## Getting Started

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### API Usage

POST request to extract insights:

```bash
curl -X POST http://localhost:8000/api/insights \
-H "Content-Type: application/json" \
-d '{"website_url": "https://memy.co.in", "persist": false, "include_competitors": false}'
```

### Folder Structure

```
shopify-insights/
│
├── backend/        # FastAPI server
│   ├── main.py
│   ├── requirements.txt
│
├── frontend/       # React + Vite app
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Catalog.jsx
│   │   │   ├── InsightsForm.jsx
│
└── README.md
```

## Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/awesome-feature`
3. Commit your changes: `git commit -m "Add awesome feature"`
4. Push to the branch: `git push origin feature/awesome-feature`
5. Create a Pull Request

## License

MIT
