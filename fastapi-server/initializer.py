from fastapi import FastAPI, File, Form, UploadFile
from tensorflow.keras.preprocessing import image
from PIL import Image as i
from tensorflow import keras
import os, image_slicer, time
import numpy as np

app = FastAPI()

async def openImage(file):
    image = i.open(file.file)
    direc = 'boards/' + str(len(os.listdir('boards')))
    name = 'boards/' + str(len(os.listdir('boards'))) + '.png'
    os.mkdir(direc)
    img = image.save(name)
    return image

async def saveTiles(tiles):
    tiles = image_slicer.slice('boards/' + str(len(os.listdir('boards'))-2) + '.png', 64, save=False)
    image_slicer.save_tiles(tiles, directory='boards/' + str(len(os.listdir('boards'))-2), prefix='sliced')
    return tiles

async def predict(direc):
    fen = ''
    tiles = sorted(os.listdir(direc))
    for tile in tiles:
        figures = ['b', 'B', '0', 'k', 'K', 'n', 'N', 'p', 'P', 'q', 'Q', 'r', 'R']
        print(direc + '/' + tile)
        test = image.load_img(direc + '/' + tile, target_size=(120,120))
        test = image.img_to_array(test)
        test = np.expand_dims(test, axis=0)
        model = keras.models.load_model('figures_recognition.h5')
        result = model.predict(test)
        result = list(result[0])
        result = result.index(max(result))
        fen += str(figures[result])
    return fen

@app.post('/chessboard')
async def handle_form(file: UploadFile = File(...)):
    image = await openImage(file)
    tiles = await saveTiles(64)
    fen = await predict('boards/' + str(len(os.listdir('boards'))-2))
    fen = '-'.join([fen[i:i+8] for i in range(0, len(fen), 8)])
    return {'message': fen}