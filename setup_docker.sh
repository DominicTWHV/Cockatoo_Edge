#!/bin/bash

RUN_CONTAINER=false
BUILD_CONTAINER=false
TAG_CONTAINER=false
PUSH_CONTAINER=false
CLEAN_CONTAINER=false
HOST=""

if [ -n "$CONTAINER_TAG" ]; then
    TAG="$CONTAINER_TAG"
elif [ -n "$TAG" ]; then
    TAG="$TAG"
else
    echo "[🐋] Error: Neither 'CONTAINER_TAG' nor 'TAG' environment variables are set."
    echo "      Please set one before running this script."
    exit 1
fi

validate_host() {
    if [[ ! "$1" =~ ^[a-zA-Z0-9.-]+(:[0-9]+)?$ ]]; then
        echo "[🐋] Error: Invalid host format '$1'. Use format: hostname[:port] or ip[:port]. Example: 192.168.1.1:5000 or registry.example.com"
        exit 1
    fi
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--run)
            RUN_CONTAINER=true
            shift
            ;;
        -b|--build)
            BUILD_CONTAINER=true
            shift
            ;;
        -t|--tag)
            TAG_CONTAINER=true
            if [[ $2 && $2 != -* ]]; then
                TAG="$2"
                shift 2
            else
                echo "[🐋] Warning: No tag name provided, using default $TAG"
                shift
            fi
            ;;
        -p|--push)
            PUSH_CONTAINER=true
            shift
            ;;
        -h|--host)
            if [[ -z "$2" || "$2" == -* ]]; then
                echo "[🐋] Error: --host requires a value"
                exit 1
            fi
            validate_host "$2"
            HOST="$2"
            shift 2
            ;;
        -c|--clean)
            CLEAN_CONTAINER=true
            docker image prune -a 
            shift
            ;;
        *)
            echo "[🐋] Unknown option $1"
            echo "[🐋] Usage: $0 [-r|--run] [-b|--build] [-t|--tag [tag_name]] [-p|--push] [-h|--host <ip>:<port>] [-c|--clean]"
            exit 1
            ;;
    esac
done

if [ "$RUN_CONTAINER" = false ] && [ "$BUILD_CONTAINER" = false ] && [ "$TAG_CONTAINER" = false ] && [ "$PUSH_CONTAINER" = false ] && [ "$CLEAN_CONTAINER" = false ]; then
    echo "[🐋] Error: Please provide at least one flag"
    echo "[🐋] Usage: $0 [-r|--run] [-b|--build] [-t|--tag [tag_name]] [-p|--push] [-h|--host <ip>:<port>] [-c|--clean]"
    exit 1
fi

if [ "$PUSH_CONTAINER" = true ]; then
    if [ -z "$HOST" ]; then
        echo "[🐋] Error: Host must be specified with -h or --host flag when using -p"
        exit 1
    fi
fi

if command -v docker >/dev/null 2>&1; then
    echo "[🐋] Docker is already installed"
else
    echo "[🐋] Docker could not be found, installing..."
    
    if [ "$EUID" -ne 0 ]; then
        echo "[🐋] Error: Docker installation requires root privileges. Please run with sudo."
        exit 1
    fi
    
    if ! apt update; then
        echo "[🐋] Error: Failed to update package list"
        exit 1
    fi
    
    if ! apt install -y docker.io; then
        echo "[🐋] Error: Failed to install Docker"
        exit 1
    fi
fi

if [ "$BUILD_CONTAINER" = true ]; then
    if [ ! -f "Dockerfile" ]; then
        echo "[🐋] Error: Dockerfile not found in current directory"
        exit 1
    fi
    
    if ! docker build -t "$TAG" .; then
        echo "[🐋] Error: Docker build failed"
        exit 1
    fi
fi

if [ "$TAG_CONTAINER" = true ] && [ "$BUILD_CONTAINER" = false ]; then
    if ! docker image inspect "$TAG" >/dev/null 2>&1; then
        echo "[🐋] Error: Image '$TAG' not found. Please build it first with -b flag."
        exit 1
    fi
fi

if [ "$PUSH_CONTAINER" = true ]; then
    REMOTE_TAG="$HOST/$TAG"

    if ! docker image inspect "$TAG" >/dev/null 2>&1; then
        echo "[🐋] Error: Image '$TAG' not found. Please build it first with -b flag."
        exit 1
    fi

    if [ "$TAG_CONTAINER" = false ]; then
        echo "[🐋] Warning: Tagging container for remote registry without -t flag. Using default tag $TAG."
    fi

    echo "[🐋] Tagging container for remote registry as $REMOTE_TAG..."
    if ! docker tag "$TAG" "$REMOTE_TAG"; then
        echo "[🐋] Error: Failed to tag container for remote registry"
        exit 1
    fi
    
    echo "[🐋] Pushing container to $HOST..."
    if ! docker push "$REMOTE_TAG"; then
        echo "[🐋] Error: Failed to push container to registry"
        exit 1
    fi
fi

if [ "$RUN_CONTAINER" = true ]; then
    echo "[🐋] Running container..."
    if ! docker run "$TAG"; then
        echo "[🐋] Error: Failed to run container"
        exit 1
    fi
fi

if [ "$BUILD_CONTAINER" = true ] && [ "$RUN_CONTAINER" = false ]; then
    echo "[🐋] Build complete. Use -r or --run flag to run the container."
fi