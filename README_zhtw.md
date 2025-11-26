# UVR (Ultimate Vocal Remover) Dockerized

## 程式碼來源 (Source Code)

本專案 `src` 目錄下的所有 Python 程式碼均來自官方開源專案 [Anjok07/ultimatevocalremovergui](https://github.com/Anjok07/ultimatevocalremovergui)。本 Docker 環境僅為其提供一個容器化的執行方案，並非由本人開發。

這個專案提供了一個 Docker 環境來執行 Ultimate Vocal Remover GUI 應用程式，並利用 NVIDIA GPU 進行加速。

## 需求 (Prerequisites)

- NVIDIA GPU 並已安裝對應的驅動程式。
- Docker Engine。
- Docker Compose。
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)。
- 一個正在運行的 X11 Server (大部分 Linux 桌面環境的標準配備)。

## 如何執行 (How to Run)

1.  **授權 X Server 連線 (Authorize X Server Connection)**

    為了讓 Docker 容器能夠顯示 GUI 介面，您需要授權容器存取您主機的 X server。請在終端機中執行以下指令：

    ```bash
    xhost +local:docker
    ```

    此指令會允許來自本機的 Docker 容器連線到 X server。

2.  **啟動應用程式 (Start the Application)**

    使用 Docker Compose 來建立並啟動容器。第一次啟動建議加上 `--build` 參數。

    ```bash
    docker-compose up --build
    ```
    
    如果映像檔已經建立過，未來可以省略 `--build` 參數：
    
    ```bash
    docker-compose up
    ```

3.  **停止應用程式 (Stop the Application)**

    當您使用完畢後，可以在執行 `docker-compose up` 的終端機按下 `Ctrl+C`，然後執行以下指令來確實關閉並移除容器：

    ```bash
    docker-compose down
    ```

4.  **撤銷 X Server 授權 (Revoke X Server Authorization)**

    基於安全考量，建議在關閉容器後，撤銷先前的授權：

    ```bash
    xhost -local:docker
    ```

## `docker-compose.yml` 設定說明

[`docker-compose.yml`](docker-compose.yml:1) 檔案已經設定好所有必要的環境變數與磁碟區掛載，以便在容器內運行 GUI 應用程式：

-   `network_mode: host`: 讓容器直接使用主機的網路，簡化 X11 與 PulseAudio 的通訊。
-   `environment`:
    -   `DISPLAY=$DISPLAY`: 將主機的 `DISPLAY` 變數傳遞給容器。
    -   `XAUTHORITY=/root/.Xauthority`: 告知容器內的應用程式 X 認證檔案的位置。
-   `volumes`:
    -   `/tmp/.X11-unix:/tmp/.X11-unix`: 掛載 X11 的 socket。
    -   `${XAUTHORITY:-$HOME/.Xauthority}:/root/.Xauthority`: 將主機的 X 認證 cookie 掛載到容器內，這是讓 GUI 正常顯示的關鍵。
    -   `./volumes:/volumes`: 掛載一個本地資料夾，方便您將音檔放入容器處理或從容器取出成果。
    -   `./src:/app/src`: 掛載原始碼，方便開發與修改。