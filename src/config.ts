import * as vscode from 'vscode';

export function getBackendUrl(): string {
    const config = vscode.workspace.getConfiguration('architector');
    const port = config.get<number>('backendPort') || 8765;
    return `http://localhost:${port}`;
}

export function getOutputDirectory(): string {
    const config = vscode.workspace.getConfiguration('architector');
    return config.get<string>('outputDirectory') || 'docs/arch';
}
