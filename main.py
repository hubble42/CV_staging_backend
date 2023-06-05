from fastapi import FastAPI, File, Form, UploadFile
from typing import Union, Dict, Any
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

# from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from helper_functions.image_helper import predict
from helper_functions.video_helper1 import check
import base64

# import json
from fastapi.responses import StreamingResponse
from moviepy.editor import *
import csv
import pandas as pd
import os.path


app = FastAPI()

# Configure CORS
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


objects = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


object_dict = {object: index for index, object in enumerate(objects)}

CSV_FILE_PATH = "C:/Users/DELL/object-detection/backend/users.csv"


class UserCredentials(BaseModel):
    email: str
    password: str


def check_existing_user(username: str, email: str) -> Union[bool, Dict[str, Any]]:
    # Check if the CSV file exists
    if not os.path.isfile(CSV_FILE_PATH):
        return False

    # Check if the CSV file is empty
    if os.path.getsize(CSV_FILE_PATH) == 0:
        return False

    # Load the CSV file using pandas
    df = pd.read_csv(
        CSV_FILE_PATH, header=None, names=["username", "email", "password"]
    )

    # Check if the username or email already exists
    existing_user = df[(df["username"] == username) | (df["email"] == email)]

    if len(existing_user) > 0:
        existing_user_data = existing_user.iloc[0].to_dict()
        return existing_user_data
    else:
        return False


def write_user_data(user_data: dict):
    # Check if the CSV file exists
    if not os.path.isfile(CSV_FILE_PATH):
        # Create the CSV file with header
        with open(CSV_FILE_PATH, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=["username", "email", "password"]
            )
            writer.writeheader()

    # Append the user data to the CSV file
    with open(CSV_FILE_PATH, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["username", "email", "password"])
        writer.writerow(user_data)


def validate_login(email: str, password: str) -> Union[bool, Dict[str, Any]]:
    # Check if the CSV file exists
    if not os.path.isfile(CSV_FILE_PATH):
        return False

    # Check if the CSV file is empty
    if os.path.getsize(CSV_FILE_PATH) == 0:
        return False

    # Load the CSV file using pandas
    df = pd.read_csv(
        CSV_FILE_PATH, header=None, names=["username", "email", "password"]
    )

    # Check if the username or email already exists
    existing_user = df[(df["email"] == email) | (df["password"] == password)]

    if len(existing_user) > 0:
        existing_user_data = existing_user.iloc[0].to_dict()
        return existing_user_data
    else:
        return False


@app.post("/login/")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")
    existing_user = validate_login(email, password)
    if existing_user:
        print(existing_user)
        return {"message": "login Successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@app.post("/signup")
def signup(user_data: dict):
    username = user_data.get("username")
    email = user_data.get("email")
    password = user_data.get("password")

    existing_user = check_existing_user(username, email)
    if existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    write_user_data(user_data)
    return {"message": "Signup Successful"}


@app.get("/pre-loaded-images/")
async def pre_loaded_classes():
    return {"objects": objects}


@app.post("/upload_image_file/")
async def create_upload_file(file: UploadFile = File(...)):
    print(file.filename)
    file_path = f"C:/Users/DELL/object-detection/backend/saved-files/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    with open(file_path, "rb") as file_object:
        encoded_string1 = base64.b64encode(file_object.read())

    # await the predict function to get its returned value
    image_path, class_names = await predict(file_path)

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return {"file": encoded_string, "file1": encoded_string1, "classes": class_names}


@app.post("/uploadvideo/")
async def upload_video(
    file: UploadFile = File(...), selected_options: list = Form(...)
):
    # Save the uploaded file to a specified location

    selected_options = selected_options[0].split(",")
    file_location = (
        f"C:/Users/DELL/object-detection/backend/saved-files/{file.filename}"
    )
    with open(file_location, "wb+") as f:
        f.write(file.file.read())

    class_list = []

    for option in selected_options:
        # try:
        # Try to look up the index for the option in the dictionary
        if option in object_dict:
            class_list.append(object_dict[option])

            # else:
            #     class_list.append(None)
        # except KeyError:
        #     # Handle cases where the option is not in the dictionary
        #     pass

    # Call the check function to get the video path
    video_path = check(file_location, file.filename, class_list)

    my_list = os.listdir("runs/detect")
    max_value = max(
        map(int, [s.replace("predict", "") for s in my_list if s != "predict"])
    )
    video_path_n = (
        f"runs/detect/predict" + str(max_value) + "/" + str(1) + str(file.filename)
    )

    # Load the input video file
    input_file = VideoFileClip(video_path)
    # Set the output video format and codec
    output_format = "mp4"
    codec = "libx264"
    # Convert the input video to the output format with the specified codec
    output_file = input_file.write_videofile(
        video_path_n,
        codec=codec,
        audio_codec="aac",
        threads=4,
        fps=input_file.fps,
        preset="medium",
        ffmpeg_params=["-crf", "23"],
    )
    # Close the input and output files
    input_file.close()

    # Return the file as a streaming response

    def file_streamer(file_location):
        with open(file_location, "rb") as video_file:
            while True:
                video_chunk = video_file.read(1024)
                if not video_chunk:
                    break
                yield video_chunk

    return StreamingResponse(file_streamer(video_path_n), media_type="video/mp4")
