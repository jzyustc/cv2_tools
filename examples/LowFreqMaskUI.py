from ..layer import *
from ..IO import *


def trans_func(input):
	LowPass_filter_size = ui.get_track_bar_value("LowPass_filter_size")
	s = Sequential()
	s.append([
		RGB2Gray(), LowPass(LowPass_filter_size), LinearMap2Mask()
	])

	mask = s(input)
	o = MaskBlack()
	return o(input, mask)


ui = ParamsAdjustUI()

ui.read_raw_image("images/bubble.png")

ui.create_trackbar()
ui.add_track_bar("LowPass_filter_size", 0, 20)

ui.get_transform_function(trans_func)
