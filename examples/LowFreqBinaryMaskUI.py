from ..layer import *
from ..IO.UI import *


def trans_func(input):
	LowPass_filter_size = ui.get_track_bar_value("LowPass_filter_size")
	BinaryThreshHold_thresh = ui.get_track_bar_value("BinaryThreshHold_thresh")
	s = Sequential()
	s.append([
		RGB2Gray(), LowPass(LowPass_filter_size), BinaryThreshHold(thresh=BinaryThreshHold_thresh),
		LinearMap2Mask()
	])

	mask = s(input)
	o = MaskBlack()
	return o(input, mask)


ui = ParamsAdjustUI()


ui.create_trackbar()
ui.add_track_bar("LowPass_filter_size", 0, 20)
ui.add_track_bar("BinaryThreshHold_thresh", 0, 255)

ui.get_transform_function(trans_func)
