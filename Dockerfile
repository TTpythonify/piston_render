FROM ubuntu:22.04

# Install languages
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    nodejs npm \
    openjdk-17-jdk \
    gcc g++ \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENV PORT=8000

CMD ["python3", "app.py"]
