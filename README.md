# FastAPI Image Generation and Ad Creation Service


This service provides an API for generating images based on textual prompts using the StableDiffusionImg2ImgPipeline, and for creating advertisement images with added slogans, button texts, and logos.

## Features
- Generate new images based on textual prompts and initial images using AI models.
- Create advertisement images by combining generated images, slogans, logos, and button texts.

## Requirements
Before running the API, you must install the following:

- Python 3.8 or higher
- FastAPI
- Uvicorn (for serving the API)
- PIL (Python Imaging Library)
- diffusers (for image generation models)
- torch (PyTorch, required by diffusers)



## Installation
Clone the repository to your local machine:
```bash
git clone [repository_url]
cd [local_repository]
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
### On Windows:
```bash
py -3 -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```
### On Mac:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Service
With the virtual environment activated, you can start the service using Uvicorn:

```python
uvicorn main:app --host 0.0.0.0 --port 8000

```
Replace main with the name of your Python file if it's different.

## Environment Variables
To run this project, you need to add the following environment variable to your .env file:

HUGGING_FACE_TOKEN - This is your API token from Hugging Face which allows you to use the StableDiffusionImg2ImgPipeline
## API Reference

### Generate a new Image
```http
POST /generate-image/
```
Form Data Parameters:

* prompt (string): The text prompt for image generation.
* base_image (UploadFile): The base image file to be modified.

### Create an advertisement

```http
POST /create-ad/
```
Form Data Parameters:

- prompt (string): Text to guide the image generation process.
- color_hex (string): Hex code for the color used in the ad.
- punchline (string): The slogan text for the advertisement.
- button_text (string): Text for the call-to-action button in the ad.
- base_image (UploadFile): The base image file for ad generation.
- logo (UploadFile): The logo image file for the advertisement.

Responses from both endpoints will be an image in image/png format which can be displayed or downloaded.

## Usage
After starting the service, you can use curl or any HTTP client to interact with the API:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/generate-image/' \
  -H 'accept: image/png' \
  -H 'Content-Type: multipart/form-data' \
  -F 'prompt=Your prompt here' \
  -F 'base_image=@path_to_your_base_image.png;type=image/png'
```
Adjust the command with the actual values and paths you're using.

## License

[MIT](https://choosealicense.com/licenses/mit/)
