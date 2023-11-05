from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
import torch

app = FastAPI()

hugging_face_token = "" # Specify your own token

device = "cuda" if torch.cuda.is_available() else "cpu"  # If there is a GPU, 'cuda' is used, otherwise 'cpu' is used.
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32,
    use_auth_token=hugging_face_token
)
pipe = pipe.to(device)

# Visual upload and reading function
def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

# Create Image
@app.post("/generate-image/")
async def generate_image(prompt: str = Form(...), base_image: UploadFile = File(...)):
    # Read first image
    content = await base_image.read()
    init_image = read_imagefile(content).convert("RGB")
    init_image = init_image.resize((768, 512))  # Resize to appropriate size

    # Create a new image with using model
    generated_images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images

    # Save image to memory and convert
    img_byte_arr = BytesIO()
    generated_images[0].save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

@app.post("/create-ad/")
async def create_ad(
    prompt: str = Form(...),
    color_hex: str = Form(...),
    punchline: str = Form(...),
    button_text: str = Form(...),
    base_image: UploadFile = File(...),
    logo: UploadFile = File(...)
):
    # Read and produce images
    base_image_data = await base_image.read()
    init_image = read_imagefile(base_image_data).convert("RGB")
    init_image = init_image.resize((768, 512))  # Resize to appropriate size

    # Create a new image with using model
    generated_images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images
    base_image = generated_images[0]

    # Read Logo image
    logo_image = read_imagefile(await logo.read())

    # Create ad image
    ad_image = create_ad_image(base_image, logo_image, punchline, button_text, color_hex)

    # Save image to memory and convert
    img_byte_arr = BytesIO()
    ad_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0) 

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

def create_ad_image(base_image: Image.Image, logo_image: Image.Image, punchline: str, button_text: str, color_hex: str) -> Image.Image:
    # Create a new image for background
    bg_width, bg_height = 768, 1024  # Adjust background dimensions based on image
    background = Image.new("RGB", (bg_width, bg_height), "white")

    # Adjust logo size and position
    logo_size = 200, 100  # Adjust logo size as desired
    logo_image.thumbnail(logo_size, Image.ANTIALIAS)
    logo_position = (bg_width - logo_image.width) // 2, 30  # Place logo top and center
    background.paste(logo_image, logo_position, logo_image.convert("RGBA"))

    # Place the product image in the center of the screen
    product_image_size = 400, 400  # Adjust product image size
    product_image = base_image.resize(product_image_size)
    product_image_position = (bg_width - product_image.width) // 2, logo_position[1] + logo_image.height + 20
    background.paste(product_image, product_image_position)

    # Prepare font and drawing objects
    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("coolvetica.otf", 20)  # Font size for button
        font2 = ImageFont.truetype("coolvetica.otf", 40)  # Font size for Punchline
    except IOError:
        font = ImageFont.load_default()
        font2 = ImageFont.load_default()

    # Place Punchline text just below the product image
    punchline_text_size = draw.textsize(punchline, font=font2)
    punchline_position = (bg_width - punchline_text_size[0]) // 2, product_image_position[1] + product_image.height + 20
    draw.text(punchline_position, punchline, font=font2, fill=color_hex)

    # Adjust button sizes and position
    button_size = 300, 60
    button_position = (bg_width - button_size[0]) // 2, punchline_position[1] + punchline_text_size[1] + 20
    draw.rectangle([button_position[0], button_position[1], button_position[0] + button_size[0], button_position[1] + button_size[1]], fill=color_hex)

    # Center button text
    button_text_size = draw.textsize(button_text, font=font)
    button_text_position = (button_position[0] + (button_size[0] - button_text_size[0]) // 2,
                            button_position[1] + (button_size[1] - button_text_size[1]) // 2)
    draw.text(button_text_position, button_text, font=font, fill="white")

    return background

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
