/**
 * Dependency Checker
 * Verifies that Python, Ollama, and other dependencies are installed
 */

import * as vscode from 'vscode';
import * as child_process from 'child_process';
import { promisify } from 'util';

const exec = promisify(child_process.exec);

export interface DependencyResult {
    installed: boolean;
    version?: string;
    message?: string;
    installCmd?: string;
}

export class DependencyChecker {
    constructor(private outputChannel: vscode.OutputChannel) {}
    
    async checkAll(): Promise<boolean> {
        this.outputChannel.appendLine('\n🔍 Checking dependencies...');
        
        const pythonOk = await this.checkPython();
        const ollamaOk = await this.checkOllama();
        const mermaidOk = await this.checkMermaid();
        
        const allOk = pythonOk && ollamaOk && mermaidOk;
        
        if (allOk) {
            this.outputChannel.appendLine('✅ All dependencies are installed\n');
        } else {
            this.outputChannel.appendLine('❌ Some dependencies are missing\n');
        }
        
        return allOk;
    }
    
    async checkAllDetailed(): Promise<Record<string, DependencyResult>> {
        return {
            'Python 3.9+': await this.checkPythonDetailed(),
            'Ollama': await this.checkOllamaDetailed(),
            'DeepSeek Coder Model': await this.checkDeepseekModel(),
            'Mermaid CLI': await this.checkMermaidDetailed(),
            'Tree-sitter': await this.checkTreesitter()
        };
    }
    
    private async checkPython(): Promise<boolean> {
        try {
            const { stdout } = await exec('python3 --version');
            const version = stdout.trim();
            this.outputChannel.appendLine(`✅ Python: ${version}`);
            return true;
        } catch (error) {
            this.outputChannel.appendLine('❌ Python 3 not found');
            return false;
        }
    }
    
    private async checkPythonDetailed(): Promise<DependencyResult> {
        try {
            const { stdout } = await exec('python3 --version');
            const version = stdout.trim().replace('Python ', '');
            return {
                installed: true,
                version,
                message: 'Python 3 is installed'
            };
        } catch (error) {
            return {
                installed: false,
                message: 'Python 3.9+ is required',
                installCmd: '# macOS\nbrew install python3\n\n# Ubuntu/Debian\nsudo apt install python3'
            };
        }
    }
    
    private async checkOllama(): Promise<boolean> {
        try {
            const { stdout } = await exec('curl -s http://localhost:11434/api/tags');
            this.outputChannel.appendLine('✅ Ollama: Running');
            return true;
        } catch (error) {
            this.outputChannel.appendLine('❌ Ollama not running');
            return false;
        }
    }
    
    private async checkOllamaDetailed(): Promise<DependencyResult> {
        try {
            const { stdout } = await exec('curl -s http://localhost:11434/api/tags');
            const data = JSON.parse(stdout);
            const models = data.models || [];
            return {
                installed: true,
                version: `${models.length} models available`,
                message: 'Ollama is running'
            };
        } catch (error) {
            return {
                installed: false,
                message: 'Ollama must be running',
                installCmd: '# macOS\ncurl https://ollama.ai/install.sh | sh\nollama serve\n\n# Or download from https://ollama.ai'
            };
        }
    }
    
    private async checkDeepseekModel(): Promise<DependencyResult> {
        try {
            const { stdout } = await exec('curl -s http://localhost:11434/api/tags');
            const data = JSON.parse(stdout);
            const models = data.models || [];
            const hasDeepseek = models.some((m: any) => 
                m.name && m.name.includes('deepseek-coder')
            );
            
            if (hasDeepseek) {
                return {
                    installed: true,
                    message: 'DeepSeek Coder model is available'
                };
            } else {
                return {
                    installed: false,
                    message: 'DeepSeek Coder model not found',
                    installCmd: 'ollama pull deepseek-coder:6.7b'
                };
            }
        } catch (error) {
            return {
                installed: false,
                message: 'Cannot check - Ollama not running',
                installCmd: 'ollama pull deepseek-coder:6.7b'
            };
        }
    }
    
    private async checkMermaid(): Promise<boolean> {
        try {
            await exec('mmdc --version');
            this.outputChannel.appendLine('✅ Mermaid CLI: Installed');
            return true;
        } catch (error) {
            this.outputChannel.appendLine('⚠️  Mermaid CLI: Not found (optional)');
            return true; // Optional dependency
        }
    }
    
    private async checkMermaidDetailed(): Promise<DependencyResult> {
        try {
            const { stdout } = await exec('mmdc --version');
            const version = stdout.trim();
            return {
                installed: true,
                version,
                message: 'Mermaid CLI for rendering diagrams (optional)'
            };
        } catch (error) {
            return {
                installed: false,
                message: 'Optional: For rendering diagram images',
                installCmd: 'npm install -g @mermaid-js/mermaid-cli'
            };
        }
    }
    
    private async checkTreesitter(): Promise<DependencyResult> {
        try {
            const { stdout } = await exec('python3 -c "import tree_sitter; print(tree_sitter.__version__)"');
            const version = stdout.trim();
            return {
                installed: true,
                version,
                message: 'Tree-sitter for code parsing'
            };
        } catch (error) {
            return {
                installed: false,
                message: 'Required for code parsing',
                installCmd: 'pip3 install tree-sitter'
            };
        }
    }
}
