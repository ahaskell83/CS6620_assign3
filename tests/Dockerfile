FROM python:3.12.2-slim

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt


WORKDIR /CS6620_ASSIGN3

COPY ./ /CS6620_ASSIGN3

COPY *.sh .
COPY *.py .
COPY *.html .
COPY . .
COPY templates ./templates
COPY tests ./tests

EXPOSE 5000

CMD ["python", "-m", "pytest"]
#["sh", "-c", "python -m pytest"]
#["./run_assign_3.sh"]
