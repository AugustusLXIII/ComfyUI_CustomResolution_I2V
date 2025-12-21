import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "WanVideo.ManualOverride",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "CustomResolutionI2V") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                
                const overrideWidget = this.widgets.find(w => w.name === "manual_override");
                const widthWidget = this.widgets.find(w => w.name === "manual_width");
                const heightWidget = this.widgets.find(w => w.name === "manual_height");

                const updateWidgets = () => {
                    const disabled = !overrideWidget.value;
                    widthWidget.disabled = disabled;
                    heightWidget.disabled = disabled;
                    // Adjust opacity to "grey out"
                    widthWidget.inputEl.style.opacity = disabled ? "0.5" : "1.0";
                    heightWidget.inputEl.style.opacity = disabled ? "0.5" : "1.0";
                };

                overrideWidget.callback = updateWidgets;
                // Run once on init
                setTimeout(updateWidgets, 10);
            };
        }
    }
});