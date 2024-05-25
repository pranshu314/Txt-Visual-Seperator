import os
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


def get_images():
    """Retruns all the segmented images"""
    images = []
    dir_obj = os.scandir(os.curdir + "/runs/segment/predict/crops")
    for entry in dir_obj:
        if entry.is_dir():
            entry_obj = os.scandir(entry.path)
            for entry1 in entry_obj:
                images.append([entry.name, entry1.name, entry1.path])
                # print(entry.name, entry1.name, entry1.path)
    return images


def get_html(path):
    """Returns the html document with text and segmented image"""

    output_name = input("Enter the name of the output file without extension: ")
    images = get_images()

    with open(os.curdir + f"/output/{output_name}.html", "w") as html:
        html.write("<!DOCTYPE html>")
        html.write("<html lang='en'>")
        html.write("<head>")
        html.write("<meta charset='utf-8'>")
        html.write(f"<title>{output_name}</title>")
        html.write(
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        )
        html.write("<meta name='description' content='Output of Txt-Visual-Seperator'>")
        html.write("<link rel='stylesheet' href='index.css'>")
        html.write("</head>")
        html.write("<body>")

        # Content of the webpage
        html.write("<h1>Txt-Visual-Seperation</h1>")
        html.write("<h2>Original Image</h2>")
        html.write(f"<img src={path} alt='Original Image' width='650'>")
        html.write("<h2>Text in the Image</h2>")
        # TODO: Write the obtained text from OCR
        html.write("<p>TODO<p>")
        html.write("<h2>Segmented Image Parts</h2>")
        for entry in images:
            html.write("<figure>")
            html.write(
                f"<img src='../{entry[2]}' alt='{entry[0]+" "+entry[1]}' width='500'>"
            )
            html.write(f"<figcaption>Object Recognized: {entry[0]}</figcaption>")
            html.write("</figure>")
        # Content end

        html.write("</body>")
        html.write("</html>")
        html.close()


def segment_image(path):
    """Segments images using YOLOv8"""
    from ultralytics import YOLO

    model = YOLO("yolov8n-seg.pt")

    img = cv2.imread(path)

    out_img = model(img, save_crop=True)
    # out_img = model(img, show=True)


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

    if os.path.isfile(image_path) is False:
        print(f"    {terminal_red}Error:{terminal_reset} Could not load image")
        print(
            f"    {terminal_yellow}Warning:{terminal_reset} {image_path} is not a file."
        )
        return

    # detect_text(image_path)
    # segment_image(image_path)
    get_html(image_path)


if __name__ == "__main__":
    main()
