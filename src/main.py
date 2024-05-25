import sys

from dotenv import load_dotenv
import cv2

load_dotenv()

terminal_red = "\033[1;31m"
terminal_yellow = "\033[1;33m"
terminal_reset = "\033[0m"


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


def segment_image(path):
    from ultralytics import YOLO

    model = YOLO("yolov8n-seg.pt")

    img = cv2.imread(path)
    out_img = model(img, save_crop=True)


def main():
    """Runs the OCR and Image-Segmentation tasks."""
    if len(sys.argv) != 2:
        print(
            f"\t{terminal_red}Error:{terminal_reset} "
            "The program takes exactly 1 command line argument which is"
            " the path to the image."
        )
        return -1

    image_path = sys.argv[1]
    # detect_text(image_path)
    segment_image(image_path)


if __name__ == "__main__":
    main()
