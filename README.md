# ApplyFlow

A full-stack job application tracker built as a portfolio project with **Vue 3 + TypeScript** and **Python/FastAPI**.

ApplyFlow helps job seekers keep applications organized, monitor pipeline status, and see quick application statistics from a single dashboard.

## Stack

### Frontend
- Vue 3
- TypeScript
- Vite
- Composition API
- Native Fetch API

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite for local development
- PostgreSQL-ready via `DATABASE_URL`

### Engineering
- REST API
- Docker / Docker Compose
- GitHub Actions CI
- Pytest backend tests
- TypeScript type checking
- Responsive UI

## Features

- Add, edit, and delete job applications
- Track status: Applied, Interview, Assessment, Offer, Rejected
- Record company, role, location, work setup, salary, URL, notes, and application date
- Filter applications by status
- Search by company or role
- Dashboard statistics
- Persistent database storage
- Health-check endpoint
- API tests
- Dockerized full-stack environment

## Run locally

### Backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend: http://localhost:8000  
API docs: http://localhost:8000/docs

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Environment

The frontend defaults to:

```
VITE_API_URL=http://localhost:8000
```

The backend defaults to local SQLite:

```
DATABASE_URL=sqlite:///./applyflow.db
```

You can switch to PostgreSQL by setting `DATABASE_URL`.

## Docker Compose

```bash
docker compose up --build
```

Then open http://localhost:5173.

## API endpoints

- `GET /api/health`
- `GET /api/applications`
- `POST /api/applications`
- `PUT /api/applications/{id}`
- `DELETE /api/applications/{id}`
- `GET /api/stats`

## Portfolio value

ApplyFlow demonstrates full-stack application architecture, typed frontend development, REST API design, CRUD operations, relational persistence, validation, automated testing, containerization, and CI.

## Future improvements

- Authentication
- Kanban drag-and-drop pipeline
- CSV import/export
- Follow-up reminders
- Resume version tracking
- Interview notes
- Analytics charts
- Cloud deployment

## License

MIT
