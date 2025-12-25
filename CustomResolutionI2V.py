class CustomResolutionI2V:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # 1. Manual resolution database
        # Structure for each key: (2:3 Portrait, 9:16 Portrait, Square)
        # Note: Landscape is handled by swapping Portrait dimensions in the logic.
        s.db = {
            "k18": ((288, 432), (264, 472), (352, 352)),
            "k20": ((320, 480), (296, 528), (384, 384)),
            "k22": ((352, 528), (328, 584), (432, 432)),
            "k24": ((384, 576), (352, 624), (464, 464)),
            "k26": ((416, 624), (384, 680), (512, 512)),
            "k28": ((448, 672), (408, 728), (544, 544)),
            "k30": ((480, 720), (440, 784), (592, 592)),
            "k32": ((512, 768), (472, 840), (624, 624)),
            "k34": ((544, 816), (504, 896), (672, 672)),
            "k36": ((576, 864), (528, 944), (704, 704)),
            "k38": ((608, 912), (560, 992), (752, 752)),
            "k40": ((640, 960), (592, 1048), (784, 784)),
            "k42": ((672, 1008), (616, 1104), (816, 816)),
            "k44": ((704, 1056), (648, 1152), (864, 864)),
            "k46": ((736, 1104), (672, 1200), (896, 896)),
            "k48": ((768, 1152), (704, 1256), (944, 944)),
            "k50": ((800, 1200), (728, 1304), (960, 960)),
            "k52": ((832, 1248), (760, 1352), (992, 992)),
            "k54": ((864, 1296), (792, 1408), (1024, 1024)),
            "k55": ((880, 1320), (808, 1440), (1040, 1040)),
        }

        # Format resolution levels for the dropdown: "k30: 480x720 / 440x784 / 592x592"
        resolution_keys = []
        for k in sorted(s.db.keys()):
            v = s.db[k]
            resolution_keys.append(f"{k}: {v[0][0]}x{v[0][1]} / {v[1][0]}x{v[1][1]} / {v[2][0]}x{v[2][1]}")

        return {
            "required": {
                "aspect_ratio": (["Portrait (2:3)", "Portrait (9:16)", "Landscape (3:2)", "Landscape (16:9)", "Square"], {
                    "default": "Portrait (2:3)",
                    "tooltip": "Set the orientation. For Landscape options, the Portrait dimensions are swapped. Shown in order: 2:3, 9:16, Square."
                }),
                "resolution_level": (resolution_keys, {
                    "default": resolution_keys[6], # Default to k30
                    "tooltip": "Predefined resolution tiers. Displays 2:3, 9:16, and Square dimensions respectively."
                }),
                "manual_override": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "Enabled", 
                    "label_off": "Disabled",
                    "tooltip": "Use manual_width and manual_height instead of the preset levels."
                }),
                "manual_width": ("INT", {
                    "default": 0, "min": 0, "max": 8192, "step": 8,
                }),
                "manual_height": ("INT", {
                    "default": 0, "min": 0, "max": 8192, "step": 8,
                }),
                "framerate": (["16", "24", "30"], {
                    "default": "16",
                    "tooltip": "Target frames per second."
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

    def calculate_params(self, aspect_ratio, resolution_level, manual_override, manual_width, manual_height, framerate, video_duration):
        fps = float(framerate)
        
        if manual_override and manual_width > 0 and manual_height > 0:
            # Automatic multiple of 8 rounding
            width = (manual_width + 4) // 8 * 8
            height = (manual_height + 4) // 8 * 8
        else:
            key_id = resolution_level.split(":")[0]
            dims_2_3, dims_9_16, dims_square = self.db[key_id]
            
            if aspect_ratio == "Portrait (2:3)":
                width, height = dims_2_3
            elif aspect_ratio == "Portrait (9:16)":
                width, height = dims_9_16
            elif aspect_ratio == "Landscape (3:2)":
                width, height = dims_2_3[1], dims_2_3[0]
            elif aspect_ratio == "Landscape (16:9)":
                width, height = dims_9_16[1], dims_9_16[0]
            else: # Square
                width, height = dims_square

        total_frames = int(video_duration * fps) + 1
        return (width, height, total_frames, fps)

NODE_CLASS_MAPPINGS = {"CustomResolutionI2V": CustomResolutionI2V}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomResolutionI2V": "CustomResolution_I2V_v1.1"}