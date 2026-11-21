# KhoAI - Smart Inventory Management & Demand Planning

KhoAI is a management and demand planning application designed for small and medium-sized retailers. It helps business owners make better inventory decisions by transforming historical sales data into demand forecasts, stock insights, and reorder recommendations.

## Project Team

| Member | Role |
| ------ | ---- |
| Chu Nguyen Khang | Project Manager, Data Scientist |
| Nguyen Ngoc Thanh Ha | UI/UX Designer, Frontend Developer |
| Bach Dinh Hien | Frontend Developer, Tester |
| Vu Dam Khanh Hung | Product Owner, Backend Developer |
| Ly Du Tuan | Backend Developer |

## Key Features

- **Inventory Management:** Track stock levels, manage products, and record inventory transactions.
- **Sales Management:** Record sales, monitor sales history, and automatically update inventory.
- **Demand Forecasting:** Analyze historical sales data to identify demand patterns and forecast future demand, including seasonal fluctuations.
- **Smart Order Recommendations:** Suggest reorder quantites based on forecasted demand and current stock levels.
- **Analytics Dashboard:** Visualize sales performance, inventory levels, and demand trends.
- **Data Import & Export:** Import and export inventory and sales data through CSV and Excel files.
- **Stock Alerts:** Indentify low-stock and overstock items.

## Tech Stack

**Frontend**

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

**Backend & Data Science**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

**Database & Deployment**

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://custom-icon-badges.demolab.com/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=aws&logoColor=white)

## Run locally

Install Docker with Compose. For first-time setup, run these commands from the
repository root to create `.env`, generate a local JWT signing secret, and
start the stack.

```sh
cp .env.example .env
printf '\nJWT_SECRET_KEY=%s\n' "$(openssl rand -hex 32)" >> .env
docker compose up --build
```

If you already have a local `.env`, add the JWT secret using the `printf`
command only if `JWT_SECRET_KEY` is missing. Reuse the same `.env` on later runs.

- Frontend: <http://localhost:5173>
- API docs: <http://localhost:8000/docs>
- API health: <http://localhost:5173/api/health> (through the Vite proxy)

Compose starts PostgreSQL, applies the Alembic migration, and then starts the API.
Run `docker compose down` to stop the stack while keeping local database data.
If ports are busy, set `FRONTEND_PORT` or `BACKEND_PORT` in `.env`.

`frontend/` is the React, TypeScript, Vite and Tailwind application.
`backend/app/` holds the FastAPI entry point and SQLAlchemy models.
`backend/migrations/` holds the PostgreSQL schema migrations.

The initial schema allows one Owner account per shop and enforces case-insensitive
email uniqueness. Signup should create the shop and its Owner in one transaction
and trim the email before saving it. Authentication and sessions are separate
implementation tasks. The Compose setup is for local development.
