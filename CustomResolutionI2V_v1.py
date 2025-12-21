class CustomResolutionI2V:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        s.resolution_keys = [
            "k18: 288x432 / 352x352", "k20: 320x480 / 384x384", "k22: 352x528 / 432x432",
            "k24: 384x576 / 464x464", "k26: 416x624 / 512x512", "k28: 448x672 / 544x544",
            "k30: 480x720 / 592x592", "k32: 512x768 / 624x624", "k34: 544x816 / 672x672",
            "k36: 576x864 / 704x704", "k38: 608x912 / 752x752", "k40: 640x960 / 784x784",
            "k42: 672x1008 / 816x816", "k44: 704x1056 / 864x864", "k46: 736x1104 / 896x896",
            "k48: 768x1152 / 944x944", "k50: 800x1200 / 960x960", "k52: 832x1248 / 992x992",
            "k54: 864x1296 / 1024x1024", "k55: 880x1320 / 1040x1040"
        ]
        
        return {
            "required": {
                "aspect_ratio": (["Portrait", "Landscape", "Square"], {
                    "default": "Portrait",
                    "tooltip": "Set the orientation. In Landscape, the Portrait dimensions are swapped."
                }),
                "resolution_level": (s.resolution_keys, {
                    "default": "k48: 768x1152 / 944x944",
                    "tooltip": "Predefined resolution tiers from the WanVideo specification."
                }),
                "manual_override": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "Enabled", 
                    "label_off": "Disabled",
                    "tooltip": "When enabled, the node uses manual_width and manual_height instead of the preset levels."
                }),
                "manual_width": ("INT", {
                    "default": 0, "min": 0, "max": 8192, "step": 1,
                    "tooltip": "Custom width. IMPORTANT: This is ignored if Manual Override is OFF or if this value is 0."
                }),
                "manual_height": ("INT", {
                    "default": 0, "min": 0, "max": 8192, "step": 1,
                    "tooltip": "Custom height. IMPORTANT: This is ignored if Manual Override is OFF or if this value is 0."
                }),
                "rounding_mode": (["None", "Multiple of 8", "Multiple of 16"], {
                    "default": "Multiple of 8",
                    "tooltip": "Round the manual dimensions to ensure compatibility with video encoders."
                }),
                "video_duration": ("FLOAT", {
                    "default": 5.0, "min": 1.0, "max": 10.0, "step": 0.5, "display": "number",
                    "tooltip": "Total length of the video in seconds."
                }),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "FLOAT")
    RETURN_NAMES = ("width", "height", "length", "framerate")
    FUNCTION = "calculate_params"
    CATEGORY = "WanVideo"

    def calculate_params(self, aspect_ratio, resolution_level, manual_override, manual_width, manual_height, rounding_mode, video_duration):
        # 1. Check for Manual Override logic
        # Must be toggled ON and both values must be greater than 0
        if manual_override and manual_width > 0 and manual_height > 0:
            w, h = manual_width, manual_height
            
            if rounding_mode == "Multiple of 8":
                w = max(8, (w + 4) // 8 * 8)
                h = max(8, (h + 4) // 8 * 8)
            elif rounding_mode == "Multiple of 16":
                w = max(16, (w + 8) // 16 * 16)
                h = max(16, (h + 8) // 16 * 16)
            
            width, height = w, h
            print(f"WanVideo: Manual Override ({rounding_mode}) -> {width}x{height}")
            
        else:
            # 2. Internal Database of Resolutions
            db = {
                "k18": ((288, 432), (352, 352)), "k20": ((320, 480), (384, 384)),
                "k22": ((352, 528), (432, 432)), "k24": ((384, 576), (464, 464)),
                "k26": ((416, 624), (512, 512)), "k28": ((448, 672), (544, 544)),
                "k30": ((480, 720), (592, 592)), "k32": ((512, 768), (624, 624)),
                "k34": ((544, 816), (672, 672)), "k36": ((576, 864), (704, 704)),
                "k38": ((608, 912), (752, 752)), "k40": ((640, 960), (784, 784)),
                "k42": ((672, 1008), (816, 816)), "k44": ((704, 1056), (864, 864)),
                "k46": ((736, 1104), (896, 896)), "k48": ((768, 1152), (944, 944)),
                "k50": ((800, 1200), (960, 960)), "k52": ((832, 1248), (992, 992)),
                "k54": ((864, 1296), (1024, 1024)), "k55": ((880, 1320), (1040, 1040)),
            }

            key_id = resolution_level.split(":")[0]
            (portrait_dims, square_dims) = db[key_id]
            
            if aspect_ratio == "Square":
                width, height = square_dims
            elif aspect_ratio == "Portrait":
                width, height = portrait_dims
            else: # Landscape
                width, height = portrait_dims[1], portrait_dims[0]
            
            print(f"WanVideo: Selected {key_id} | {aspect_ratio} -> {width}x{height}")

        # 3. Calculate Video Specs
        framerate = 16
        total_frames = int(video_duration * framerate) + 1

        return (width, height, total_frames, framerate)

NODE_CLASS_MAPPINGS = {"CustomResolutionI2V": CustomResolutionI2V}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomResolutionI2V": "CustomResolution_I2V_v1.0"}