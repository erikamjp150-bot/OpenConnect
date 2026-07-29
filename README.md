# OpenConnect

**An open-source, wellness-first alternative to Meta/Facebook**

## Mission

To build a social platform that prioritizes human wellbeing over engagement metrics. OpenConnect is designed to foster meaningful connections without the addictive design patterns that characterize mainstream platforms.

## Key Features

- **Wellness-First Feed**: Ranking algorithm that prioritizes positive, enriching content
- **Privacy-First**: No behavioral tracking, data minimization, user-owned data
- **Decentralized Messaging**: Matrix protocol for E2E encrypted communication
- **Community-Governed**: Transparent moderation and governance
- **Open Architecture**: Fully auditable code and ranking logic

## Architecture

```text
User → Frontend (React) → Backend API (FastAPI)
                            ↓
                    PostgreSQL (Users, Posts)
                    Neo4j (Social Graph)
                    KeyDB (Cache)
                    MinIO (Media)
                    Matrix (Messaging)
                    PyTorch (Ranking)
```

## Tech Stack

- **Backend**: FastAPI (Python), PostgreSQL, Neo4j
- **Feed Ranking**: PyTorch (wellness-first model)
- **Messaging**: Matrix protocol (decentralized)
- **Frontend**: React (web) + React Native (mobile)
- **Storage**: MinIO (S3-compatible)
- **Cache**: KeyDB/Redis

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, coding standards, and pull request expectations.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Quick Start

```bash
# Clone and set up
git clone https://github.com/erikamjp150-bot/OpenConnect.git
cd OpenConnect
cp .env.example .env

# Start infrastructure
docker-compose up -d

# Run backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Run frontend
cd ../frontend/web
npm install
npm start
