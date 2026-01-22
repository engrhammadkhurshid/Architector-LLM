"use strict";
/**
 * Progress Panel
 * Shows a webview panel with real-time progress updates
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProgressPanel = void 0;
const vscode = __importStar(require("vscode"));
class ProgressPanel {
    constructor(extensionUri) {
        this.extensionUri = extensionUri;
        this.messages = [];
        this.panel = vscode.window.createWebviewPanel('architectorProgress', 'Generating Documentation', vscode.ViewColumn.Beside, {
            enableScripts: true,
            retainContextWhenHidden: true
        });
        this.panel.webview.html = this.getWebviewContent();
    }
    show() {
        this.panel.reveal();
    }
    updateProgress(message) {
        this.messages.push(message);
        this.panel.webview.postMessage({
            command: 'updateProgress',
            message: message
        });
    }
    dispose() {
        this.panel.dispose();
    }
    getWebviewContent() {
        return `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Generating Documentation</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        min-height: 100vh;
                        margin: 0;
                    }
                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        text-align: center;
                    }
                    h1 {
                        font-size: 2em;
                        margin-bottom: 30px;
                        animation: fadeIn 0.5s ease-in;
                    }
                    .logo {
                        font-size: 4em;
                        margin-bottom: 20px;
                        animation: bounce 2s infinite;
                    }
                    .progress-area {
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 15px;
                        padding: 30px;
                        backdrop-filter: blur(10px);
                        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    }
                    .spinner {
                        width: 60px;
                        height: 60px;
                        margin: 20px auto;
                        border: 6px solid rgba(255, 255, 255, 0.3);
                        border-top-color: white;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    }
                    .message {
                        font-size: 1.2em;
                        margin: 15px 0;
                        animation: slideIn 0.3s ease-out;
                    }
                    .log {
                        text-align: left;
                        max-height: 300px;
                        overflow-y: auto;
                        margin-top: 20px;
                        padding: 15px;
                        background: rgba(0, 0, 0, 0.2);
                        border-radius: 8px;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9em;
                    }
                    .log-entry {
                        margin: 5px 0;
                        padding: 5px;
                        border-left: 3px solid rgba(255, 255, 255, 0.5);
                        padding-left: 10px;
                        animation: slideIn 0.3s ease-out;
                    }
                    @keyframes spin {
                        to { transform: rotate(360deg); }
                    }
                    @keyframes bounce {
                        0%, 100% { transform: translateY(0); }
                        50% { transform: translateY(-20px); }
                    }
                    @keyframes fadeIn {
                        from { opacity: 0; }
                        to { opacity: 1; }
                    }
                    @keyframes slideIn {
                        from {
                            opacity: 0;
                            transform: translateX(-20px);
                        }
                        to {
                            opacity: 1;
                            transform: translateX(0);
                        }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo">📚</div>
                    <h1>Architector-LLM</h1>
                    <div class="progress-area">
                        <div class="spinner"></div>
                        <div class="message" id="currentMessage">Initializing...</div>
                        <div class="log" id="log"></div>
                    </div>
                </div>
                
                <script>
                    const vscode = acquireVsCodeApi();
                    const logElement = document.getElementById('log');
                    const messageElement = document.getElementById('currentMessage');
                    
                    window.addEventListener('message', event => {
                        const message = event.data;
                        if (message.command === 'updateProgress') {
                            messageElement.textContent = message.message;
                            
                            const entry = document.createElement('div');
                            entry.className = 'log-entry';
                            entry.textContent = message.message;
                            logElement.appendChild(entry);
                            
                            // Auto-scroll to bottom
                            logElement.scrollTop = logElement.scrollHeight;
                        }
                    });
                </script>
            </body>
            </html>
        `;
    }
}
exports.ProgressPanel = ProgressPanel;
//# sourceMappingURL=progressPanel.js.map