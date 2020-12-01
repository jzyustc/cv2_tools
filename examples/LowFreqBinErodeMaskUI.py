from ..layer import *
from ..IO import *


def trans_func(input):
	LowPass_filter_size = ui.get_track_bar_value("LowPass_filter_size")
	BinaryThreshHold_thresh = ui.get_track_bar_value("BinaryThreshHold_thresh")
	ErodeMaskFuzzy_kernel_size = ui.get_track_bar_value("ErodeMaskFuzzy_thresh_size")
	ErodeMaskFuzzy_filter_size = ui.get_track_bar_value("ErodeMaskFuzzy_filter_size")
	s = Sequential()
	s.append([
		RGB2Gray(), LowPass(LowPass_filter_size), BinaryThreshHold(thresh=BinaryThreshHold_thresh),
		ErodeMaskFuzzy(kernel_size=ErodeMaskFuzzy_kernel_size, filter_size=ErodeMaskFuzzy_filter_size),
		LinearMap2Mask()
	])

	mask = s(input)
	o = MaskBlack()
	return o(input, mask)


ui = ParamsAdjustUI()

ui.read_raw_image("images/bubble.png")

ui.create_trackbar()
ui.add_track_bar("LowPass_filter_size", 0, 20)
ui.add_track_bar("BinaryThreshHold_thresh", 0, 255)
ui.add_track_bar("ErodeMaskFuzzy_thresh_size", 0, 255)
ui.add_track_bar("ErodeMaskFuzzy_filter_size", 0, 20)

ui.get_transform_function(trans_func)
