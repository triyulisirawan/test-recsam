# Speed Explorer V2 — Streamlit Online

Interactive speed simulator for elementary-school learners.

## Architecture

- `physics.py`: pure physics calculations.
- `config.py`: configurable limits.
- `app.py`: Streamlit UI + browser animation.
- JavaScript inside the visualization handles smooth real-time animation.
- Python remains the source of truth for distance, time, speed, and unit conversion.

## Local run

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
streamlit run app.py
```

## Test physics engine

```powershell
py test_physics.py
```

## Streamlit Community Cloud

Put the contents of this folder in a GitHub repository.

Required files at repository root:

```text
app.py
physics.py
config.py
requirements.txt
.streamlit/config.toml
```

Then deploy `app.py` from Streamlit Community Cloud.

## Design notes

The simulator uses a browser animation component for Play/Pause/Step/Reset. This avoids trying to animate the object by repeatedly rerunning Streamlit's Python script.

Play uses actual browser elapsed time.
Step advances exactly one simulation second.
The physical model is constant speed:
`v = s/t`
and
`position(t) = v*t`.
