/**
 * Architector-LLM VS Code Extension
 * Main entry point for the extension
 */

import * as vscode from 'vscode';
import * as path from 'path';
import { DependencyChecker } from './dependencyChecker';
import { PythonRunner } from './pythonRunner';
import { ProgressPanel } from './progressPanel';
import { SetupWizard } from './setupWizard';
import { ApiKeyManager } from './apiKeyManager';
import { DeveloperInfoManager } from './analytics/developerInfo';
import { AnalyticsManager } from './analytics/telemetry';

let statusBarItem: vscode.StatusBarItem;
let outputChannel: vscode.OutputChannel;
let dependenciesChecked: boolean = false; // Cache dependency check for session

export function activate(context: vscode.ExtensionContext) {
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
    const generateDocsCommand = vscode.commands.registerCommand(
        'architector-llm.generateDocs',
        async () => await generateDocumentation(context)
    );
    
    const checkDependenciesCommand = vscode.commands.registerCommand(
        'architector-llm.checkDependencies',
        async () => await checkDependencies()
    );
    
    const showAboutCommand = vscode.commands.registerCommand(
        'architector-llm.showAbout',
        async () => await showAbout(context)
    );
    
    const showPrivacyPolicyCommand = vscode.commands.registerCommand(
        'architector-llm.showPrivacyPolicy',
        async () => await showPrivacyPolicy(context)
    );
    
    const revokeConsentCommand = vscode.commands.registerCommand(
        'architector-llm.revokeConsent',
        async () => {
            const devInfoManager = new DeveloperInfoManager(context);
            await devInfoManager.revokeConsent();
        }
    );
    
    const updateDeveloperInfoCommand = vscode.commands.registerCommand(
        'architector-llm.updateDeveloperInfo',
        async () => {
            const devInfoManager = new DeveloperInfoManager(context);
            await devInfoManager.updateDeveloperInfo();
        }
    );
    
    const exportAnalyticsCommand = vscode.commands.registerCommand(
        'architector-llm.exportAnalytics',
        async () => {
            try {
                const analytics = new AnalyticsManager(context);
                const exportPath = await analytics.exportAnalytics();
                const open = await vscode.window.showInformationMessage(
                    `Analytics exported to: ${exportPath}`,
                    'Open File'
                );
                if (open === 'Open File') {
                    vscode.commands.executeCommand('vscode.open', vscode.Uri.file(exportPath));
                }
            } catch (error: any) {
                vscode.window.showErrorMessage(`Failed to export analytics: ${error.message}`);
            }
        }
    );
    
    const runSetupWizardCommand = vscode.commands.registerCommand(
        'architector-llm.runSetupWizard',
        async () => {
            // Reset setup state to allow re-running
            await context.globalState.update('setupCompleted', false);
            const setupWizard = new SetupWizard(context);
            await setupWizard.run();
        }
    );
    
    context.subscriptions.push(
        generateDocsCommand,
        checkDependenciesCommand,
        showAboutCommand,
        showPrivacyPolicyCommand,
        revokeConsentCommand,
        updateDeveloperInfoCommand,
        exportAnalyticsCommand,
        runSetupWizardCommand,
        outputChannel
    );
    
    // First-run detection: Show welcome only on FIRST activation
    // Run asynchronously to not block extension activation
    (async () => {
        const hasSeenWelcome = context.globalState.get('hasSeenWelcome', false);
        const setupCompleted = context.globalState.get('setupCompleted', false);
        
        if (!hasSeenWelcome) {
            // Mark as seen immediately to prevent showing again
            await context.globalState.update('hasSeenWelcome', true);
            
            // Show welcome notification with setup action
            const action = await vscode.window.showInformationMessage(
                '🎉 Welcome to Architector-LLM! Let\'s set up your AI-powered documentation generator.',
                'Setup Now',
                'Later'
            );
            
            if (action === 'Setup Now') {
                const setupWizard = new SetupWizard(context);
                await setupWizard.run();
                // Show quick tip after successful setup
                if (context.globalState.get('setupCompleted', false)) {
                    setTimeout(() => setupWizard.showQuickTip(), 2000);
                }
            } else {
                // User chose "Later" - show reminder
                vscode.window.showInformationMessage(
                    'Setup incomplete. Run "Architector: Run Setup Wizard" from Command Palette (Cmd+Shift+P) when ready.',
                    'OK'
                );
            }
        } else if (!setupCompleted) {
            // Not first run, but setup not completed - show subtle reminder in status bar
            const reminder = vscode.window.setStatusBarMessage(
                '$(warning) Architector: Setup incomplete. Click "Architector" or run Setup Wizard',
                10000
            );
            context.subscriptions.push(reminder);
        }
    })();
}

async function generateDocumentation(context: vscode.ExtensionContext) {
    outputChannel.show();
    outputChannel.appendLine('Starting documentation generation...');
    
    // Track event
    const analytics = new AnalyticsManager(context);
    await analytics.trackEvent('generateDocs.started');
    
    const startTime = Date.now();
    
    // Get workspace folder
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }
    
    const projectPath = workspaceFolder.uri.fsPath;
    outputChannel.appendLine(`Project path: ${projectPath}`);
    
    // Check if LLM provider is configured
    const llmProvider = vscode.workspace.getConfiguration('architector').get<string>('llmProvider');
    if (!llmProvider) {
        // Run setup wizard if not configured
        const setupWizard = new SetupWizard(context);
        await setupWizard.run();
        return;
    }
    
    // If using API, check for API key
    if (llmProvider !== 'ollama') {
        const apiKeyManager = new ApiKeyManager(context);
        const hasKey = await apiKeyManager.hasApiKey(llmProvider);
        if (!hasKey) {
            const key = await apiKeyManager.promptForApiKey(llmProvider);
            if (!key) {
                vscode.window.showErrorMessage('API key is required to use cloud LLM provider');
                return;
            }
        }
    }
    
    // Check dependencies (cached after first check in session)
    if (!dependenciesChecked) {
        const checker = new DependencyChecker(outputChannel);
        const depsOk = await checker.checkAll();
        
        if (!depsOk) {
            const install = await vscode.window.showErrorMessage(
                'Some dependencies are missing. Would you like to see the installation guide?',
                'Yes', 'No'
            );
            if (install === 'Yes') {
                await vscode.commands.executeCommand('architector-llm.checkDependencies');
            }
            return;
        }
        
        // Cache successful check for this session
        dependenciesChecked = true;
        outputChannel.appendLine('✅ Dependencies cached for session\n');
    } else {
        outputChannel.appendLine('✅ Using cached dependency check\n');
    }
    
    // Ask for semantic version (with auto-detect option)
    const version = await vscode.window.showInputBox({
        prompt: 'Enter semantic version for documentation (leave empty to auto-detect from project files)',
        placeHolder: 'e.g., 1.0.0, 2.3.1, or leave empty for auto-detection',
        value: '',
        validateInput: (value) => {
            if (value && !/^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$/.test(value)) {
                return 'Please enter a valid semantic version (e.g., 1.0.0) or leave empty for auto-detection';
            }
            return null;
        }
    });
    
    if (version === undefined) {
        return; // User cancelled (ESC or close button)
    }
    
    // Empty string means auto-detect, which is valid
    const versionToUse = version.trim() || undefined;
    
    if (versionToUse) {
        outputChannel.appendLine(`📦 Using version: ${versionToUse}\n`);
    } else {
        outputChannel.appendLine('🔍 Version will be auto-detected from project files (package.json, pyproject.toml, etc.)\n');
    }
    
    // Show progress panel
    const progressPanel = new ProgressPanel(context.extensionUri);
    progressPanel.show();
    
    try {
        statusBarItem.text = "$(sync~spin) Generating...";
        
        // Set LLM provider environment variable
        const apiKeyManager = new ApiKeyManager(context);
        const apiKey = await apiKeyManager.getApiKey(llmProvider);
        
        // Run Python pipeline
        const runner = new PythonRunner(outputChannel);
        const extensionPath = context.extensionPath;
        const backendPath = path.join(extensionPath, 'backend', 'src');
        
        const result = await runner.runPipeline(
            projectPath,
            versionToUse,  // Can be undefined for auto-detection
            backendPath,
            (message) => {
                progressPanel.updateProgress(message);
            },
            {
                LLM_PROVIDER: llmProvider,
                ...(apiKey ? { [`${llmProvider.toUpperCase()}_API_KEY`]: apiKey } : {})
            }
        );
        
        statusBarItem.text = "$(book) Architector";
        
        const generationTime = (Date.now() - startTime) / 1000;
        
        if (result.success) {
            outputChannel.appendLine('\n✅ Documentation generated successfully!');
            outputChannel.appendLine(`Output: ${result.outputPath}`);
            
            progressPanel.updateProgress('✅ Complete! Opening documentation...');
            
            // Log analytics
            await analytics.logGeneration({
                projectPath,
                success: true,
                diagramsGenerated: result.diagrams || 0,
                generationTimeSeconds: generationTime,
                qualityScore: result.quality,
                validationScores: result.validationScores
            });
            
            // Show success message with options
            const action = await vscode.window.showInformationMessage(
                `Documentation generated successfully!\n${result.diagrams} diagrams created with ${result.quality}/100 quality score.`,
                'Open Documentation', 'Show in Finder', 'Close'
            );
            
            if (action === 'Open Documentation' && result.outputPath) {
                const readmePath = path.join(result.outputPath, 'README.md');
                const doc = await vscode.workspace.openTextDocument(readmePath);
                await vscode.window.showTextDocument(doc);
            } else if (action === 'Show in Finder' && result.outputPath) {
                vscode.commands.executeCommand('revealFileInOS', vscode.Uri.file(result.outputPath));
            }
            
            progressPanel.dispose();
        } else {
            outputChannel.appendLine(`\n❌ Error: ${result.error}`);
            vscode.window.showErrorMessage(`Documentation generation failed: ${result.error}`);
            progressPanel.updateProgress(`❌ Failed: ${result.error}`);
            
            // Log failure
            await analytics.logGeneration({
                projectPath,
                success: false,
                diagramsGenerated: 0,
                generationTimeSeconds: generationTime,
                errorType: result.error?.toString()
            });
            
            setTimeout(() => progressPanel.dispose(), 3000);
        }
        
    } catch (error) {
        statusBarItem.text = "$(book) Architector";
        outputChannel.appendLine(`\n❌ Error: ${error}`);
        vscode.window.showErrorMessage(`Documentation generation failed: ${error}`);
        progressPanel.dispose();
        
        // Log exception
        const generationTime = (Date.now() - startTime) / 1000;
        await analytics.logGeneration({
            projectPath,
            success: false,
            diagramsGenerated: 0,
            generationTimeSeconds: generationTime,
            errorType: error?.toString()
        });
    }
}

async function checkDependencies(context?: vscode.ExtensionContext) {
    // Track event if context provided
    if (context) {
        const analytics = new AnalyticsManager(context);
        await analytics.trackEvent('dependencyCheck');
    }
    
    const checker = new DependencyChecker(outputChannel);
    const panel = vscode.window.createWebviewPanel(
        'dependencyCheck',
        'Architector Dependencies',
        vscode.ViewColumn.One,
        {}
    );
    
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
    
    panel.webview.html = panel.webview.html.replace(
        '<div id="status">Loading...</div>',
        html
    );
}

async function showAbout(context: vscode.ExtensionContext) {
    const panel = vscode.window.createWebviewPanel(
        'architectorAbout',
        'About Architector-LLM',
        vscode.ViewColumn.One,
        { enableScripts: true, localResourceRoots: [context.extensionUri] }
    );
    
    const version = vscode.extensions.getExtension('architector.architector-llm')?.packageJSON.version || '1.0.0';
    
    // Get logo URI for webview
    const logoPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');
    const logoUri = panel.webview.asWebviewUri(logoPath);
    
    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>About Architector-LLM</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    padding: 0;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    line-height: 1.6;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }
                .header {
                    text-align: center;
                    margin-bottom: 40px;
                    animation: fadeIn 0.8s ease-in;
                }
                .logo {
                    width: 150px;
                    height: 150px;
                    margin: 0 auto 20px;
                    animation: float 3s ease-in-out infinite;
                }
                .logo img {
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                    filter: drop-shadow(0 10px 25px rgba(0, 0, 0, 0.3));
                }
                h1 {
                    font-size: 2.5em;
                    margin: 10px 0;
                    font-weight: 700;
                }
                .version {
                    font-size: 1.2em;
                    opacity: 0.9;
                    margin: 10px 0;
                }
                .tagline {
                    font-size: 1.1em;
                    opacity: 0.85;
                    font-style: italic;
                }
                .section {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 25px;
                    margin: 20px 0;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    animation: slideIn 0.6s ease-out;
                }
                .section h2 {
                    margin-top: 0;
                    font-size: 1.8em;
                    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .feature-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }
                .feature {
                    background: rgba(255, 255, 255, 0.15);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                }
                .feature-icon {
                    font-size: 2em;
                    margin-bottom: 10px;
                }
                .credit-item {
                    margin: 15px 0;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    border-left: 4px solid rgba(255, 255, 255, 0.5);
                }
                .credit-name {
                    font-weight: bold;
                    font-size: 1.1em;
                    margin-bottom: 5px;
                }
                .credit-role {
                    opacity: 0.85;
                    font-size: 0.95em;
                }
                .tech-stack {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin: 15px 0;
                }
                .tech-badge {
                    background: rgba(255, 255, 255, 0.2);
                    padding: 8px 15px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    font-weight: 500;
                }
                .stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }
                .stat {
                    text-align: center;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 10px;
                }
                .stat-value {
                    font-size: 2.5em;
                    font-weight: bold;
                    display: block;
                    margin-bottom: 5px;
                }
                .stat-label {
                    font-size: 0.9em;
                    opacity: 0.85;
                }
                a {
                    color: #FFD700;
                    text-decoration: none;
                    font-weight: 500;
                }
                a:hover {
                    text-decoration: underline;
                }
                .footer {
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid rgba(255, 255, 255, 0.3);
                    opacity: 0.85;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(-20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes slideIn {
                    from { opacity: 0; transform: translateX(-30px); }
                    to { opacity: 1; transform: translateX(0); }
                }
                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-15px); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">
                        <img src="${logoUri}" alt="Architector-LLM Logo">
                    </div>
                    <h1>Architector-LLM</h1>
                    <div class="version">Version ${version}</div>
                    <div class="tagline">Automated Architecture Documentation Generation</div>
                </div>

                <div class="section">
                    <h2>🎯 What is Architector?</h2>
                    <p>Architector-LLM is an intelligent VS Code extension that automatically generates comprehensive architecture documentation for your codebase using Large Language Models (LLMs).</p>
                    <p><strong>🔬 Research Prototype:</strong> This extension is a prototype developed for the research paper <em>"From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"</em>.</p>
                    <div class="feature-grid">
                        <div class="feature">
                            <div class="feature-icon">📊</div>
                            <strong>10 Diagram Types</strong>
                            <div>Component, Class, Sequence, Activity, Data Flow, C4, ER, and more</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🤖</div>
                            <strong>AI-Powered</strong>
                            <div>Uses DeepSeek Coder 6.7B via Ollama</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">✅</div>
                            <strong>Quality Validation</strong>
                            <div>4-component validation system</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🔗</div>
                            <strong>Smart Relationships</strong>
                            <div>Cross-diagram entity mapping</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>📈 Project Statistics</h2>
                    <div class="stats">
                        <div class="stat">
                            <span class="stat-value">6,123</span>
                            <span class="stat-label">Lines of Code</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">23</span>
                            <span class="stat-label">Backend Modules</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">10</span>
                            <span class="stat-label">Diagram Types</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">4</span>
                            <span class="stat-label">Validation Dimensions</span>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>👨‍💻 Author</h2>
                    <div class="credit-item">
                        <div class="credit-name">🧑‍💻 Engr. Hammad Khurshid</div>
                        <div class="credit-role">Department of Software Engineering</div>
                        <div class="credit-role">National University of Science and Technology (NUST), Pakistan</div>
                        <div class="credit-role" style="margin-top: 10px;">
                            📧 <a href="mailto:engr.hammadkhurshid@gmail.com">engr.hammadkhurshid@gmail.com</a><br>
                            📧 <a href="mailto:hkhurshid.cse25ceme@student.nust.edu.pk">hkhurshid.cse25ceme@student.nust.edu.pk</a><br>
                            💻 <a href="https://github.com/engrhammadkhurshid">github.com/engrhammadkhurshid</a>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>🛠️ Technology Stack</h2>
                    <div class="tech-stack">
                        <span class="tech-badge">🐍 Python 3.9+</span>
                        <span class="tech-badge">📘 TypeScript</span>
                        <span class="tech-badge">🔷 VS Code API</span>
                        <span class="tech-badge">🦙 Ollama</span>
                        <span class="tech-badge">🤖 DeepSeek Coder 6.7B</span>
                        <span class="tech-badge">🌳 Tree-sitter</span>
                        <span class="tech-badge">🧜‍♀️ Mermaid.js</span>
                        <span class="tech-badge">⚡ Node.js</span>
                    </div>
                </div>

                <div class="section">
                    <h2>📄 License & Repository</h2>
                    <p><strong>License:</strong> MIT License</p>
                    <p><strong>Repository:</strong> <a href="https://github.com/engrhammadkhurshid/architector-llm">github.com/engrhammadkhurshid/architector-llm</a></p>
                    <p><strong>Release Date:</strong> January 23, 2026</p>
                    <p><strong>Research Paper:</strong> <em>"From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"</em></p>
                    <p><strong>Institution:</strong> National University of Science and Technology (NUST), Pakistan</p>
                </div>

                <div class="section">
                    <h2>🚀 Features</h2>
                    <ul>
                        <li>✨ <strong>Multi-Diagram Generation:</strong> 10 different diagram types automatically selected based on codebase</li>
                        <li>📊 <strong>Quality Validation:</strong> 4-dimension validation (Syntax, Completeness, Clarity, Accuracy)</li>
                        <li>🔗 <strong>Relationship Mapping:</strong> Automatic cross-diagram entity tracking</li>
                        <li>📝 <strong>Interactive Documentation:</strong> Enhanced navigation with comparisons</li>
                        <li>⚡ <strong>Parallel Processing:</strong> Fast diagram generation with configurable parallelism</li>
                        <li>🎨 <strong>Beautiful UI:</strong> Animated progress panel with real-time updates</li>
                        <li>🔍 <strong>Dependency Checking:</strong> Automatic verification of required tools</li>
                        <li>📦 <strong>Easy Installation:</strong> One-click extension installation</li>
                    </ul>
                </div>

                <div class="footer">
                    <p>© 2026 Engr. Hammad Khurshid</p>
                    <p>National University of Science and Technology (NUST), Pakistan</p>
                    <p>Research Prototype for Academic Publication</p>
                    <p>Thank you for using Architector-LLM! 🎉</p>
                </div>
            </div>
        </body>
        </html>
    `;
    
    // Track about page view
    const analytics = new AnalyticsManager(context);
    await analytics.trackEvent('aboutPageView');
}

async function showPrivacyPolicy(context: vscode.ExtensionContext) {
    const privacyPolicyPath = path.join(
        path.dirname(context.extensionPath),
        'PRIVACY_POLICY.md'
    );
    
    try {
        const doc = await vscode.workspace.openTextDocument(privacyPolicyPath);
        await vscode.window.showTextDocument(doc, { preview: false });
    } catch (error) {
        vscode.window.showErrorMessage('Privacy policy file not found');
    }
}

export function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
    if (outputChannel) {
        outputChannel.dispose();
    }
}
