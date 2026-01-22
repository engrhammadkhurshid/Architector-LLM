import * as vscode from 'vscode';
import { generateArchitectureDocs, startBackendServer, stopBackendServer } from './commands';

let backendProcess: any = null;
let statusBarItem: vscode.StatusBarItem;

export async function activate(context: vscode.ExtensionContext) {
    console.log('Architector-LLM extension is now active');

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'architector-llm.showMenu';
    updateStatusBar('ready');
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register commands
    const generateDocsCommand = vscode.commands.registerCommand(
        'architector-llm.generateDocs',
        async () => {
            updateStatusBar('generating');
            try {
                await generateArchitectureDocs(context);
                updateStatusBar('ready');
            } catch (error) {
                updateStatusBar('error');
                setTimeout(() => updateStatusBar('ready'), 5000);
            }
        }
    );

    const startBackendCommand = vscode.commands.registerCommand(
        'architector-llm.startBackend',
        async () => {
            updateStatusBar('starting');
            backendProcess = await startBackendServer(context);
            updateStatusBar('ready');
        }
    );

    const stopBackendCommand = vscode.commands.registerCommand(
        'architector-llm.stopBackend',
        async () => {
            await stopBackendServer(backendProcess);
            backendProcess = null;
            updateStatusBar('ready');
        }
    );

    // Show quick menu
    const showMenuCommand = vscode.commands.registerCommand(
        'architector-llm.showMenu',
        async () => {
            const items = [
                { label: '$(file-text) Generate Documentation', command: 'architector-llm.generateDocs' },
                { label: '$(play) Start Backend Server', command: 'architector-llm.startBackend' },
                { label: '$(debug-stop) Stop Backend Server', command: 'architector-llm.stopBackend' },
            ];

            const selected = await vscode.window.showQuickPick(items, {
                placeHolder: 'Select an Architector-LLM action',
            });

            if (selected) {
                await vscode.commands.executeCommand(selected.command);
            }
        }
    );

    context.subscriptions.push(generateDocsCommand, startBackendCommand, stopBackendCommand, showMenuCommand);

    // Auto-start backend if configured
    const config = vscode.workspace.getConfiguration('architector');
    if (config.get('autoStartBackend')) {
        updateStatusBar('starting');
        backendProcess = await startBackendServer(context);
        updateStatusBar('ready');
    }

    vscode.window.showInformationMessage('Architector-LLM is ready!');
}

function updateStatusBar(state: 'ready' | 'generating' | 'starting' | 'error') {
    switch (state) {
        case 'ready':
            statusBarItem.text = '$(circuit-board) Architector';
            statusBarItem.tooltip = 'Architector-LLM: Ready';
            statusBarItem.backgroundColor = undefined;
            break;
        case 'generating':
            statusBarItem.text = '$(sync~spin) Architector';
            statusBarItem.tooltip = 'Architector-LLM: Generating documentation...';
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            break;
        case 'starting':
            statusBarItem.text = '$(sync~spin) Architector';
            statusBarItem.tooltip = 'Architector-LLM: Starting backend...';
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            break;
        case 'error':
            statusBarItem.text = '$(error) Architector';
            statusBarItem.tooltip = 'Architector-LLM: Error occurred';
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
            break;
    }
}

export function deactivate() {
    if (backendProcess) {
        backendProcess.kill();
    }
}
