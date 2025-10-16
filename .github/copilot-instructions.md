# Copilot Instructions for SwarmMalackathon25

## Project Overview
This is a Dash web application for the Malackathon event. The project uses modern Python tooling with `uv` for dependency management and requires Python 3.13+.

## Architecture & Components
- **Entry Point**: `main.py` - Minimal Dash app with a single "Hello World" layout
- **Tech Stack**: Dash framework for interactive web dashboards, with Pandas for data processing and Bootstrap components for UI
- **Data Flow**: Currently bootstrapped; expect data processing with Pandas feeding into Dash visualizations

## Development Environment

### Package Management
- Uses **`uv`** (not pip/poetry) for dependency management - `uv.lock` is the lockfile
- Dependencies defined in `pyproject.toml` under `[project]` table
- Python version pinned to 3.13 (`.python-version`)

### Running the Application
```bash
# Install dependencies
uv sync

# Run the Dash app
uv run python main.py
```
The app runs in debug mode on default port (http://127.0.0.1:8050)

## Coding Conventions

### Dash Patterns
- Layout defined as a list (not `html.Div` wrapper): `app.layout = [html.Div(...)]`
- Debug mode enabled by default in `app.run(debug=True)`

### Dependencies
- Use `dash-bootstrap-components` for UI components (available but not yet used in `main.py`)
- Pandas available for data manipulation
- Add new dependencies via `uv add <package>` (not manual `pyproject.toml` edits)

## Key Files
- `main.py`: Application entry point and layout definition
- `pyproject.toml`: Project metadata and dependencies (managed by uv)
- `.python-version`: Enforces Python 3.13 for tooling consistency

## Important Notes
- This is an early-stage project - core dashboard functionality is yet to be implemented
- Expect integration of Pandas DataFrames with Dash DataTable/Graph components
- Bootstrap theming likely to be added via `dash-bootstrap-components`
