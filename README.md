# 🏛️ Parliamentary Transparency & Conflict Monitor

An open-source intelligence portal that monitors public declarations, wealth details, cash balances, land holdings, gold weights, and corporate equity portfolios of Members of Parliament (MPs) in Nepal to detect conflicts of interest and track transparency indices.

---

## 🚀 Key Features

1. **Structured Wealth Matrix**:
   - Tracks cash balances (deposits, currencies, institutions).
   - Monitors land holdings in native Nepalese measurement systems: **Ropani-Aana-Paisa-Daam (RAPD)** for hilly regions, and **Bigha-Katha-Dhur (BKD)** for terai regions.
   - Measures gold, silver, and precious metals holdings in **Tolas**.
   - Captures corporate equity portfolios (promoter vs ordinary shares, market value, ownership percentage).

2. **FastAPI Backend Service**:
   - Python-based REST API engine serving serialized MP wealth profiles, query filters, and aggregated summary stats.
   - Built-in PostgreSQL integration with model definitions.

3. **React/Next.js Layout Framework**:
   - Modern web portal built with Next.js (TypeScript, Vanilla CSS modules) serving a dashboard on host port `3002`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy/SQLModel, Uvicorn
- **Database**: PostgreSQL 15+ (Alpine)
- **Frontend**: React 18+, Next.js 14+ (App Router, TypeScript, Vanilla CSS Modules)
- **Infrastructure**: Docker, Docker Compose

---

## ⚙️ Quick Start (Local Deployment)

### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### Build and Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kaji-maker/parliament-watch.git
   cd parliament-watch
   ```

2. **Spin up the services**:
   ```bash
   docker-compose up -d --build
   ```

3. **Verify running containers**:
   - **Frontend UI**: Open [http://localhost:3002](http://localhost:3002)
   - **Backend API**: Open [http://localhost:8002/docs](http://localhost:8002/docs)
   - **PostgreSQL**: Listening on localhost port `5434`
