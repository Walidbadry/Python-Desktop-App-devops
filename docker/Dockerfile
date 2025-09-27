FROM python:latist

WORKDIR /app

COPY app/ /app/

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt pyinstaller

# Build executable
RUN pyinstaller --onefile app.py

CMD ["./dist/app"]
