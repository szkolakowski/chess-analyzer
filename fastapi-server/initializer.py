from fastapi import FastAPI, File, Form, UploadFile
from tensorflow.keras.preprocessing import image
from PIL import Image as i
from tensorflow import keras
import os, image_slicer, time, shutil
import numpy as np
from stockfish import Stockfish

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
        figures = ['B', '0', 'K', 'N', 'P', 'Q', 'R']
        test = image.load_img(direc + '/' + tile, target_size=(120,120))
        test = image.img_to_array(test)
        test = np.expand_dims(test, axis=0)
        model = keras.models.load_model('figures_recognition.h5')
        result = model.predict(test)
        result = list(result[0])
        result = result.index(max(result))
        fen += str(figures[result])
    return fen

async def clean(conf):
    if conf:
        os.remove('boards/' + str(len(os.listdir('boards'))-2) + '.png')
        shutil.rmtree('boards/' + str(len(os.listdir('boards'))-1))
    return conf

@app.post('/chessboard')
async def handle_form(file: UploadFile = File(...)):
    image = await openImage(file)
    tiles = await saveTiles(64)
    fen = await predict('boards/' + str(len(os.listdir('boards'))-2))
    fen_save = fen
    fen_r = [fen[i:i+8] for i in range(0, len(fen), 8)]
    fen = []
    for fen_part in fen_r:
        f = ''
        conn = 0
        for chars in fen_part:
            if chars == '0':
                conn += 1
            else:
                if conn > 0:
                    f += str(conn)
                conn = 0
                f += chars
        if conn > 0:
            f += str(conn)
        fen.append(f)

    fen = '/'.join(fen)

    mess = await clean(True)

    return {'fen': fen, 'fec': '8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8','fen-raw': fen_save}