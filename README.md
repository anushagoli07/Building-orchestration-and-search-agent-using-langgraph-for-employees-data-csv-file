# Payroll LangGraph Agent

This project parses payroll questions with Gemini, filters the employee CSV, and reports matching records through a LangGraph pipeline.

## Project layout

- `app/data.py`: employee data generation and loading
- `app/agents.py`: query parsing and employee search agents
- `app/graph.py`: LangGraph construction
- `app/cli.py`: interactive command-line interface
- `main.py`: application entrypoint
- `generate_csv.py`: explicit dataset generation command

## Run

Generate the dataset when needed:

```powershell
uv run python generate_csv.py
```

Start the interactive agent:

```powershell
uv run python main.py
```

Type `exit` or `quit` to stop the application.

Run tests:

```powershell
uv run python -m unittest discover -s tests -v
```
