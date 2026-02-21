# PR Review MCP Server

> **AI-assisted code review tool for developers/AQA engineers**

A Python MCP (Model Context Protocol) server that connects Claude Desktop to GitHub Pull Requests. It fetches PR diffs, filters out binary and asset files (Unity `.meta`, images, audio, shaders, etc.), and gives Claude only the actual code to review.

Built as a QA automation tool to speed up pull request reviews using AI.


## Requirements

- Python 3.11+
- Claude Desktop

## Installation

```bash
git clone https://github.com/<your-username>/pr-review-mcp.git
cd pr-review-mcp
pip install -r requirements.txt
```

## First Run — Token Setup

Run the server once manually to store your GitHub token and repository in your OS keychain:

```bash
python server.py
```

You will be prompted for:

1. **GITHUB_TOKEN** — A GitHub Personal Access Token (classic) with `repo` scope. Generate one at [github.com/settings/tokens](https://github.com/settings/tokens).
2. **GITHUB_REPO** — The repository in `owner/repo` format (e.g. `octocat/Hello-World`).

Both values are stored securely in your OS keychain via the `keyring` library and will not be prompted again.

## Claude Desktop Configuration

Add the following to your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pr-review": {
      "command": "python",
      "args": ["C:\\path\\to\\pr-review-mcp\\server.py"]
    }
  }
}
```

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pr-review": {
      "command": "python",
      "args": ["/path/to/pr-review-mcp/server.py"]
    }
  }
}
```

After editing the config, **restart Claude Desktop**.

## Claude Code Configuration

Option A — CLI command:

```bash
claude mcp add pr-review -- python /path/to/pr-review-mcp/server.py
```

Option B — create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "pr-review": {
      "command": "python",
      "args": ["/path/to/pr-review-mcp/server.py"]
    }
  }
}
```

Then restart Claude Code.

## Usage

Once configured, Claude Desktop will have two new tools:

- **list_open_prs** — Lists open PRs in the configured repository.
- **get_pr_diff** — Fetches the code diff for a specific PR number, filtering out binary/asset files.

Example prompts in Claude Desktop:

- "List open PRs"
- "Review PR #42"
- "What changed in PR #15?"

## Reset Tokens

To clear stored credentials and re-enter them:

```bash
python server.py --reset
```

Then run `python server.py` again to enter new values.

## Architecture

```
Claude Desktop  ──MCP──▶  server.py  ──REST API──▶  GitHub
                              │
                         keyring (OS)
                         secure token storage
```

---

## Описание

MCP-сервер для автоматизации код-ревью пулл-реквестов с помощью Claude AI.

### Что это?

Это инструмент для QA-инженеров, который подключает Claude Desktop к GitHub и позволяет ИИ анализировать изменения в пулл-реквестах. Сервер автоматически фильтрует бинарные файлы и ассеты (Unity `.meta`, текстуры, аудио, шейдеры и т.д.), передавая Claude только код для ревью.

### Что умеет?

- **list_open_prs** — показать список открытых PR в репозитории
- **get_pr_diff** — получить diff конкретного PR с фильтрацией бинарных файлов

### Зачем?

- Ускоряет процесс код-ревью в QA
- ИИ проверяет код на типичные ошибки, проблемы безопасности, читаемость
- Фильтрует шум — бинарники, ассеты Unity, изображения не попадают в ревью
- Токен GitHub хранится безопасно в системном keychain (не в открытом виде)

### Требования

- Python 3.11+
- Claude Desktop

### Установка

```bash
git clone https://github.com/<your-username>/pr-review-mcp.git
cd pr-review-mcp
pip install -r requirements.txt
```

### Первый запуск — настройка токена

Запустите сервер вручную, чтобы сохранить токен и репозиторий в системный keychain:

```bash
python server.py
```

Вам будет предложено ввести:

1. **GITHUB_TOKEN** — Personal Access Token (classic) с правами `repo`. Создать можно здесь: [github.com/settings/tokens](https://github.com/settings/tokens).
2. **GITHUB_REPO** — Репозиторий в формате `owner/repo` (например `octocat/Hello-World`).

Оба значения сохраняются в системном keychain через библиотеку `keyring` и больше запрашиваться не будут.

### Настройка Claude Desktop

Добавьте в конфиг Claude Desktop:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pr-review": {
      "command": "python",
      "args": ["C:\\path\\to\\pr-review-mcp\\server.py"]
    }
  }
}
```

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pr-review": {
      "command": "python",
      "args": ["/path/to/pr-review-mcp/server.py"]
    }
  }
}
```

После изменения конфига **перезапустите Claude Desktop**.

### Настройка Claude Code

Вариант A — через CLI:

```bash
claude mcp add pr-review -- python /path/to/pr-review-mcp/server.py
```

Вариант B — создайте `.mcp.json` в корне проекта:

```json
{
  "mcpServers": {
    "pr-review": {
      "command": "python",
      "args": ["/path/to/pr-review-mcp/server.py"]
    }
  }
}
```

Затем перезапустите Claude Code.

### Использование

После настройки в Claude Desktop появятся два инструмента:

- **list_open_prs** — список открытых PR в репозитории
- **get_pr_diff** — diff конкретного PR с фильтрацией бинарных файлов

Примеры промптов:

- «Покажи открытые PR»
- «Сделай ревью PR #42»
- «Что изменилось в PR #15?»

### Сброс токенов

Чтобы удалить сохранённые данные и ввести заново:

```bash
python server.py --reset
```

Затем запустите `python server.py` снова для ввода новых значений.

### Структура проекта

```
pr-review-mcp/
├── server.py          — MCP-инструменты и точка входа
├── github_client.py   — авторизация и работа с GitHub API
├── file_filter.py     — правила фильтрации файлов по расширениям
├── requirements.txt   — зависимости
└── README.md
```

### Поддерживаемые расширения для ревью

`.cs`, `.json`, `.xml`, `.yaml`, `.yml`, `.md`, `.txt`, `.gradle`, `.java`, `.kt`, `.sh`, `.py`

### Игнорируемые файлы

`.meta`, `.prefab`, `.unity`, `.asset`, `.mat`, `.fbx`, `.png`, `.jpg`, `.shader`, `.dll`, `.mp3`, `.wav`, `.anim` и другие бинарные форматы.

---

## License

MIT
