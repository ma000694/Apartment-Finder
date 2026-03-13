# Use the official Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (lets Docker cache this layer)
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Playwright's browser binaries
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy the rest of the project files into the container
COPY . .

# Default command to run the scraper
CMD ["python", "data-scraping/getinfo.py"]
```

---

**What each line does:**

`FROM python:3.11-slim` — starts from an official lightweight Python image. Everyone on the team will use the exact same Python version, no mismatches.

`WORKDIR /app` — sets `/app` as the working directory inside the container. All subsequent commands run from here.

`COPY requirements.txt .` — copies just the requirements file first. Docker caches each step, so if requirements haven't changed, it won't reinstall packages on every build — making rebuilds much faster.

`RUN pip install -r requirements.txt` — installs all Python packages including `playwright-stealth`.

`RUN playwright install chromium` — downloads Chromium browser binaries inside the container.

`RUN playwright install-deps chromium` — installs the system-level dependencies Chromium needs to run headlessly on Linux.

`COPY . .` — copies all your project files into the container.

`CMD [...]` — the default command that runs when the container starts.

---

Once you've created that file, also create a `.dockerignore` file in the same directory:
```
venv/
__pycache__/
*.pyc
.git/
.DS_Store
*.csv