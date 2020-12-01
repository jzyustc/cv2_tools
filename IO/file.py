'''
File read and save

By jzyustc, 2020/11/30

'''

from . import *


def read_image(path: str):
	if not os.path.exists(path):
		raise FileNotFoundError("Image path not exist")
	return cv2.imread(path)


def write_image(path: str, img: np.ndarray):
	cv2.imwrite(path, img)
