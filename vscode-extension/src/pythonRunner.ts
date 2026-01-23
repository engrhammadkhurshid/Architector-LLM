/**
 * Python Runner
 * Executes the Python backend pipeline and captures output
 */

import * as vscode from 'vscode';
import * as child_process from 'child_process';
import * as path from 'path';

export interface PipelineResult {
    success: boolean;
    outputPath?: string;
    diagrams?: number;
    quality?: number;
    validationScores?: {
        syntax: number;
        completeness: number;
        clarity: number;
        accuracy: number;
    };
    error?: string;
}

export class PythonRunner {
    constructor(private outputChannel: vscode.OutputChannel) {}
    
    async runPipeline(
        projectPath: string,
        version: string | undefined,
        backendPath: string,
        progressCallback?: (message: string) => void,
        envVars?: Record<string, string>
    ): Promise<PipelineResult> {
        return new Promise((resolve, reject) => {
            // Find architector.py in the extension directory
            const extensionRoot = path.dirname(path.dirname(__dirname));
            const architectorScript = path.join(extensionRoot, 'architector.py');
            
            // Build command args - only include version if provided
            const args = version ? [architectorScript, projectPath, version] : [architectorScript, projectPath];
            const versionStr = version || 'auto-detect';
            
            this.outputChannel.appendLine(`Running: python3 ${architectorScript} ${projectPath} ${versionStr}`);
            
            if (progressCallback) {
                progressCallback('Starting analysis...');
            }
            
            // Set PYTHONPATH to include backend/src and merge custom env vars
            const env: NodeJS.ProcessEnv = { ...process.env, ...envVars };
            env.PYTHONPATH = backendPath;
            
            const childProcess = child_process.spawn(
                'python3',
                args,
                { env, cwd: extensionRoot }
            );
            
            let output = '';
            let errorOutput = '';
            
            childProcess.stdout?.on('data', (data: Buffer) => {
                const text = data.toString();
                output += text;
                this.outputChannel.append(text);
                
                // Parse progress messages
                if (progressCallback) {
                    if (text.includes('Stage 1:')) {
                        progressCallback('📝 Parsing codebase...');
                    } else if (text.includes('Stage 2:')) {
                        progressCallback('🔗 Building dependency graph...');
                    } else if (text.includes('Stage 3:')) {
                        progressCallback('🔍 Analyzing codebase...');
                    } else if (text.includes('Stage 4:')) {
                        progressCallback('📋 Selecting diagrams...');
                    } else if (text.includes('Stage 5:')) {
                        progressCallback('🎨 Generating diagrams...');
                    } else if (text.includes('Stage 6:')) {
                        progressCallback('✅ Validating diagrams...');
                    } else if (text.includes('Stage 7:')) {
                        progressCallback('📊 Generating quality report...');
                    } else if (text.includes('Stage 8:')) {
                        progressCallback('📄 Creating documentation...');
                    }
                }
            });
            
            childProcess.stderr?.on('data', (data: Buffer) => {
                const text = data.toString();
                errorOutput += text;
                this.outputChannel.append(text);
            });
            
            childProcess.on('close', (code: number | null) => {
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
                } else {
                    const errorMatch = errorOutput.match(/Error: (.+)/) || 
                                      output.match(/❌ FAILED: (.+)/);
                    resolve({
                        success: false,
                        error: errorMatch ? errorMatch[1] : `Process exited with code ${code}`
                    });
                }
            });
            
            childProcess.on('error', (error: Error) => {
                reject(error);
            });
        });
    }
}
