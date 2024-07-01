# Project README

## Overview

This project is a full-stack web application that consists of a Next.js frontend and a Django backend. The frontend provides a user interface for interacting with the backend, which offers various APIs and handles business logic. Docker and Docker Compose are used to manage the development environment, ensuring that both services run consistently across different environments.

## Project Structure

```
project-root/
│
├── backend/
│   ├── Dockerfile
│   ├── backend/  # Your Django project
│   ├── manage.py
│   └── ...  # Other backend files and directories
│
├── frontend/
│   ├── Dockerfile
│   ├── next.config.js
│   ├── src/
│   ├── package.json
│   └── ...  # Other frontend files and directories
│
├── compose.yml
└── README.md
```

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd project-root
```

### Environment Variables

Create a `.env` file in the root directory of the project and define the necessary environment variables for both frontend and backend.

Example for Django backend:
```
DJANGO_SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@db:5432/dbname
```

Example for Next.js frontend:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Build and Run the Containers

To build and run the containers for both frontend and backend, execute the following command:

```bash
docker-compose -f compose.yaml up --build
```

This command will:

- Build the Docker images for both the frontend and backend.
- Start the containers and set up the necessary services.

### Access the Application

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

## Development

### Frontend Development

To start the Next.js development server with hot-reloading:

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

To start the Django development server:

```bash
cd backend
pip install -r requirements/local.txt
python manage.py runserver
```

## Running Tests

### Frontend Tests

To run the frontend tests:

```bash
cd frontend
npm test
```

### Backend Tests

To run the backend tests:

```bash
cd backend
python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
