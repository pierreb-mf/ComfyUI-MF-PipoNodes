import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";
import { api } from "../../../scripts/api.js";

// Load Chart.js from CDN for Graph Plotter
const loadChartJS = () => {
    return new Promise((resolve, reject) => {
        if (window.Chart) {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load Chart.js'));
        document.head.appendChild(script);
    });
};

app.registerExtension({
    name: "MF.PipoNodes",
    
    async setup() {
        // Load Chart.js on startup for Graph Plotter
        try {
            await loadChartJS();
            console.log("📊 Chart.js loaded for MF Graph Plotter");
        } catch (error) {
            console.error("Failed to load Chart.js:", error);
        }
    },
    
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
        
        // ====================================================================
        // GRAPH PLOTTER
        // ====================================================================
        if (nodeData.name === "MF_GraphPlotter") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                
                // Store reference to this node's ID (use ComfyUI's node ID)
                this.graphNodeId = this.id;
                console.log(`📊 Graph Plotter node created with ID: ${this.graphNodeId}`);
                
                // Add reset button
                this.addWidget(
                    "button",
                    "🔄 Reset Graph",
                    null,
                    () => {
                        this.resetGraph();
                    },
                    { serialize: false }
                );
                
                // Add save graph button
                this.addWidget(
                    "button",
                    "💾 Save Graph",
                    null,
                    () => {
                        this.saveGraphWithDialog();
                    },
                    { serialize: false }
                );
                
                // Create canvas for the graph
                const canvas = document.createElement('canvas');
                canvas.width = 400;
                canvas.height = 300;
                canvas.style.width = '100%';
                canvas.style.height = 'auto';
                
                // Add canvas widget (no label)
                const canvasWidget = this.addDOMWidget("graph_canvas", "canvas", canvas, {
                    serialize: false,
                    hideOnZoom: false,
                });
                canvasWidget.computeSize = function() {
                    return [400, 300];
                };
                
                // Remove the label element if it exists
                if (canvasWidget.label) {
                    canvasWidget.label = "";
                }
                
                // Store canvas reference
                this.graphCanvas = canvas;
                this.canvasWidget = canvasWidget;
                
                // Initialize Chart.js chart
                this.initChart();
                
                return r;
            };
            
            // Initialize Chart.js instance
            nodeType.prototype.initChart = function () {
                if (!window.Chart || !this.graphCanvas) {
                    console.warn("⚠️ Chart.js or canvas not available");
                    return;
                }
                
                // Destroy existing chart if it exists
                if (this.chart) {
                    try {
                        this.chart.destroy();
                        this.chart = null;
                    } catch (e) {
                        console.warn("Warning destroying old chart:", e);
                    }
                }
                
                const ctx = this.graphCanvas.getContext('2d');
                
                // Plugin to draw custom Y axis label (upright, not rotated)
                const customYAxisLabel = {
                    id: 'customYAxisLabel',
                    afterDraw: (chart) => {
                        const ctx = chart.ctx;
                        const yScale = chart.scales.y;
                        
                        if (yScale) {
                            ctx.save();
                            ctx.font = 'bold 14px sans-serif';
                            ctx.fillStyle = '#ffffff';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'bottom';
                            
                            // Draw Y label at the top-left of the chart (upright)
                            const x = yScale.left - 20;
                            const y = yScale.top - 10;
                            ctx.fillText('Y', x, y);
                            
                            ctx.restore();
                        }
                    }
                };
                
                try {
                    this.chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: [],
                            datasets: [{
                                label: 'Y Values',
                                data: [],
                                borderColor: '#FFEC00',
                                backgroundColor: 'rgba(255, 236, 0, 0.15)',
                                borderWidth: 2,
                                fill: true,
                                pointRadius: 5,
                                pointBackgroundColor: '#FFEC00',
                                pointBorderColor: '#ffffff',
                                pointBorderWidth: 2,
                                pointHoverRadius: 7,
                                tension: 0.4  // Smooth curves
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            animation: {
                                duration: 300
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    enabled: true,
                                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                    titleColor: '#ffffff',
                                    bodyColor: '#ffffff',
                                    borderColor: '#ffffff',
                                    borderWidth: 1,
                                    callbacks: {
                                        title: function() {
                                            return '';
                                        },
                                        label: function(context) {
                                            const xValue = context.parsed.x;
                                            const yValue = context.parsed.y;
                                            return [
                                                'X = ' + xValue,
                                                'Y = ' + yValue
                                            ];
                                        }
                                    },
                                    displayColors: false
                                }
                            },
                            scales: {
                                x: {
                                    title: {
                                        display: false  // X label removed
                                    },
                                    ticks: { 
                                        display: false
                                    },
                                    grid: { 
                                        color: 'rgba(255, 255, 255, 0.1)',
                                        drawTicks: true
                                    },
                                    border: {
                                        display: true,
                                        color: '#000000',
                                        width: 2
                                    }
                                },
                                y: {
                                    title: {
                                        display: false
                                    },
                                    ticks: { 
                                        display: false
                                    },
                                    grid: { 
                                        color: function(context) {
                                            // Make the zero line more visible
                                            if (context.tick.value === 0) {
                                                return 'rgba(255, 255, 255, 0.5)';
                                            }
                                            return 'rgba(255, 255, 255, 0.1)';
                                        },
                                        drawTicks: true
                                    },
                                    border: {
                                        display: true,
                                        color: '#000000',
                                        width: 2
                                    }
                                }
                            }
                        },
                        plugins: [customYAxisLabel]
                    });
                } catch (error) {
                    console.error("Error creating chart:", error);
                    this.chart = null;
                }
            };
            
            // Update chart with new data
            nodeType.prototype.updateChart = function (xValues, yValues) {
                if (!this.chart) {
                    console.warn("⚠️ Chart not initialized");
                    return;
                }
                
                try {
                    // Update chart data
                    this.chart.data.labels = xValues;
                    this.chart.data.datasets[0].data = yValues;
                    this.chart.update();
                } catch (error) {
                    console.error("Error updating chart:", error);
                }
            };
            
            // Save graph with file dialog
            nodeType.prototype.saveGraphWithDialog = async function () {
                if (!this.chart || !this.graphCanvas) {
                    console.warn("⚠️ No graph data to save");
                    return;
                }
                
                try {
                    // Create a temporary link element
                    const link = document.createElement('a');
                    
                    // Convert canvas to blob
                    this.graphCanvas.toBlob(async (blob) => {
                        // For browsers that support showSaveFilePicker (Chrome, Edge)
                        if (window.showSaveFilePicker) {
                            try {
                                const handle = await window.showSaveFilePicker({
                                    suggestedName: `graph_${this.graphNodeId || 'plot'}.jpg`,
                                    types: [{
                                        description: 'JPEG Image',
                                        accept: {'image/jpeg': ['.jpg', '.jpeg']},
                                    }],
                                });
                                
                                const writable = await handle.createWritable();
                                
                                // Convert to JPEG
                                const canvas = document.createElement('canvas');
                                canvas.width = this.graphCanvas.width;
                                canvas.height = this.graphCanvas.height;
                                const ctx = canvas.getContext('2d');
                                
                                // Fill with white background
                                ctx.fillStyle = '#FFFFFF';
                                ctx.fillRect(0, 0, canvas.width, canvas.height);
                                ctx.drawImage(this.graphCanvas, 0, 0);
                                
                                canvas.toBlob(async (jpegBlob) => {
                                    await writable.write(jpegBlob);
                                    await writable.close();
                                    console.log('📊 Graph saved successfully');
                                }, 'image/jpeg', 0.95);
                                
                            } catch (err) {
                                // User cancelled the save dialog
                                if (err.name !== 'AbortError') {
                                    console.error('Error saving file:', err);
                                }
                            }
                        } else {
                            // Fallback for browsers that don't support showSaveFilePicker
                            const canvas = document.createElement('canvas');
                            canvas.width = this.graphCanvas.width;
                            canvas.height = this.graphCanvas.height;
                            const ctx = canvas.getContext('2d');
                            
                            // Fill with white background
                            ctx.fillStyle = '#FFFFFF';
                            ctx.fillRect(0, 0, canvas.width, canvas.height);
                            ctx.drawImage(this.graphCanvas, 0, 0);
                            
                            canvas.toBlob((jpegBlob) => {
                                const url = URL.createObjectURL(jpegBlob);
                                link.href = url;
                                link.download = `graph_${this.graphNodeId || 'plot'}.jpg`;
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                                URL.revokeObjectURL(url);
                                console.log('📊 Graph downloaded (browser does not support save dialog)');
                            }, 'image/jpeg', 0.95);
                        }
                    });
                    
                } catch (error) {
                    console.error('Error saving graph:', error);
                }
            };
            
            // Reset graph data
            nodeType.prototype.resetGraph = async function () {
                try {
                    const response = await api.fetchApi("/graph_plotter/reset", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            node_id: String(this.graphNodeId || this.id)
                        })
                    });
                    
                    if (response.ok) {
                        // Clear the chart immediately and force update
                        if (this.chart) {
                            this.chart.data.labels = [];
                            this.chart.data.datasets[0].data = [];
                            this.chart.update('none');  // Update without animation
                        }
                        
                        console.log(`🔄 MF Graph Plotter: Data reset for node ${this.graphNodeId}`);
                    } else {
                        console.error("Failed to reset graph:", await response.text());
                    }
                } catch (error) {
                    console.error("Error resetting graph:", error);
                }
            };
            
            // Handle execution results
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                // Don't process if node is being removed
                if (this && this._isBeingRemoved) {
                    console.log("⚠️ Skipping onExecuted - node being removed");
                    return;
                }
                
                onExecuted?.apply(this, arguments);
                
                if (message.graph_data && message.graph_data[0]) {
                    const data = message.graph_data[0];
                    
                    // Store the node ID from the backend
                    if (data.node_id) {
                        this.graphNodeId = data.node_id;
                    }
                    
                    // Don't update if we have no data points (fresh after reset)
                    if (data.point_count === 0) {
                        return;
                    }
                    
                    // Update chart - but check if still valid
                    if (this && this.chart && !this._isBeingRemoved) {
                        this.updateChart(data.x_values, data.y_values);
                        console.log(`📊 Graph updated: ${data.point_count} points`);
                    }
                }
            };
            
            // Cleanup on node removal - CRITICAL: Must prevent all chart access
            const onRemoved = nodeType.prototype.onRemoved;
            nodeType.prototype.onRemoved = function () {
                console.log("🗑️ [MF_GraphPlotter] Removing node...");
                
                // Check if 'this' exists before doing anything
                if (!this) {
                    console.warn("⚠️ [MF_GraphPlotter] 'this' is undefined in onRemoved");
                    if (onRemoved && typeof onRemoved === 'function') {
                        try {
                            return onRemoved.call(null, ...arguments);
                        } catch (e) {
                            console.error("Error in original onRemoved:", e);
                        }
                    }
                    return;
                }
                
                // Set flag to prevent any operations during removal
                try {
                    this._isBeingRemoved = true;
                } catch (e) {
                    console.warn("⚠️ Could not set removal flag:", e);
                }
                
                // Destroy chart instance with extreme safety
                try {
                    if (this.chart) {
                        try {
                            // Detach all event listeners
                            if (this.chart.canvas) {
                                this.chart.canvas.onclick = null;
                                this.chart.canvas.onmousemove = null;
                            }
                            
                            // Destroy the chart
                            this.chart.destroy();
                            console.log("✅ [MF_GraphPlotter] Chart destroyed");
                        } catch (error) {
                            console.error("❌ Error destroying chart:", error);
                        }
                        this.chart = null;
                    }
                } catch (e) {
                    console.error("❌ Chart cleanup error:", e);
                }
                
                // Clean up canvas element
                try {
                    if (this.graphCanvas) {
                        try {
                            const canvas = this.graphCanvas;
                            // Remove all event listeners
                            canvas.onclick = null;
                            canvas.onmousemove = null;
                            
                            // Remove from DOM
                            if (canvas.parentNode) {
                                canvas.parentNode.removeChild(canvas);
                            }
                            console.log("✅ [MF_GraphPlotter] Canvas cleaned");
                        } catch (error) {
                            console.warn("⚠️ Warning cleaning canvas:", error);
                        }
                        this.graphCanvas = null;
                    }
                } catch (e) {
                    console.error("❌ Canvas cleanup error:", e);
                }
                
                // Clean up widget reference
                try {
                    if (this.canvasWidget) {
                        this.canvasWidget = null;
                    }
                } catch (e) {
                    // Ignore
                }
                
                // Clean up node ID
                try {
                    if (this.graphNodeId) {
                        this.graphNodeId = null;
                    }
                } catch (e) {
                    // Ignore
                }
                
                console.log("✅ [MF_GraphPlotter] Cleanup complete");
                
                // Call original onRemoved with proper context
                if (onRemoved && typeof onRemoved === 'function') {
                    try {
                        return onRemoved.apply(this, arguments);
                    } catch (error) {
                        console.error("❌ Error in original onRemoved:", error);
                    }
                }
            };
            
            // Override methods to check if node is being removed
            const originalUpdateChart = nodeType.prototype.updateChart;
            nodeType.prototype.updateChart = function(xValues, yValues) {
                if (this && this._isBeingRemoved) {
                    console.log("⚠️ Skipping updateChart - node being removed");
                    return;
                }
                if (originalUpdateChart) {
                    return originalUpdateChart.call(this, xValues, yValues);
                }
            };
            
            const originalInitChart = nodeType.prototype.initChart;
            nodeType.prototype.initChart = function() {
                if (this && this._isBeingRemoved) {
                    console.log("⚠️ Skipping initChart - node being removed");
                    return;
                }
                if (originalInitChart) {
                    return originalInitChart.call(this);
                }
            };
        }
        
        // ====================================================================
        // STORY DRIVER
        // ====================================================================
        if (nodeData.name === "MF_StoryDriver") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                
                // Add reset button
                this.addWidget(
                    "button",
                    "🔄 Reset Story",
                    null,
                    () => {
                        this.resetStory();
                    },
                    { serialize: false }
                );
                
                // Add status display widget
                const widgetObj = ComfyWidgets["STRING"](
                    this, 
                    "status_display", 
                    ["STRING", { multiline: false }], 
                    app
                );
                
                const widget = widgetObj.widget;
                
                if (widget && widget.inputEl) {
                    widget.inputEl.readOnly = true;
                    widget.inputEl.style.opacity = 0.7;
                    widget.inputEl.style.textAlign = "center";
                    widget.inputEl.style.fontFamily = "monospace";
                }
                widget.value = "Step: 0 | Seed: 0";
                
                return r;
            };
            
            // Add reset method
            nodeType.prototype.resetStory = async function () {
                const projectNameWidget = this.widgets?.find(w => w.name === "projectName");
                const randomizeSeedWidget = this.widgets?.find(w => w.name === "randomize_seed_on_reset");
                
                const projectName = projectNameWidget ? projectNameWidget.value : "MyProject";
                const randomizeSeed = randomizeSeedWidget ? randomizeSeedWidget.value : true;
                
                try {
                    const response = await api.fetchApi("/story_driver/reset", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            project_name: projectName,
                            randomize_seed: randomizeSeed
                        })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        const statusWidget = this.widgets?.find(w => w.name === "status_display");
                        if (statusWidget) {
                            statusWidget.value = `Step: ${data.step} | Seed: ${data.seed}`;
                        }
                        console.log(`🔄 MF Story Driver reset: ${projectName} - Step: ${data.step}, Seed: ${data.seed}`);
                    } else {
                        console.error("Error resetting story:", await response.text());
                    }
                } catch (error) {
                    console.error("Error resetting story:", error);
                }
            };
            
            // Handle execution results
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                const widget = this.widgets?.find((w) => w.name === "status_display");
                
                if (widget && message.status_display?.[0]) {
                    widget.value = message.status_display[0];
                }
            };
        }

        // ====================================================================
        // MF SHOW DATA
        // ====================================================================
        if (nodeData.name === "MFShowData") {
                    // Add a callback for when the node is executed
                    const onExecuted = nodeType.prototype.onExecuted;
                    nodeType.prototype.onExecuted = function (message) {
                        onExecuted?.apply(this, arguments);
                        
                        if (message.text) {
                            // Find or create the text widget
                            let textWidget = this.widgets?.find(w => w.name === "display_text");
                            
                            if (!textWidget) {
                                textWidget = ComfyWidgets["STRING"](this, "display_text", ["STRING", { multiline: true }], app).widget;
                                textWidget.inputEl.readOnly = true;
                                textWidget.inputEl.style.opacity = 0.7;
                                textWidget.inputEl.style.fontSize = "10pt";
                                textWidget.inputEl.style.fontFamily = "monospace";
                            }
                            
                            // Update the text content
                            const text = message.text[0];
                            textWidget.value = text;
                            
                            // Auto-resize based on content
                            const lines = text.split('\n').length;
                            textWidget.inputEl.rows = Math.min(Math.max(lines, 3), 20);
                            
                            this.setSize([
                                Math.max(this.size[0], 400),
                                this.computeSize()[1]
                            ]);
                        }
                    };
                }
        
    },
});
