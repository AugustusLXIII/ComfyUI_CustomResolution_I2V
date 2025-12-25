import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "WanVideo.CustomResolutionLogic",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "CustomResolutionI2V") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                
                const overrideWidget = this.widgets.find(w => w.name === "manual_override");
                const widthWidget = this.widgets.find(w => w.name === "manual_width");
                const heightWidget = this.widgets.find(w => w.name === "manual_height");

                const updateManualVisibility = () => {
                    const manualEnabled = !!overrideWidget?.value;
                    
                    if (widthWidget) widthWidget.disabled = !manualEnabled;
                    if (heightWidget) heightWidget.disabled = !manualEnabled;
                    
                    // Visual feedback: reduce opacity for disabled widgets if inputEl exists
                    if (widthWidget?.inputEl?.style) {
                        widthWidget.inputEl.style.opacity = manualEnabled ? "1.0" : "0.5";
                    }
                    if (heightWidget?.inputEl?.style) {
                        heightWidget.inputEl.style.opacity = manualEnabled ? "1.0" : "0.5";
                    }
                };

                if (overrideWidget) {
                    overrideWidget.callback = updateManualVisibility;
                }

                // Delay slightly to ensure widgets and their elements are fully initialized
                setTimeout(() => {
                    updateManualVisibility();
                }, 100);
            };
        }
    }
});