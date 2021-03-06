from subprocess import call
import image_slicer
import shutil
import os

# slice board images
img = 0
imgs = len(os.listdir('archive/train'))
for images in os.listdir('archive/train'):
	tiles = image_slicer.slice('archive/train/' + images, 64, save=False)
	image_slicer.save_tiles(tiles, directory='possible-tiles/empty', prefix=images[:-5])
	img += 1
	load = int((img/imgs)*100) * '=' + '>' + (int((imgs/imgs)*100)-1-int((img/imgs)*100)) * '.'
	print('Sliced images: ' + str(img) + '/' + str(imgs) + ':')
	print(str(int((img/imgs)*100)) + '% ' + load)

# transfer images to folders
img = 0
imgs = len(os.listdir('possible-tiles/empty'))
for images in os.listdir('possible-tiles/empty'):
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
		upper_bool = tile.isupper()
		destination_foler = 'possible-tiles/'
		if tile == 'p' or tile =='P':
			destination_foler += 'pawn'
			shutil.move('possible-tiles/empty/' + images, destination_foler)
		elif tile == 'n' or tile =='N':
			destination_foler += 'knight'
			shutil.move('possible-tiles/empty/' + images, destination_foler)
		elif tile == 'b' or tile =='B':
			destination_foler += 'bishop'
			shutil.move('possible-tiles/empty/' + images, destination_foler)
		elif tile == 'r' or tile =='R':
			destination_foler += 'rook'
			shutil.move('possible-tiles/empty/' + images, destination_foler)
		elif tile == 'q' or tile =='Q':
			destination_foler += 'queen'
			shutil.move('possible-tiles/empty/' + images, destination_foler)
		elif tile == 'k' or tile =='K':
			destination_foler += 'king'
			shutil.move('possible-tiles/empty/' + images, destination_foler)
		print('current position: ' + str(img) + '/' + str(imgs))
		# empty tiles in empty

# remove extra items
for folders in os.listdir('possible-tiles'):
	imgs = 1
	for images in os.listdir('possible-tiles/' + folders):
		imgs += 1
		if imgs > 24000:
			os.remove('possible-tiles/' + folders + '/' + images)
			print('current position: ' + str(imgs) + '/24000 in ' + folders)