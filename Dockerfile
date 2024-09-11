FROM python:3.11.5-slim-bullseye
WORKDIR /PaymentSystem
COPY requirements.txt /PaymentSystem/
RUN pip install --no-cache -r requirements.txt
COPY . /PaymentSystem/
CMD ["python", "-m", "app"]