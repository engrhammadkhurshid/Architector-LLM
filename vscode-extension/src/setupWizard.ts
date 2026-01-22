/**
 * Setup Wizard - First Run Experience
 * Guides users through LLM provider selection and configuration
 */

import * as vscode from 'vscode';
import { ApiKeyManager } from './apiKeyManager';
import { DeveloperInfoManager } from './analytics/developerInfo';

export class SetupWizard {
    constructor(private context: vscode.ExtensionContext) {}
    
    async run(): Promise<void> {
        // Check if setup already completed
        const setupCompleted = this.context.globalState.get('setupCompleted', false);
        if (setupCompleted) {
            return;
        }
        
        // Welcome screen
        const proceed = await vscode.window.showInformationMessage(
            '🎉 Welcome to Architector-LLM!\\n\\nLet\'s set up your documentation generator in 2 minutes.',
            { modal: true },
            'Get Started',
            'Later'
        );
        
        if (proceed !== 'Get Started') {
            return;
        }
        
        // Step 1: Choose LLM Provider
        const provider = await this.selectLLMProvider();
        if (!provider) return;
        
        await vscode.workspace.getConfiguration('architector').update(
            'llmProvider',
            provider,
            vscode.ConfigurationTarget.Global
        );
        
        // Step 2: Configure selected provider
        if (provider !== 'ollama') {
            const configured = await this.configureAPIProvider(provider);
            if (!configured) return;
        } else {
            await this.showOllamaInstructions();
        }
        
        // Step 3: Research participation (optional)
        await this.askResearchParticipation();
        
        // Mark setup as complete
        await this.context.globalState.update('setupCompleted', true);
        
        vscode.window.showInformationMessage(
            '✅ Setup complete! Click "Architector" in the status bar to generate documentation.',
            'Got it!'
        );
    }
    
    private async selectLLMProvider(): Promise<string | undefined> {
        // Auto-detect if Ollama is already installed and running
        const ollamaDetected = await this.detectOllama();
        const modelDetected = ollamaDetected ? await this.detectDeepseekModel() : false;
        
        // Build options with detection info
        const options = [
            {
                label: '$(cloud) Cloud API',
                detail: 'Use DeepSeek, OpenAI, or Claude API - Instant setup, requires API key',
                value: 'api'
            },
            {
                label: ollamaDetected 
                    ? '$(check) Local LLM (Ollama) - Detected!' 
                    : '$(desktop-download) Local LLM (Ollama)',
                detail: ollamaDetected
                    ? (modelDetected 
                        ? '✅ Ollama is running with deepseek-coder model - Ready to use!'
                        : '⚠️  Ollama running, but deepseek-coder model needs to be downloaded')
                    : 'Free, private, but requires 3.8GB model download',
                value: 'ollama'
            }
        ];
        
        const choice = await vscode.window.showQuickPick(options, {
            placeHolder: ollamaDetected 
                ? '✨ Ollama detected! Choose your preferred option or use the detected installation'
                : 'Choose how you want to run the LLM',
            ignoreFocusOut: true
        });
        
        if (!choice) return undefined;
        
        if (choice.value === 'api') {
            return await this.selectAPIProvider();
        }
        
        return 'ollama';
    }
    
    private async selectAPIProvider(): Promise<string | undefined> {
        const provider = await vscode.window.showQuickPick([
            {
                label: '$(star) DeepSeek',
                detail: 'Recommended - Fast and affordable ($0.14/1M tokens)',
                value: 'deepseek'
            },
            {
                label: '$(symbol-misc) OpenAI GPT-4',
                detail: 'Most capable but expensive ($30/1M tokens)',
                value: 'openai'
            },
            {
                label: '$(globe) Anthropic Claude',
                detail: 'High quality, good for complex code ($15/1M tokens)',
                value: 'claude'
            }
        ], {
            placeHolder: 'Select your API provider',
            ignoreFocusOut: true
        });
        
        return provider?.value;
    }
    
    private async configureAPIProvider(provider: string): Promise<boolean> {
        const apiKeyManager = new ApiKeyManager(this.context);
        
        // Show instructions
        const providerInfo = {
            'deepseek': {
                name: 'DeepSeek',
                url: 'https://platform.deepseek.com/api_keys',
                example: 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            },
            'openai': {
                name: 'OpenAI',
                url: 'https://platform.openai.com/api-keys',
                example: 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            },
            'claude': {
                name: 'Anthropic Claude',
                url: 'https://console.anthropic.com/settings/keys',
                example: 'sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            }
        };
        
        const info = providerInfo[provider as keyof typeof providerInfo];
        
        const getKey = await vscode.window.showInformationMessage(
            `📋 Get your ${info.name} API key:\\n\\n1. Visit: ${info.url}\\n2. Create or copy your API key\\n3. Paste it in the next step`,
            { modal: true },
            'Open URL',
            'I have my key'
        );
        
        if (getKey === 'Open URL') {
            vscode.env.openExternal(vscode.Uri.parse(info.url));
        }
        
        // Prompt for API key
        const apiKey = await vscode.window.showInputBox({
            prompt: `Enter your ${info.name} API key`,
            placeHolder: info.example,
            password: true,
            ignoreFocusOut: true,
            validateInput: (value) => {
                if (!value || value.length < 20) {
                    return 'API key seems too short. Please check and try again.';
                }
                return null;
            }
        });
        
        if (!apiKey) return false;
        
        // Store API key securely
        await apiKeyManager.storeApiKey(provider, apiKey);
        
        // Test connection
        const testing = vscode.window.setStatusBarMessage('$(sync~spin) Testing API connection...');
        const isValid = await apiKeyManager.testConnection(provider, apiKey);
        testing.dispose();
        
        if (isValid) {
            vscode.window.showInformationMessage(`✅ ${info.name} API key verified!`);
            return true;
        } else {
            const retry = await vscode.window.showErrorMessage(
                `❌ Failed to verify API key. Please check and try again.`,
                'Retry',
                'Skip'
            );
            if (retry === 'Retry') {
                return await this.configureAPIProvider(provider);
            }
            return false;
        }
    }
    
    private async showOllamaInstructions(): Promise<void> {
        // Check if Ollama is already set up
        const ollamaRunning = await this.detectOllama();
        const modelAvailable = ollamaRunning ? await this.detectDeepseekModel() : false;
        
        if (ollamaRunning && modelAvailable) {
            vscode.window.showInformationMessage(
                '✅ Ollama is already set up and ready!\\n\\nModel: deepseek-coder:6.7b is available.',
                'Got it!'
            );
            return;
        }
        
        if (ollamaRunning && !modelAvailable) {
            const download = await vscode.window.showInformationMessage(
                '⚠️  Ollama is running, but deepseek-coder model is missing.\\n\\n' +
                'Download the model now (~3.8GB)?',
                { modal: true },
                'Download Model',
                'Manual Setup'
            );
            
            if (download === 'Download Model') {
                vscode.window.showInformationMessage(
                    'Run this command in your terminal:\\n\\n' +
                    'ollama pull deepseek-coder:6.7b',
                    'Copy Command'
                ).then(result => {
                    if (result === 'Copy Command') {
                        vscode.env.clipboard.writeText('ollama pull deepseek-coder:6.7b');
                    }
                });
            }
            return;
        }
        
        const result = await vscode.window.showInformationMessage(
            '📦 Local LLM Setup Required:\\n\\n' +
            '1. Install Ollama: https://ollama.ai\\n' +
            '2. Run: ollama pull deepseek-coder:6.7b\\n' +
            '3. Start: ollama serve\\n\\n' +
            'This is a one-time setup (~3.8GB download).',
            { modal: true },
            'Open Ollama Website',
            'Check Dependencies'
        );
        
        if (result === 'Open Ollama Website') {
            vscode.env.openExternal(vscode.Uri.parse('https://ollama.ai'));
        } else if (result === 'Check Dependencies') {
            vscode.commands.executeCommand('architector-llm.checkDependencies');
        }
    }
    
    private async askResearchParticipation(): Promise<void> {
        const devInfoManager = new DeveloperInfoManager(this.context);
        
        const participate = await vscode.window.showInformationMessage(
            '📊 Research Study Participation\\n\\n' +
            'This extension is part of research at NUST Pakistan. ' +
            'Would you like to help improve this tool by sharing anonymous usage data?\\n\\n' +
            '✅ What we collect: Usage stats, performance metrics\\n' +
            '❌ What we DON\'T collect: Your code or sensitive data',
            { modal: true },
            'Learn More',
            'Yes, Help Research',
            'No Thanks'
        );
        
        if (participate === 'Learn More') {
            vscode.commands.executeCommand('architector-llm.showPrivacyPolicy');
            // Ask again after showing policy
            const decision = await vscode.window.showInformationMessage(
                'Would you like to participate in the research study?',
                'Yes, Help Research',
                'No Thanks'
            );
            if (decision === 'Yes, Help Research') {
                await devInfoManager.showConsentDialog();
            }
        } else if (participate === 'Yes, Help Research') {
            await devInfoManager.showConsentDialog();
        }
    }
    
    /**
     * Detect if Ollama is installed and running
     */
    private async detectOllama(): Promise<boolean> {
        try {
            const { exec } = require('child_process');
            const { promisify } = require('util');
            const execAsync = promisify(exec);
            
            const { stdout } = await execAsync('curl -s --max-time 2 http://localhost:11434/api/tags');
            const data = JSON.parse(stdout);
            return data.models !== undefined;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Detect if deepseek-coder model is available in Ollama
     */
    private async detectDeepseekModel(): Promise<boolean> {
        try {
            const { exec } = require('child_process');
            const { promisify } = require('util');
            const execAsync = promisify(exec);
            
            const { stdout } = await execAsync('curl -s --max-time 2 http://localhost:11434/api/tags');
            const data = JSON.parse(stdout);
            const models = data.models || [];
            return models.some((m: any) => m.name && m.name.includes('deepseek-coder'));
        } catch (error) {
            return false;
        }
    }
    
    async showQuickTip(): Promise<void> {
        const tip = await vscode.window.showInformationMessage(
            '💡 Quick Tip: Click "Architector" in the status bar to generate documentation for your current project!',
            'Try it now',
            'Dismiss'
        );
        
        if (tip === 'Try it now') {
            vscode.commands.executeCommand('architector-llm.generateDocs');
        }
    }
}
