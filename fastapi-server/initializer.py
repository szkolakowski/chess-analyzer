from fastapi import FastAPI, File, Form, UploadFile
from PIL import Image as i
import os, image_slicer

app = FastAPI()

@app.post('/chessboard')
async def handle_form(file: UploadFile = File(...)):
    img = i.open(file.file)
    name = 'boards/' + str(len(os.listdir('boards'))) + '.png'
    img.save(name)

    fen = ''
    tiles = image_slicer.slice(name, 64, save=False)
    for tile in tiles:
        pass
    return {'message': 'works'}