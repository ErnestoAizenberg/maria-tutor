#!/bin/bash

# Django-Tailwind Project Manager
# Usage: ./run.sh [command] [options]

# Configuration - adjust these paths as needed
TAILWIND_INPUT="main/static/src/css/input.css"
TAILWIND_OUTPUT="main/static/dist/css/styles.css"
TAILWIND_CONFIG="main/static/src/tailwind.config.js"
VENV_NAME="venv"  # Virtual environment name
PYTHON_CMD="python3"  # Change to 'python' if needed

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Main function
main() {
    case "$1" in
        tail|tailwind)
            compile_tailwind
            ;;
        run|server)
            run_server "$2"
            ;;
        migrate)
            django_migrate
            ;;
        makemigrations)
            django_makemigrations "$2"
            ;;
        createsuperuser)
            django_createsuperuser
            ;;
        shell)
            django_shell
            ;;
        test)
            run_tests "$2"
            ;;
        venv)
            manage_venv "$2"
            ;;
        clean)
            clean_project
            ;;
        logs)
            show_logs
            ;;
        backup)
            backup_db
            ;;
        install)
            install_dependencies
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Compile Tailwind CSS
compile_tailwind() {
    echo -e "${GREEN}Compiling Tailwind CSS...${NC}"
    npx tailwindcss@3.3.3 \
        -i "$TAILWIND_INPUT" \
        -o "$TAILWIND_OUTPUT" \
        --config "$TAILWIND_CONFIG" \
        --minify

    echo -e "${GREEN}Collecting static files...${NC}"
    $PYTHON_CMD manage.py collectstatic --noinput
}

# Run development server
run_server() {
    local port="${1:-8000}"
    echo -e "${GREEN}Starting Django development server on port $port...${NC}"
    $PYTHON_CMD manage.py runserver "$port"
}

# Django migrations
django_migrate() {
    echo -e "${GREEN}Running migrations...${NC}"
    $PYTHON_CMD manage.py migrate
}

django_makemigrations() {
    echo -e "${GREEN}Creating migrations...${NC}"
    if [ -z "$1" ]; then
        $PYTHON_CMD manage.py makemigrations
    else
        $PYTHON_CMD manage.py makemigrations "$1"
    fi
}

# Django superuser creation
django_createsuperuser() {
    echo -e "${GREEN}Creating superuser...${NC}"
    $PYTHON_CMD manage.py createsuperuser
}

# Django shell
django_shell() {
    echo -e "${GREEN}Starting Django shell...${NC}"
    $PYTHON_CMD manage.py shell
}

# Run tests
run_tests() {
    if [ -z "$1" ]; then
        echo -e "${GREEN}Running all tests...${NC}"
        $PYTHON_CMD manage.py test
    else
        echo -e "${GREEN}Running tests for $1...${NC}"
        $PYTHON_CMD manage.py test "$1"
    fi
}

# Virtual environment management
manage_venv() {
    case "$1" in
        create)
            echo -e "${GREEN}Creating virtual environment...${NC}"
            $PYTHON_CMD -m venv "$VENV_NAME"
            ;;
        activate)
            echo -e "${GREEN}Activating virtual environment...${NC}"
            source "$VENV_NAME/bin/activate"
            ;;
        install)
            echo -e "${GREEN}Installing requirements...${NC}"
            pip install -r requirements.txt
            ;;
        *)
            echo -e "${RED}Usage: ./run.sh venv [create|activate|install]${NC}"
            ;;
    esac
}

# Clean project
clean_project() {
    echo -e "${GREEN}Cleaning up...${NC}"
    # Remove Python cache files
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -delete

    # Remove other temporary files
    rm -f app.log settings.log

    echo -e "${YELLOW}Note: This doesn't delete your database or media files.${NC}"
}

# Show logs
show_logs() {
    echo -e "${GREEN}Showing logs...${NC}"
    tail -f app.log settings.log
}

# Backup database
backup_db() {
    local backup_file="db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"
    echo -e "${GREEN}Creating database backup: $backup_file...${NC}"
    cp db.sqlite3 "$backup_file"
}

# Install dependencies
install_dependencies() {
    echo -e "${GREEN}Installing Python dependencies...${NC}"
    pip install -r requirements.txt

    echo -e "${GREEN}Installing Node.js dependencies...${NC}"
    npm install tailwindcss@3.3.3
}

# Show help
show_help() {
    echo -e "${YELLOW}Django-Tailwind Project Manager${NC}"
    echo "Available commands:"
    echo "  tail, tailwind    - Compile Tailwind CSS and collect static files"
    echo "  run [port]        - Run development server (default: 8000)"
    echo "  migrate           - Run database migrations"
    echo "  makemigrations [app] - Create new migrations"
    echo "  createsuperuser   - Create a Django superuser"
    echo "  shell             - Start Django shell"
    echo "  test [app]        - Run tests"
    echo "  venv [cmd]        - Virtual environment management (create/activate/install)"
    echo "  clean             - Clean temporary files"
    echo "  logs              - Show logs"
    echo "  backup            - Backup database"
    echo "  install           - Install all dependencies"
    echo "  help              - Show this help message"
}

# Run main function with all arguments
main "$@"
