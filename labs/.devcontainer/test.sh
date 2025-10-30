#!/bin/bash

# Test that conftest and terraform are properly installed in the devcontainer using podman

set -e

echo "Building devcontainer with podman..."

# Build the devcontainer image
podman build -t devcontainer-test .devcontainer/

echo "Testing conftest and terraform installation in devcontainer..."

# Run the container and test conftest
if podman run --rm devcontainer-test bash -c "
    set -e
    echo 'Testing conftest installation...'

    # Check if conftest command exists
    if ! command -v conftest &> /dev/null; then
        echo 'ERROR: conftest command not found'
        exit 1
    fi

    # Check if conftest is executable
    if ! conftest --version &> /dev/null; then
        echo 'ERROR: conftest is not executable or not working properly'
        exit 1
    fi

    # Display version for verification
    echo 'SUCCESS: conftest is properly installed'
    echo \"Version: \$(conftest --version)\"

    echo 'Testing terraform installation...'

    # Check if terraform command exists
    if ! command -v terraform &> /dev/null; then
        echo 'ERROR: terraform command not found'
        exit 1
    fi

    # Check if terraform is executable
    if ! terraform version &> /dev/null; then
        echo 'ERROR: terraform is not executable or not working properly'
        exit 1
    fi

    # Display version for verification
    echo 'SUCCESS: terraform is properly installed'
    echo \"Version: \$(terraform version)\"
"; then
    echo "Devcontainer test completed successfully!"
else
    echo "Devcontainer test failed!"
    exit 1
fi
