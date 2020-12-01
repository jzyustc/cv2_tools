from ..layer import *
from ..IO import *


def trans_func(input):
	BoxContourMask_thresh = ui.get_track_bar_value("BoxContourMask_thresh")
	BoxContourMask_min_area = ui.get_track_bar_value("BoxContourMask_min_area")
	s = Sequential()
	s.append([
		RGB2Gray(), BoxContourMask(thresh=BoxContourMask_thresh, min_area=BoxContourMask_min_area), LinearMap2Mask()
	])

	mask = s(input)
	o = MaskBlack()
	return o(input, mask)


ui = ParamsAdjustUI()

ui.read_raw_image("images/bubble.png")

ui.create_trackbar()
ui.add_track_bar("BoxContourMask_thresh", 0, 255)
ui.add_track_bar("BoxContourMask_min_area", 100, 400)

ui.get_transform_function(trans_func)

