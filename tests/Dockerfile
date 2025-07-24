FROM python:3.12.2-slim

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY *.sh .
COPY *.py .
COPY *.html .
COPY . .


EXPOSE 5000

CMD ["tests/run_tests_assign_3.sh"]
#["pytest", "tests/"]
