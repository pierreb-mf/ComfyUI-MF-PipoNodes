import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "MF.PipoNodes",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        
        // ====================================================================
        // DICE ROLLER
        // ====================================================================
        if (nodeData.name === "MF_DiceRoller") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                
                const widget = ComfyWidgets["STRING"](
                    this, 
                    "result", 
                    ["STRING", { multiline: true }], 
                    app
                ).widget;
                
                widget.inputEl.readOnly = true;
                widget.inputEl.style.opacity = 0.6;
                widget.value = "🎲 Roll the dice!";
                
                return r;
            };
            
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                const widget = this.widgets?.find((w) => w.name === "result");
                
                if (widget && message.text?.[0]) {
                    widget.value = message.text[0];
                }
            };
        }
        
        // ====================================================================
        // LOG FILE
        // ====================================================================
        if (nodeData.name === "MF_LogFile") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                
                const widget = ComfyWidgets["STRING"](
                    this, 
                    "log_display", 
                    ["STRING", { multiline: true }], 
                    app
                ).widget;
                
                widget.inputEl.readOnly = true;
                widget.inputEl.style.opacity = 0.6;
                widget.inputEl.style.fontFamily = "monospace";
                widget.inputEl.style.fontSize = "12px";
                widget.value = "📝 Log file content will appear here...";
                
                widget.inputEl.style.height = "150px";
                widget.inputEl.style.maxHeight = "150px";
                
                return r;
            };
            
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                const widget = this.widgets?.find((w) => w.name === "log_display");
                
                if (widget && message.log_display?.[0]) {
                    widget.value = message.log_display[0];
                }
            };
        }
        
        // ====================================================================
        // MODULO
        // ====================================================================
        if (nodeData.name === "MF_Modulo") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                
                const widget = ComfyWidgets["STRING"](
                    this, 
                    "result", 
                    ["STRING", { multiline: true }], 
                    app
                ).widget;
                
                widget.inputEl.readOnly = true;
                widget.inputEl.style.opacity = 0.6;
                widget.value = "🔢 Calculate modulo";
                
                return r;
            };
            
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                const widget = this.widgets?.find((w) => w.name === "result");
                
                if (widget && message.text?.[0]) {
                    widget.value = message.text[0];
                }
            };
        }
        
        // ====================================================================
        // MODULO ADVANCED
        // ====================================================================
        if (nodeData.name === "MF_ModuloAdvanced") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                
                const widget = ComfyWidgets["STRING"](
                    this, 
                    "result", 
                    ["STRING", { multiline: true }], 
                    app
                ).widget;
                
                widget.inputEl.readOnly = true;
                widget.inputEl.style.opacity = 0.6;
                widget.value = "🔢 Calculate modulo\n🔄 Cycle: 0";
                
                widget.inputEl.style.height = "60px";
                widget.inputEl.style.maxHeight = "60px";
                
                return r;
            };
            
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                const widget = this.widgets?.find((w) => w.name === "result");
                
                if (widget && message.text?.[0]) {
                    widget.value = message.text[0];
                }
            };
        }
    },
});