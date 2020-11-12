FROM python:3.8-slim

EXPOSE 8000
ENV PYTHONPATH=/app/password-resets

RUN apt-get update && apt-get install git -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm -f /requirements.txt

RUN git clone https://gitlab.gnome.org/Infrastructure/password-resets.git /app/password-resets && \
    git clone https://gitlab.gnome.org/Infrastructure/sysadmin-bin.git /app/password-resets/sysadmin-bin

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
