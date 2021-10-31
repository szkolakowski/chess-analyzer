from subprocess import call
import image_slicer
import shutil
import os

#img = 0
#imgs = len(os.listdir('archive/train'))
#for images in os.listdir('archive/train'):
#	tiles = image_slicer.slice('archive/train/' + images, 64, save=False)
#	image_slicer.save_tiles(tiles, directory='possible-tiles/x-tiles', prefix=images[:-5])
#	img += 1
#	load = int((img/imgs)*100) * '=' + '>' + (int((imgs/imgs)*100)-1-int((img/imgs)*100)) * '.'
#	print('Sliced images: ' + str(img) + '/' + str(imgs) + ':')
#	print(str(int((img/imgs)*100)) + '% ' + load)

img = 0
imgs = len(os.listdir('possible-tiles/x-tiles'))
for images in os.listdir('possible-tiles/x-tiles'):
	if True:
		img += 1
		image_name = images.split('.')[0]
		tile_row_column = [image_name.split('_')[1], image_name.split('_')[2]]
		fen = image_name.split('_')[0]
		fen_row = fen.split('-')[int(tile_row_column[0])-1]
		row = ''
		for chars in fen_row:
			if chars in ['p', 'P', 'n', 'N', 'b', 'B', 'r', 'R', 'q', 'Q', 'k' , 'K']:
				row += chars
			else:
				row += int(chars) * '0'
		tile = row[int(tile_row_column[1])-1]
		destination_foler = 'possible-tiles/'
		if tile == 'p' or tile =='P':
			destination_foler += 'pawn'
			shutil.move('possible-tiles/x-tiles/' + images, destination_foler)
		elif tile == 'n' or tile =='N':
			destination_foler += 'knight'
			shutil.move('possible-tiles/x-tiles/' + images, destination_foler)
		elif tile == 'b' or tile =='B':
			destination_foler += 'bishop'
			shutil.move('possible-tiles/x-tiles/' + images, destination_foler)
		elif tile == 'r' or tile =='R':
			destination_foler += 'rook'
			shutil.move('possible-tiles/x-tiles/' + images, destination_foler)
		elif tile == 'q' or tile =='Q':
			destination_foler += 'queen'
			shutil.move('possible-tiles/x-tiles/' + images, destination_foler)
		elif tile == 'k' or tile =='K':
			destination_foler += 'king'
			shutil.move('possible-tiles/x-tiles/' + images, destination_foler)
		print('current position: ' + str(img) + '/' + str(imgs))