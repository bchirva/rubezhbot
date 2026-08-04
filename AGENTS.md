# Rubezh VK Bot

## Commands

- Install dependencies: `poetry install`.
- Run all tests: `poetry run pytest`.
- Format: `poetry run black src tests`.
- Lint: `poetry run pylint src tests`.
- Start locally: `poetry run python -m src.main`.
- Start the container: `docker compose up --build`.

## Application Structure

- `src/main.py` imports `chat_actions` and `side_actions` for decorator side effects. New handlers must be exported from the corresponding package `__init__.py`, or they will not be registered.
- `src.app` owns the shared route labeler, state dispenser, and VK API clients. Reuse these objects in handlers instead of creating clients locally.
- This is a Poetry project in non-package mode; source modules are imported directly as `src.*`.

## Configuration

- `src.config` validates `VK_BOT_KEY`, `VK_GROUP_KEY`, `VK_GROUP_ID`, and `VK_LIKES_REPORT_CHAT_ID` during import, and exits when any is missing or invalid.
- Keep credentials in the ignored `.env` file. Docker Compose loads that file for the bot container.

## Tests

- Chat-action tests must stay independent of VK credentials and API calls. `tests/conftest.py` replaces `src.app` and `vkbottle` with test doubles before action modules import.
- Use `make_message()` for messages, `monkeypatch` to make `random.randint` deterministic, `asyncio.run()` for handlers, and `AsyncMock` assertions on `message.answer`.
