#!/bin/bash

RUN_CONTAINER=false
BUILD_CONTAINER=false
TAG_CONTAINER=false
PUSH_CONTAINER=false
HOST=""

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
            shift
            ;;
        -p|--push)
            PUSH_CONTAINER=true
            shift
            ;;
        -h|--host)
            HOST="$2"
            shift 2
            ;;
        *)
            echo "Unknown option $1"
            echo "Usage: $0 [-r|--run] [-b|--build] [-t|--tag] [-p|--push] [-h|--host <ip>:<port>]"
            exit 1
            ;;
    esac
done

if [ "$RUN_CONTAINER" = false ] && [ "$BUILD_CONTAINER" = false ] && [ "$TAG_CONTAINER" = false ] && [ "$PUSH_CONTAINER" = false ]; then
    echo "Error: Please provide at least one flag"
    echo "Usage: $0 [-r|--run] [-b|--build] [-t|--tag] [-p|--push] [-h|--host <ip>:<port>]"
    exit 1
fi

if [ "$TAG_CONTAINER" = true ] || [ "$PUSH_CONTAINER" = true ]; then
    if [ -z "$HOST" ]; then
        echo "Error: Host must be specified with -h or --host flag when using -t or -p"
        exit 1
    fi
fi

if command -v docker >/dev/null 2>&1; then
    echo "Docker is already installed"
else
    echo "Docker could not be found, installing..."
    
    apt update
    apt install -y docker.io
fi

if [ "$BUILD_CONTAINER" = true ]; then
    docker build -t cockatoo_edge:latest .
fi

if [ "$TAG_CONTAINER" = true ]; then
    echo "Tagging container as cockatoo_edge:latest for host $HOST..."
    docker tag cockatoo_edge:latest "$HOST/cockatoo_edge:latest"
fi

if [ "$PUSH_CONTAINER" = true ]; then
    echo "Pushing container to $HOST..."
    docker push "$HOST/cockatoo_edge:latest"
fi

if [ "$RUN_CONTAINER" = true ]; then
    echo "Running container..."
    docker run cockatoo_edge:latest
fi

if [ "$BUILD_CONTAINER" = true ] && [ "$RUN_CONTAINER" = false ]; then
    echo "Build complete. Use -r or --run flag to run the container."
fi