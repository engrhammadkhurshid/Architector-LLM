/**
 * API Key Manager
 * Securely stores and manages API keys for different LLM providers
 */

import * as vscode from 'vscode';

export class ApiKeyManager {
    constructor(private context: vscode.ExtensionContext) {}
    
    async storeApiKey(provider: string, apiKey: string): Promise<void> {
        await this.context.secrets.store(`architector.apiKey.${provider}`, apiKey);
    }
    
    async getApiKey(provider: string): Promise<string | undefined> {
        return await this.context.secrets.get(`architector.apiKey.${provider}`);
    }
    
    async deleteApiKey(provider: string): Promise<void> {
        await this.context.secrets.delete(`architector.apiKey.${provider}`);
    }
    
    async hasApiKey(provider: string): Promise<boolean> {
        const key = await this.getApiKey(provider);
        return !!key;
    }
    
    async testConnection(provider: string, apiKey: string): Promise<boolean> {
        try {
            switch (provider) {
                case 'deepseek':
                    return await this.testDeepSeek(apiKey);
                case 'openai':
                    return await this.testOpenAI(apiKey);
                case 'claude':
                    return await this.testClaude(apiKey);
                default:
                    return false;
            }
        } catch (error) {
            console.error('API test failed:', error);
            return false;
        }
    }
    
    private async testDeepSeek(apiKey: string): Promise<boolean> {
        try {
            const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'deepseek-coder',
                    messages: [{ role: 'user', content: 'test' }],
                    max_tokens: 10
                })
            });
            return response.ok || response.status === 429; // 429 = rate limit (but key valid)
        } catch {
            return false;
        }
    }
    
    private async testOpenAI(apiKey: string): Promise<boolean> {
        try {
            const response = await fetch('https://api.openai.com/v1/models', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${apiKey}`
                }
            });
            return response.ok;
        } catch {
            return false;
        }
    }
    
    private async testClaude(apiKey: string): Promise<boolean> {
        try {
            const response = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'x-api-key': apiKey,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'claude-3-sonnet-20240229',
                    messages: [{ role: 'user', content: 'test' }],
                    max_tokens: 10
                })
            });
            return response.ok || response.status === 429;
        } catch {
            return false;
        }
    }
    
    async promptForApiKey(provider: string): Promise<string | undefined> {
        const providerNames = {
            'deepseek': 'DeepSeek',
            'openai': 'OpenAI',
            'claude': 'Anthropic Claude'
        };
        
        const name = providerNames[provider as keyof typeof providerNames] || provider;
        
        const apiKey = await vscode.window.showInputBox({
            prompt: `Enter your ${name} API key`,
            password: true,
            ignoreFocusOut: true,
            validateInput: (value) => {
                if (!value || value.length < 20) {
                    return 'API key seems too short';
                }
                return null;
            }
        });
        
        if (apiKey) {
            await this.storeApiKey(provider, apiKey);
        }
        
        return apiKey;
    }
}
