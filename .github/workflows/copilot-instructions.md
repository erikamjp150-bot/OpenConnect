# GitHub Copilot Agent Instructions for OpenConnect Development

## Project Context
OpenConnect is an open-source, wellness-first social networking platform.

## Core Principles
1. **Wellness-First**: Ranking should prioritize positive, helpful content over engagement.
2. **Privacy-First**: Data minimization, user-owned data, and no behavioral profiling.
3. **Transparent**: All code and ranking logic should be auditable.
4. **Decentralized**: End-to-end encrypted messaging via Matrix.

## Architecture
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (user data, posts) + Neo4j (social graph)
- **Ranking**: PyTorch (wellness-first model)
- **Messaging**: Matrix protocol
- **Frontend**: React (web) + React Native (mobile)
- **Storage**: MinIO (S3-compatible)

## Coding Standards
- Python: PEP 8, type hints, async/await, and Pydantic validation
- TypeScript: strict mode, functional components with hooks
- Testing: pytest for backend, Jest for frontend
- Documentation: docstrings and inline comments

## Key Components to Build
1. ✅ Database models
2. ✅ Auth routes
3. ✅ Feed ranking service
4. ✅ Graph service (Neo4j)
5. ✅ Frontend feed component
6. 🔜 Messaging service (Matrix integration)
7. 🔜 Moderation service (HITL)
8. 🔜 Mobile app (React Native)

## Common Patterns
- Use async/await for FastAPI routes
- Use httpx for external service calls
- Use Alembic for database migrations
- Use pytest-asyncio for async tests
