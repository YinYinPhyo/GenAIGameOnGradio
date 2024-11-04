import gradio as gr
import logging
from src.api.captioner import captioner
from src.api.generator import generate

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def caption_and_generate(image):
    try:
        if image is None:
            return "No image uploaded", None
        
        caption = captioner(image)
        logger.debug(f"Generated caption: {caption}")
        generated_image = generate(caption)
        return caption, generated_image
    except Exception as e:
        logger.error(f"Error in caption_and_generate: {str(e)}", exc_info=True)
        return f"Error: {str(e)}", None

with gr.Blocks() as demo:
    gr.Markdown("# Describe-and-Generate Game")
    image_upload = gr.Image(label="Upload an image", type="pil")
    btn_all = gr.Button("Caption and Generate")
    caption = gr.Textbox(label="Generated Caption")
    image_output = gr.Image(label="Generated Image")

    btn_all.click(fn=caption_and_generate, 
                  inputs=[image_upload], 
                  outputs=[caption, image_output])

if __name__ == "__main__":
    demo.launch(share=True)
