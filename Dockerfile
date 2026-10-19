FROM python:3.14-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# model/artifacts is included only if you trained it locally (it is gitignored);
# without it the app still runs with the literature tools only.
COPY . .

RUN useradd --create-home app && chown -R app /app
USER app

EXPOSE 8501
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.headless=true"]
