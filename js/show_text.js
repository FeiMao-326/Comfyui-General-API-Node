import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "FeiMao-326.ShowText",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
<<<<<<< HEAD
        if (nodeData.name === "ShowTextNode") {
=======
        // --- GLOBAL VISUAL UNIFICATION (AESTHETICS) ---
        // Force all sockets in this node pack to be circles (0 = LITEGRAPH.CIRCLE_SHAPE)
        if (nodeData.name && nodeData.name.startsWith("FeiMao_326_")) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                if (this.inputs) {
                    this.inputs.forEach(input => { input.shape = 0; });
                }
                if (this.outputs) {
                    this.outputs.forEach(output => { output.shape = 0; });
                }
                return r;
            };
        }

        // --- 1. ShowTextNode Specific Logic ---
        if (nodeData.name === "FeiMao_326_ShowTextNode") {
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

<<<<<<< HEAD
                if (this.widgets) {
                    const pos = this.widgets.findIndex((w) => w.name === "text");
                    if (pos !== -1) {
                        for (let i = pos; i < this.widgets.length; i++) {
                            this.widgets[i].onRemove?.();
                        }
                        this.widgets.length = pos;
                    }
                }

=======
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
                let text = message.text;
                if (Array.isArray(text)) {
                    text = text.join("\n");
                }
<<<<<<< HEAD
                const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
                w.inputEl.readOnly = true;
                w.inputEl.style.opacity = 0.6;
                w.value = text;

                this.onResize?.(this.size);
=======

                // --- NODES 2.0 ROBUST RENDERING ---
                // Rename widget to avoid conflict with 'text' input slot
                let w = this.widgets?.find((w) => w.name === "display_text");
                
                if (!w) {
                    // Create if not exists
                    w = ComfyWidgets["STRING"](this, "display_text", ["STRING", { multiline: true }], app).widget;
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.8; 
                    w.inputEl.style.pointerEvents = "auto"; // FORCE interactions for scroll
                    
                    // Prevent these values from being saved into the workflow JSON
                    w.serializeValue = () => undefined;

                    w.inputEl.addEventListener("wheel", (e) => {
                        // Just stop propagation to prevent canvas zoom
                        // Let the browser handle internal scroll when focused
                        e.stopPropagation();
                    }, { passive: false });
                    
                    w.inputEl.addEventListener("mousedown", (e) => {
                        e.stopPropagation();
                    });
                    
                    w.inputEl.addEventListener("keydown", (e) => {
                        e.stopPropagation();
                    });
                }

                w.value = text;
                if (w.inputEl) {
                    w.inputEl.value = text;
                }

                this.onResize?.(this.size);
                app.canvas.setDirty?.(true); 
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
            };
        }
    },
});
