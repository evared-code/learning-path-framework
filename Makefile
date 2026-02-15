.PHONY: help build up down restart logs test clean

help:
	@echo "Learning Path Framework - Make Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Build Docker containers"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View backend logs"
	@echo "  make test      - Run API tests"
	@echo "  make clean     - Remove containers and volumes"
	@echo "  make db        - Open database shell"
	@echo "  make backup    - Backup database"
	@echo ""

build:
	@echo "Building Docker containers..."
	docker-compose build

up:
	@echo "Starting services..."
	docker-compose up -d
	@echo "Waiting for backend to be ready..."
	@sleep 5
	@echo ""
	@echo "Services started!"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""

down:
	@echo "Stopping services..."
	docker-compose down

restart:
	@echo "Restarting services..."
	docker-compose restart

logs:
	docker-compose logs -f backend

test:
	@echo "Running tests..."
	@./test.sh http://localhost:8000

clean:
	@echo "Removing all containers, volumes, and data..."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		rm -rf data/; \
		echo "Cleaned!"; \
	fi

db:
	@echo "Opening database shell..."
	docker exec -it learning-path-backend sqlite3 /app/data/learning_paths.db

backup:
	@echo "Backing up database..."
	@mkdir -p backups
	docker cp learning-path-backend:/app/data/learning_paths.db backups/backup_$$(date +%Y%m%d_%H%M%S).db
	@echo "Backup saved to backups/"

status:
	@echo "Service status:"
	@docker-compose ps
