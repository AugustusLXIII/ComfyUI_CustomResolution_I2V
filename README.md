ComfyUI Custom Resolution I2V
A specialized resolution utility node for WanVideo Image-to-Video (I2V) workflows. This node provides standard resolution presets while offering a manual override system with automatic rounding.

✨ Features
WanVideo Presets: 20 pre-defined resolution levels (k18 to k55) optimized for WanVideo, covering Portrait, Landscape, and Square aspect ratios.

Smart Manual Override: Easily switch from presets to custom dimensions.

Automatic Rounding: Optional rounding modes (Multiple of 8 or 16) to ensure your custom resolutions are compatible with video encoders.

In-Node Tooltips: Hover over any field within ComfyUI to see detailed instructions and logic explanations.

🛠 Installation
Option 1: Via ComfyUI Manager (Recommended)
Search for Custom Resolution I2V in the ComfyUI Manager.

Click Install.

Option 2: Manual Installation (Git)
Open a terminal in your ComfyUI/custom_nodes/ folder.

Run the following command:

git clone https://github.com/YourGitHubUsername/ComfyUI_CustomResolution_I2V.git

Restart ComfyUI.

🚀 How to Use
Aspect Ratio: Choose between Portrait, Landscape, or Square.

Resolution Level: Select a preset tier. The node will automatically calculate the correct dimensions.

Manual Override: * Set the toggle to Enabled.

Input your desired manual_width and manual_height.

Note: If either dimension is set to 0, the node will ignore the override and default back to the selected Preset Level.

Rounding Mode: Choose a rounding preference for your manual dimensions to prevent "division by zero" or "invalid shape" errors during video encoding.

📦 Node Outputs
width/height: The calculated dimensions (integer).

length: Total frame count (calculated based on your duration input @ 16fps).

framerate: Fixed at 16fps as per WanVideo standards.

📄 License
This project is licensed under the MIT License.