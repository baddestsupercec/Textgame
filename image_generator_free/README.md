# Installation
1. Follow [installation instructions](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running)
2. `source stable-diffusion-webui/venv/Scripts/activate` to activate venv

# Running the Server Locally
1. For webui: 
    - `python launch.py`. also `--share` to host on web.
2. For API:
    - `python launch.py --nowebui`

# Obtaining a Hosted API Url

1. Run
    - `python launch.py --nowebui --no-half`
2. Forward the local server to the internet
    - Using ngrok, `ngrok http http://127.0.0.1:7861`
3. Now use the provided hosted URL to launch the game.