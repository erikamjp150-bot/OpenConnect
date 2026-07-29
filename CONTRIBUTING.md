# Contributing to OpenConnect

Thank you for your interest in improving OpenConnect.

## Development Guidelines

- Keep the project wellness-first: prioritize humane, helpful, and transparent experiences.
- Prefer small, well-documented changes with clear intent.
- Follow the existing project structure and naming patterns.
- Write tests for new backend or frontend behavior whenever practical.

## Coding Standards

- Python: use PEP 8 style, type hints, and clear docstrings.
- TypeScript/JavaScript: prefer functional components, hooks, and strict typing where possible.
- Backend routes should use async/await patterns and validate inputs clearly.
- Keep ranking and moderation logic auditable and explainable.

## Pull Request Expectations

1. Describe the change clearly in the PR description.
2. Link any related issue or discussion.
3. Include relevant tests or validation steps.
4. Keep the diff focused on the requested improvement.

## Local Development

- Use Docker Compose for the core services when possible.
- Run backend tests with pytest and frontend checks with your existing toolchain.
- Document environment changes in the README or relevant config files.
