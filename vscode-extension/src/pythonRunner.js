"use strict";
/**
 * Python Runner
 * Executes the Python backend pipeline and captures output
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
exports.PythonRunner = void 0;
const child_process = __importStar(require("child_process"));
const path = __importStar(require("path"));
class PythonRunner {
    constructor(outputChannel) {
        this.outputChannel = outputChannel;
    }
    async runPipeline(projectPath, version, backendPath, progressCallback) {
        return new Promise((resolve, reject) => {
            // Find architector.py in the parent directory of vscode-extension
            const extensionParent = path.dirname(path.dirname(__dirname));
            const architectorScript = path.join(extensionParent, 'architector.py');
            this.outputChannel.appendLine(`Running: python3 ${architectorScript} ${projectPath} ${version}`);
            if (progressCallback) {
                progressCallback('Starting analysis...');
            }
            // Set PYTHONPATH to include backend/src
            const env = { ...process.env };
            env.PYTHONPATH = backendPath;
            const process = child_process.spawn('python3', [architectorScript, projectPath, version], { env, cwd: extensionParent });
            let output = '';
            let errorOutput = '';
            process.stdout?.on('data', (data) => {
                const text = data.toString();
                output += text;
                this.outputChannel.append(text);
                // Parse progress messages
                if (progressCallback) {
                    if (text.includes('Stage 1:')) {
                        progressCallback('📝 Parsing codebase...');
                    }
                    else if (text.includes('Stage 2:')) {
                        progressCallback('🔗 Building dependency graph...');
                    }
                    else if (text.includes('Stage 3:')) {
                        progressCallback('🔍 Analyzing codebase...');
                    }
                    else if (text.includes('Stage 4:')) {
                        progressCallback('📋 Selecting diagrams...');
                    }
                    else if (text.includes('Stage 5:')) {
                        progressCallback('🎨 Generating diagrams...');
                    }
                    else if (text.includes('Stage 6:')) {
                        progressCallback('✅ Validating diagrams...');
                    }
                    else if (text.includes('Stage 7:')) {
                        progressCallback('📊 Generating quality report...');
                    }
                    else if (text.includes('Stage 8:')) {
                        progressCallback('📄 Creating documentation...');
                    }
                }
            });
            process.stderr?.on('data', (data) => {
                const text = data.toString();
                errorOutput += text;
                this.outputChannel.append(text);
            });
            process.on('close', (code) => {
                if (code === 0) {
                    // Parse output for metrics
                    const outputMatch = output.match(/Output: (.+)/);
                    const diagramsMatch = output.match(/Diagrams: (\d+)\/\d+/);
                    const qualityMatch = output.match(/Quality: ([\d.]+)\/100/);
                    resolve({
                        success: true,
                        outputPath: outputMatch ? outputMatch[1].trim() : undefined,
                        diagrams: diagramsMatch ? parseInt(diagramsMatch[1]) : undefined,
                        quality: qualityMatch ? parseFloat(qualityMatch[1]) : undefined
                    });
                }
                else {
                    const errorMatch = errorOutput.match(/Error: (.+)/) ||
                        output.match(/❌ FAILED: (.+)/);
                    resolve({
                        success: false,
                        error: errorMatch ? errorMatch[1] : `Process exited with code ${code}`
                    });
                }
            });
            process.on('error', (error) => {
                reject(error);
            });
        });
    }
}
exports.PythonRunner = PythonRunner;
//# sourceMappingURL=pythonRunner.js.map