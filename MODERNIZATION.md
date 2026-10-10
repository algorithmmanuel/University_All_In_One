# EduCyber Nigeria — modernization MVP

This branch introduces a **separate web-first prototype** alongside the untouched legacy Android application.

## Scope delivered
- Responsive Next.js/TypeScript landing page for three academies
- Academy pathway previews and an interactive cybersecurity safety quiz
- FastAPI health and academy catalogue endpoints
- No accounts, database, analytics, external AI calls or personal data collection in this prototype

## Run locally

**Web:** Install Node.js 20.9+ and run:

```bash
cd web
npm install
npm run dev
```

Open http://localhost:3000.

**API:** With Python 3.11+:

```bash
cd api
python -m venv .venv
# Activate your virtual environment
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000/docs. The frontend currently uses local preview data, not the API; integration is a follow-up task.

## Next implementation milestones
1. Validate legacy app functionality and content licensing; review Firebase rules and committed configuration.
2. Introduce PostgreSQL migrations, a secure authentication provider, RBAC and protected teacher workflows.
3. Define curriculum mappings (NERDC / relevant exam syllabuses / institution-specific tertiary courses), content provenance and editorial review.
4. Implement course CRUD, lesson reader, quizzes, progress persistence and moderation.
5. Add accessible PWA support and low-data/offline design.
6. Add curriculum-grounded AI tutoring with citations, safety guardrails, rate limits and evaluation.
7. Add controlled cyber missions, CI security checks, tests and privacy compliance review before deployment.

**Security:** This prototype is not a production LMS. Do not accept real student data until authentication, access controls, privacy notices, data retention and child safety requirements have been implemented and tested.
