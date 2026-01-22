"use strict";
/**
 * Dependency Checker
 * Verifies that Python, Ollama, and other dependencies are installed
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
exports.DependencyChecker = void 0;
const child_process = __importStar(require("child_process"));
const util_1 = require("util");
const exec = (0, util_1.promisify)(child_process.exec);
class DependencyChecker {
    constructor(outputChannel) {
        this.outputChannel = outputChannel;
    }
    async checkAll() {
        this.outputChannel.appendLine('\n🔍 Checking dependencies...');
        const pythonOk = await this.checkPython();
        const ollamaOk = await this.checkOllama();
        const mermaidOk = await this.checkMermaid();
        const allOk = pythonOk && ollamaOk && mermaidOk;
        if (allOk) {
            this.outputChannel.appendLine('✅ All dependencies are installed\n');
        }
        else {
            this.outputChannel.appendLine('❌ Some dependencies are missing\n');
        }
        return allOk;
    }
    async checkAllDetailed() {
        return {
            'Python 3.9+': await this.checkPythonDetailed(),
            'Ollama': await this.checkOllamaDetailed(),
            'DeepSeek Coder Model': await this.checkDeepseekModel(),
            'Mermaid CLI': await this.checkMermaidDetailed(),
            'Tree-sitter': await this.checkTreesitter()
        };
    }
    async checkPython() {
        try {
            const { stdout } = await exec('python3 --version');
            const version = stdout.trim();
            this.outputChannel.appendLine(`✅ Python: ${version}`);
            return true;
        }
        catch (error) {
            this.outputChannel.appendLine('❌ Python 3 not found');
            return false;
        }
    }
    async checkPythonDetailed() {
        try {
            const { stdout } = await exec('python3 --version');
            const version = stdout.trim().replace('Python ', '');
            return {
                installed: true,
                version,
                message: 'Python 3 is installed'
            };
        }
        catch (error) {
            return {
                installed: false,
                message: 'Python 3.9+ is required',
                installCmd: '# macOS\nbrew install python3\n\n# Ubuntu/Debian\nsudo apt install python3'
            };
        }
    }
    async checkOllama() {
        try {
            const { stdout } = await exec('curl -s http://localhost:11434/api/tags');
            this.outputChannel.appendLine('✅ Ollama: Running');
            return true;
        }
        catch (error) {
            this.outputChannel.appendLine('❌ Ollama not running');
            return false;
        }
    }
    async checkOllamaDetailed() {
        try {
            const { stdout } = await exec('curl -s http://localhost:11434/api/tags');
            const data = JSON.parse(stdout);
            const models = data.models || [];
            return {
                installed: true,
                version: `${models.length} models available`,
                message: 'Ollama is running'
            };
        }
        catch (error) {
            return {
                installed: false,
                message: 'Ollama must be running',
                installCmd: '# macOS\ncurl https://ollama.ai/install.sh | sh\nollama serve\n\n# Or download from https://ollama.ai'
            };
        }
    }
    async checkDeepseekModel() {
        try {
            const { stdout } = await exec('curl -s http://localhost:11434/api/tags');
            const data = JSON.parse(stdout);
            const models = data.models || [];
            const hasDeepseek = models.some((m) => m.name && m.name.includes('deepseek-coder'));
            if (hasDeepseek) {
                return {
                    installed: true,
                    message: 'DeepSeek Coder model is available'
                };
            }
            else {
                return {
                    installed: false,
                    message: 'DeepSeek Coder model not found',
                    installCmd: 'ollama pull deepseek-coder:6.7b'
                };
            }
        }
        catch (error) {
            return {
                installed: false,
                message: 'Cannot check - Ollama not running',
                installCmd: 'ollama pull deepseek-coder:6.7b'
            };
        }
    }
    async checkMermaid() {
        try {
            await exec('mmdc --version');
            this.outputChannel.appendLine('✅ Mermaid CLI: Installed');
            return true;
        }
        catch (error) {
            this.outputChannel.appendLine('⚠️  Mermaid CLI: Not found (optional)');
            return true; // Optional dependency
        }
    }
    async checkMermaidDetailed() {
        try {
            const { stdout } = await exec('mmdc --version');
            const version = stdout.trim();
            return {
                installed: true,
                version,
                message: 'Mermaid CLI for rendering diagrams (optional)'
            };
        }
        catch (error) {
            return {
                installed: false,
                message: 'Optional: For rendering diagram images',
                installCmd: 'npm install -g @mermaid-js/mermaid-cli'
            };
        }
    }
    async checkTreesitter() {
        try {
            const { stdout } = await exec('python3 -c "import tree_sitter; print(tree_sitter.__version__)"');
            const version = stdout.trim();
            return {
                installed: true,
                version,
                message: 'Tree-sitter for code parsing'
            };
        }
        catch (error) {
            return {
                installed: false,
                message: 'Required for code parsing',
                installCmd: 'pip3 install tree-sitter'
            };
        }
    }
}
exports.DependencyChecker = DependencyChecker;
//# sourceMappingURL=dependencyChecker.js.map