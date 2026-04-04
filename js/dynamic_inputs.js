import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "FeiMao-326.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {

        // --- 1. General API Node (Dynamic Image Inputs) ---
        if (nodeData.name === "FeiMao_326_GeneralAPINode") {
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, slot) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }

                if (type !== 1) return;

                const imageInputRegex = /^image_(\d+)$/;
                const imageInputs = this.inputs.filter(inp => imageInputRegex.test(inp.name));

                let maxConnectedIndex = 0;
                for (const inp of imageInputs) {
                    if (inp.link !== null) {
                        const idx = parseInt(inp.name.match(imageInputRegex)[1]);
                        if (idx > maxConnectedIndex) maxConnectedIndex = idx;
                    }
                }

                const targetCount = Math.max(3, maxConnectedIndex + 1);
                const existingIndices = imageInputs.map(inp => parseInt(inp.name.match(imageInputRegex)[1])).sort((a, b) => a - b);
                const maxExistingIndex = existingIndices.length > 0 ? existingIndices[existingIndices.length - 1] : 0;

                if (maxExistingIndex < targetCount) {
                    for (let i = maxExistingIndex + 1; i <= targetCount; i++) {
                        const newName = `image_${i}`;
                        if (!this.inputs.find(inp => inp.name === newName)) {
                            this.addInput(newName, "IMAGE");
                        }
                    }
                    this.onResize?.(this.size);
<<<<<<< HEAD
=======
                    app.canvas.setDirty?.(true);
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
                }

                if (maxExistingIndex > targetCount) {
                    for (let i = maxExistingIndex; i > targetCount; i--) {
                        const nameToRemove = `image_${i}`;
                        const inputIndex = this.inputs.findIndex(inp => inp.name === nameToRemove);
                        if (inputIndex !== -1) {
                            this.removeInput(inputIndex);
                        }
                    }
                    this.onResize?.(this.size);
<<<<<<< HEAD
=======
                    app.canvas.setDirty?.(true);
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
                }
            };
        }

        // --- 2. JSON Parser (Dynamic Outputs) ---
        if (nodeData.name === "FeiMao_326_JsonParser") {
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, slot) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }

                if (type !== 2) return;

                const outputRegex = /^output_(\d+)$/;
                const outputs = this.outputs.filter(out => outputRegex.test(out.name));

                let maxConnectedIndex = 0;
                for (const out of outputs) {
                    if (out.links && out.links.length > 0) {
                        const idx = parseInt(out.name.match(outputRegex)[1]);
                        if (idx > maxConnectedIndex) maxConnectedIndex = idx;
                    }
                }

                const targetCount = Math.max(2, maxConnectedIndex + 1);
                const MAX_ALLOWED = 50;
                const finalTargetCount = Math.min(targetCount, MAX_ALLOWED);

                const existingIndices = outputs.map(out => parseInt(out.name.match(outputRegex)[1])).sort((a, b) => a - b);
                const maxExistingIndex = existingIndices.length > 0 ? existingIndices[existingIndices.length - 1] : 0;

                if (maxExistingIndex < finalTargetCount) {
                    for (let i = maxExistingIndex + 1; i <= finalTargetCount; i++) {
                        const newName = `output_${i}`;
                        if (!this.outputs.find(out => out.name === newName)) {
                            this.addOutput(newName, "STRING");
                        }
                    }
                    this.onResize?.(this.size);
<<<<<<< HEAD
=======
                    app.canvas.setDirty?.(true);
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
                }

                if (maxExistingIndex > finalTargetCount) {
                    for (let i = maxExistingIndex; i > finalTargetCount; i--) {
                        const nameToRemove = `output_${i}`;
                        const outputIndex = this.outputs.findIndex(out => out.name === nameToRemove);
                        if (outputIndex !== -1) {
                            this.removeOutput(outputIndex);
                        }
                    }
                    this.onResize?.(this.size);
                }
            };
        }
<<<<<<< HEAD
=======

        // --- 3. Text Template (Variable-based Dynamic Inputs) ---
        if (nodeData.name === "FeiMao_326_TextTemplate") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                const templateWidget = this.widgets.find(w => w.name === "template");
                
                const updateInputs = () => {
                    const text = templateWidget.value || "";
                    // Match all {var_name} (Support Unicode/Chinese)
                    const matches = text.match(/\{([^{}\s]+)\}/g) || [];
                    const vars = [...new Set(matches.map(m => m.slice(1, -1)))];
                    
                    // Add new inputs
                    vars.forEach(v => {
                        if (!this.inputs || !this.inputs.find(i => i.name === v)) {
                            this.addInput(v, "*"); // Universal type
                        }
                    });
                    
                    // Remove outdated inputs
                    if (this.inputs) {
                        for (let i = this.inputs.length - 1; i >= 0; i--) {
                            const inputName = this.inputs[i].name;
                            if (!vars.includes(inputName)) {
                                this.removeInput(i);
                            }
                        }
                    }
                    
                    this.onResize?.(this.size);
                    app.canvas.setDirty?.(true);
                };

                // Watch for widget changes
                templateWidget.callback = updateInputs;
                
                // Initial sync
                setTimeout(updateInputs, 100); 
                return r;
            };
        }
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
    },
});
