# Txt-Visual-Seperator

A program that separates text and visual elements from image.<br>
The program uses Google Cloud Vision API for OCR and YOLOv8 for image segmentation.

## Working

- The program takes a command line argument, which is the path to the image.
- It then makes an html file with the output in the output directory.
- It also creates a runs directory which stores all the past segmentation results.

_Note:_ There are two sample output files namely `person.html` and `winter.html` in the output directory. To view the demos correctly please run the demos using `make person` and `make winter`

## How to run

- Make a python virtual environment (`python3 -m venv venv`)
- Install poetry (`pip3 install poetry`)
- Install all the dependencies using poetry (`poetry install --no-root`)
- Create a new google cloud project and download json_credentials
- Enable Cloud_Vision_API and Billing in the Google Project
- Copy the .env.example to .env and edit it accordingly
- Run the application by running `python3 main.py <path_to_image>` in the src directory
- You can also run the demos by running `make person` or `make winter` in the project root directory
