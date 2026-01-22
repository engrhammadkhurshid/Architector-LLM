import * as vscode from 'vscode';
import * as path from 'path';
import * as child_process from 'child_process';
import axios from 'axios';
import { getBackendUrl } from './config';

// Output channel for detailed logs
let outputChannel: vscode.OutputChannel | null = null;

function getOutputChannel(): vscode.OutputChannel {
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel('Architector-LLM');
    }
    return outputChannel;
}

function log(message: string) {
    const channel = getOutputChannel();
    const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
    channel.appendLine(`[${timestamp}] ${message}`);
}

// Stage mapping for progress tracking
const STAGES = [
    { name: 'Parsing codebase', increment: 15 },
    { name: 'Building dependency graph', increment: 15 },
    { name: 'Curating prompts', increment: 10 },
    { name: 'Generating with LLM', increment: 40 },
    { name: 'Parsing response', increment: 10 },
    { name: 'Rendering diagrams', increment: 5 },
    { name: 'Organizing output', increment: 5 },
];

export async function generateArchitectureDocs(context: vscode.ExtensionContext): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    const codebasePath = workspaceFolder.uri.fsPath;

    // Show output panel
    const channel = getOutputChannel();
    channel.show(true);
    log('='.repeat(60));
    log('Starting architecture documentation generation');
    log(`Codebase: ${codebasePath}`);

    try {
        // Show progress
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'Architector-LLM',
                cancellable: true,
            },
            async (progress, token) => {
                const startTime = Date.now();
                progress.report({ increment: 0, message: 'Connecting to backend...' });
                log('Connecting to backend server...');

                // Call backend API
                const backendUrl = getBackendUrl();
                log(`Backend URL: ${backendUrl}`);
                
                // Start with stage tracking
                let currentStageIndex = 0;
                const updateProgress = () => {
                    if (currentStageIndex < STAGES.length) {
                        const stage = STAGES[currentStageIndex];
                        progress.report({ increment: stage.increment, message: stage.name });
                        log(`Stage ${currentStageIndex + 1}/${STAGES.length}: ${stage.name}`);
                        currentStageIndex++;
                    }
                };

                // Simulate stage progression (since backend doesn't provide streaming updates yet)
                const progressInterval = setInterval(() => {
                    if (!token.isCancellationRequested) {
                        updateProgress();
                    }
                }, 8000); // Update every 8 seconds

                try {
                    const response = await axios.post(
                        `${backendUrl}/generate`,
                        {
                            codebase_path: codebasePath,
                        },
                        {
                            timeout: 600000, // 10 minutes
                        }
                    );

                    clearInterval(progressInterval);

                    if (token.isCancellationRequested) {
                        log('Generation cancelled by user');
                        return;
                    }

                    // Complete all remaining stages
                    while (currentStageIndex < STAGES.length) {
                        updateProgress();
                    }

                    const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
                    log(`Generation completed in ${elapsedTime}s`);

                    const data = response.data;
                    const outputDir = data.output_dir || data.output_path;
                    
                    // Log metrics
                    if (data.metrics) {
                        log('Metrics:');
                        log(`  - Files analyzed: ${data.metrics.files_analyzed || 'N/A'}`);
                        log(`  - Classes found: ${data.metrics.classes_found || 'N/A'}`);
                        log(`  - Functions found: ${data.metrics.functions_found || 'N/A'}`);
                        log(`  - Processing time: ${data.metrics.processing_time_seconds || elapsedTime}s`);
                    }
                    log(`Output directory: ${outputDir}`);
                    
                    if (data.saved_files) {
                        log('Generated files:');
                        data.saved_files.forEach((file: string) => log(`  - ${file}`));
                    }
                    log('='.repeat(60));

                    const message = `Documentation generated in ${elapsedTime}s`; 
                    
                    const action = await vscode.window.showInformationMessage(
                        message,
                        'Open Documentation',
                        'View Diagram',
                        'Show in Explorer'
                    );

                    if (action === 'Open Documentation') {
                        const docUri = vscode.Uri.file(path.join(outputDir, 'README.md'));
                        await vscode.commands.executeCommand('markdown.showPreview', docUri);
                    } else if (action === 'View Diagram') {
                        // Try to open PNG first, then SVG, then Mermaid source
                        const pngPath = path.join(outputDir, 'diagrams', 'architecture.png');
                        const svgPath = path.join(outputDir, 'diagrams', 'architecture.svg');
                        const mmdPath = path.join(outputDir, 'diagrams', 'architecture.mmd');
                        
                        try {
                            const fs = require('fs');
                            if (fs.existsSync(pngPath)) {
                                const pngUri = vscode.Uri.file(pngPath);
                                await vscode.commands.executeCommand('vscode.open', pngUri);
                            } else if (fs.existsSync(svgPath)) {
                                const svgUri = vscode.Uri.file(svgPath);
                                await vscode.commands.executeCommand('vscode.open', svgUri);
                            } else if (fs.existsSync(mmdPath)) {
                                const mmdUri = vscode.Uri.file(mmdPath);
                                await vscode.commands.executeCommand('markdown.showPreview', mmdUri);
                            }
                        } catch (err) {
                            log(`Error opening diagram: ${err}`);
                        }
                    } else if (action === 'Show in Explorer') {
                        const folderUri = vscode.Uri.file(outputDir);
                        await vscode.commands.executeCommand('revealFileInOS', folderUri);
                    }
                } catch (error: any) {
                    clearInterval(progressInterval);
                    throw error;
                }
            }
        );
    } catch (error: any) {
        log(`ERROR: ${error.message}`);
        if (error.response) {
            log(`Response status: ${error.response.status}`);
            log(`Response data: ${JSON.stringify(error.response.data)}`);
        }
        log('='.repeat(60));
        console.error('Error generating documentation:', error);
        vscode.window.showErrorMessage(
            `Failed to generate documentation: ${error.message}`
        );
    }
}

export async function startBackendServer(context: vscode.ExtensionContext): Promise<any> {
    const extensionPath = context.extensionPath;
    const backendPath = path.join(extensionPath, 'backend', 'src', 'main.py');
    
    try {
        // Check if backend is already running
        const backendUrl = getBackendUrl();
        log('Checking if backend is already running...');
        try {
            await axios.get(`${backendUrl}/health`, { timeout: 2000 });
            log('Backend server is already running');
            vscode.window.showInformationMessage('Backend server is already running');
            return null;
        } catch (e) {
            // Backend not running, start it
            log('Backend not running, starting new instance...');
        }

        vscode.window.showInformationMessage('Starting backend server...');
        log(`Starting backend: ${backendPath}`);

        const pythonProcess = child_process.spawn('python3', [backendPath], {
            cwd: path.join(extensionPath, 'backend'),
            env: { ...process.env },
        });

        pythonProcess.stdout.on('data', (data) => {
            const message = data.toString().trim();
            log(`[Backend] ${message}`);
            console.log(`Backend: ${data}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            const message = data.toString().trim();
            log(`[Backend Error] ${message}`);
            console.error(`Backend Error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            log(`Backend process exited with code ${code}`);
            console.log(`Backend process exited with code ${code}`);
        });

        // Wait for server to be ready
        log('Waiting for backend to initialize...');
        await new Promise((resolve) => setTimeout(resolve, 3000));

        // Verify backend is responding
        try {
            await axios.get(`${backendUrl}/health`, { timeout: 2000 });
            log('Backend server started successfully');
            vscode.window.showInformationMessage('Backend server started successfully');
        } catch (e) {
            log('WARNING: Backend may not be fully ready yet');
        }

        return pythonProcess;
    } catch (error: any) {
        log(`Failed to start backend: ${error.message}`);
        vscode.window.showErrorMessage(`Failed to start backend: ${error.message}`);
        throw error;
    }
}

export async function stopBackendServer(process: any): Promise<void> {
    if (process) {
        log('Stopping backend server...');
        process.kill();
        log('Backend server stopped');
        vscode.window.showInformationMessage('Backend server stopped');
    } else {
        log('No backend process to stop');
    }
}
