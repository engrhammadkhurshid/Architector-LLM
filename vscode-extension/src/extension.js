"use strict";
/**
 * Architector-LLM VS Code Extension
 * Main entry point for the extension
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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const dependencyChecker_1 = require("./dependencyChecker");
const pythonRunner_1 = require("./pythonRunner");
const progressPanel_1 = require("./progressPanel");
let statusBarItem;
let outputChannel;
function activate(context) {
    console.log('Architector-LLM extension is now active');
    // Create output channel
    outputChannel = vscode.window.createOutputChannel('Architector-LLM');
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = "$(book) Architector";
    statusBarItem.tooltip = "Generate Architecture Documentation";
    statusBarItem.command = 'architector-llm.generateDocs';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
    // Register commands
    const generateDocsCommand = vscode.commands.registerCommand('architector-llm.generateDocs', async () => await generateDocumentation(context));
    const checkDependenciesCommand = vscode.commands.registerCommand('architector-llm.checkDependencies', async () => await checkDependencies());
    context.subscriptions.push(generateDocsCommand, checkDependenciesCommand, outputChannel);
    // Check dependencies on activation
    checkDependencies();
}
async function generateDocumentation(context) {
    outputChannel.show();
    outputChannel.appendLine('Starting documentation generation...');
    // Get workspace folder
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }
    const projectPath = workspaceFolder.uri.fsPath;
    outputChannel.appendLine(`Project path: ${projectPath}`);
    // Check dependencies first
    const checker = new dependencyChecker_1.DependencyChecker(outputChannel);
    const depsOk = await checker.checkAll();
    if (!depsOk) {
        const install = await vscode.window.showErrorMessage('Some dependencies are missing. Would you like to see the installation guide?', 'Yes', 'No');
        if (install === 'Yes') {
            await vscode.commands.executeCommand('architector-llm.checkDependencies');
        }
        return;
    }
    // Ask for semantic version
    const version = await vscode.window.showInputBox({
        prompt: 'Enter semantic version for documentation (e.g., 1.0.0)',
        value: '1.0.0',
        validateInput: (value) => {
            if (!/^\d+\.\d+\.\d+$/.test(value)) {
                return 'Please enter a valid semantic version (e.g., 1.0.0)';
            }
            return null;
        }
    });
    if (!version) {
        return; // User cancelled
    }
    // Show progress panel
    const progressPanel = new progressPanel_1.ProgressPanel(context.extensionUri);
    progressPanel.show();
    try {
        statusBarItem.text = "$(sync~spin) Generating...";
        // Run Python pipeline
        const runner = new pythonRunner_1.PythonRunner(outputChannel);
        const extensionPath = context.extensionPath;
        const backendPath = path.join(path.dirname(extensionPath), 'backend', 'src');
        const result = await runner.runPipeline(projectPath, version, backendPath, (message) => {
            progressPanel.updateProgress(message);
        });
        statusBarItem.text = "$(book) Architector";
        if (result.success) {
            outputChannel.appendLine('\n✅ Documentation generated successfully!');
            outputChannel.appendLine(`Output: ${result.outputPath}`);
            progressPanel.updateProgress('✅ Complete! Opening documentation...');
            // Show success message with options
            const action = await vscode.window.showInformationMessage(`Documentation generated successfully!\n${result.diagrams} diagrams created with ${result.quality}/100 quality score.`, 'Open Documentation', 'Show in Finder', 'Close');
            if (action === 'Open Documentation') {
                const readmePath = path.join(result.outputPath, 'README.md');
                const doc = await vscode.workspace.openTextDocument(readmePath);
                await vscode.window.showTextDocument(doc);
            }
            else if (action === 'Show in Finder') {
                vscode.commands.executeCommand('revealFileInOS', vscode.Uri.file(result.outputPath));
            }
            progressPanel.dispose();
        }
        else {
            outputChannel.appendLine(`\n❌ Error: ${result.error}`);
            vscode.window.showErrorMessage(`Documentation generation failed: ${result.error}`);
            progressPanel.updateProgress(`❌ Failed: ${result.error}`);
            setTimeout(() => progressPanel.dispose(), 3000);
        }
    }
    catch (error) {
        statusBarItem.text = "$(book) Architector";
        outputChannel.appendLine(`\n❌ Error: ${error}`);
        vscode.window.showErrorMessage(`Documentation generation failed: ${error}`);
        progressPanel.dispose();
    }
}
async function checkDependencies() {
    const checker = new dependencyChecker_1.DependencyChecker(outputChannel);
    const panel = vscode.window.createWebviewPanel('dependencyCheck', 'Architector Dependencies', vscode.ViewColumn.One, {});
    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 { color: #007acc; }
                .dependency {
                    margin: 15px 0;
                    padding: 10px;
                    border-left: 3px solid #ddd;
                    background: #f5f5f5;
                }
                .dependency.installed {
                    border-left-color: #4caf50;
                }
                .dependency.missing {
                    border-left-color: #f44336;
                }
                .status {
                    font-weight: bold;
                    margin-right: 10px;
                }
                .installed .status { color: #4caf50; }
                .missing .status { color: #f44336; }
                code {
                    background: #e0e0e0;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-size: 0.9em;
                }
                pre {
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }
            </style>
        </head>
        <body>
            <h1>🔧 Dependency Check</h1>
            <p>Checking for required dependencies...</p>
            <div id="status">Loading...</div>
        </body>
        </html>
    `;
    // Check dependencies
    const results = await checker.checkAllDetailed();
    let html = '<h2>Status</h2>';
    for (const [name, result] of Object.entries(results)) {
        const statusClass = result.installed ? 'installed' : 'missing';
        const statusText = result.installed ? '✅ Installed' : '❌ Missing';
        html += `
            <div class="dependency ${statusClass}">
                <span class="status">${statusText}</span>
                <strong>${name}</strong>
                ${result.version ? `<br><small>Version: ${result.version}</small>` : ''}
                ${result.message ? `<br><small>${result.message}</small>` : ''}
                ${!result.installed && result.installCmd ? `
                    <br><br>
                    <strong>Installation:</strong>
                    <pre>${result.installCmd}</pre>
                ` : ''}
            </div>
        `;
    }
    panel.webview.html = panel.webview.html.replace('<div id="status">Loading...</div>', html);
}
function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
    if (outputChannel) {
        outputChannel.dispose();
    }
}
//# sourceMappingURL=extension.js.map