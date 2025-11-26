# UVR (Ultimate Vocal Remover) Dockerized

## Source Code

All Python code under the `src` directory of this project comes from the official open-source project [Anjok07/ultimatevocalremovergui](https://github.com/Anjok07/ultimatevocalremovergui). This Docker environment only provides a containerized solution for its execution and was not developed by the author of this repository.

This project provides a Docker environment to run the Ultimate Vocal Remover GUI application, accelerated by NVIDIA GPUs.

## Prerequisites

-   NVIDIA GPU with corresponding drivers installed.
-   Docker Engine.
-   Docker Compose.
-   [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
-   A running X11 Server (standard on most Linux desktop environments).

## How to Run

1.  **Authorize X Server Connection**

    To allow the Docker container to display the GUI, you need to authorize it to access your host's X server. Execute the following command in your terminal:

    ```bash
    xhost +local:docker
    ```

    This command allows local Docker containers to connect to the X server.

2.  **Start the Application**

    Use Docker Compose to build and start the container. It's recommended to add the `--build` flag for the first launch.

    ```bash
    docker-compose up --build
    ```
    
    If the image has already been built, you can omit the `--build` flag in the future:
    
    ```bash
    docker-compose up
    ```

3.  **Stop the Application**

    When you are done, press `Ctrl+C` in the terminal where `docker-compose up` is running, and then execute the following command to properly shut down and remove the container:

    ```bash
    docker-compose down
    ```

4.  **Revoke X Server Authorization**

    For security reasons, it is recommended to revoke the authorization after stopping the container:

    ```bash
    xhost -local:docker
    ```

## `docker-compose.yml` Configuration Explained

The [`docker-compose.yml`](docker-compose.yml:1) file is pre-configured with all the necessary environment variables and volume mounts to run the GUI application inside the container:

-   `network_mode: host`: Allows the container to use the host's network stack directly, simplifying communication for X11 and PulseAudio.
-   `environment`:
    -   `DISPLAY=$DISPLAY`: Passes the host's `DISPLAY` variable to the container.
    -   `XAUTHORITY=/root/.Xauthority`: Informs the application inside the container where to find the X authentication file.
-   `volumes`:
    -   `/tmp/.X11-unix:/tmp/.X11-unix`: Mounts the X11 socket.
    -   `${XAUTHORITY:-$HOME/.Xauthority}:/root/.Xauthority`: Mounts the host's X authentication cookie into the container for the root user. This is crucial for the GUI to display correctly.
    -   `./volumes:/volumes`: Mounts a local folder for easily moving audio files into and out of the container.
    -   `./src:/app/src`: Mounts the source code for easier development and modification.