# Levers Assignment Solution

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Docker and Docker Compose on your machine.
- You are familiar with basic Docker operations and command line usage.

![deployment](https://github.com/reeshabhranjan/levers-assignment/blob/master/.github/workflows/main.yml/badge.svg)
![testing](https://github.com/reeshabhranjan/levers-assignment/blob/master/.github/workflows/tests.yml/badge.svg)

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing
purposes.

### Setup

To set up the project environment, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/reeshabhranjan/levers-assignment
   cd levers-assignment
   ```

2. **Create a `.env` file**
    ```bash
    cp .env.example .env
   
    ```
3. **Build and run the project**
   ```bash
    docker compose -f docker-compose.dev.yaml --env-file .env up --build -d
    ```

4. **Access the FastAPI server**

   The FastAPI server will be running at [http://localhost:8000](http://localhost:8000).

5. **Access the Swagger UI**

   The Swagger UI will be available at [http://localhost:8000/docs](http://localhost:8000/docs).


