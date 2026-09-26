/**
 * Analytics & Telemetry Manager
 * Collects anonymous usage data for research purposes
 */

import * as vscode from 'vscode';
import { DeveloperInfoManager } from './developerInfo';
import * as fs from 'fs';
import * as path from 'path';

export interface SessionData {
    sessionId: string;
    participantId: string;
    timestamp: string;
    extensionVersion: string;
    vscodeVersion: string;
    platform: string;
    
    // Project information
    projectLanguage: string;
    projectType: string;
    projectSize: 'small' | 'medium' | 'large' | 'enterprise';
    fileCount: number;
    lineCount?: number;
    
    // Generation metrics
    diagramsGenerated: number;
    diagramTypes: string[];
    generationTimeSeconds: number;
    success: boolean;
    errorType?: string;
    
    // Quality metrics
    qualityScore?: number;
    validationScores?: {
        syntax: number;
        completeness: number;
        clarity: number;
        accuracy: number;
    };
    
    // LLM configuration
    llmProvider: string;
    modelName?: string;
    
    // User interactions
    dependencyCheckRun: boolean;
    aboutPageViewed: boolean;
    setupWizardCompleted: boolean;
}

export interface ProjectMetadata {
    language: string;
    type: string;
    size: 'small' | 'medium' | 'large' | 'enterprise';
    fileCount: number;
    lineCount?: number;
}

export class AnalyticsManager {
    private sessionId: string;
    private logFilePath: string;
    
    constructor(private context: vscode.ExtensionContext) {
        this.sessionId = this.generateSessionId();
        this.logFilePath = path.join(
            context.globalStorageUri.fsPath,
            'analytics',
            'sessions.jsonl'
        );
        this.ensureLogDirectory();
    }
    
    private generateSessionId(): string {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    private ensureLogDirectory(): void {
        const dir = path.dirname(this.logFilePath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
    }
    
    async logGeneration(data: {
        projectPath: string;
        success: boolean;
        diagramsGenerated: number;
        generationTimeSeconds: number;
        qualityScore?: number;
        validationScores?: any;
        errorType?: string;
    }): Promise<void> {
        const devInfoManager = new DeveloperInfoManager(this.context);
        const hasConsent = await devInfoManager.hasConsent();
        
        if (!hasConsent) {
            // Only log locally without identifiable info
            this.logLocally('generation', data);
            return;
        }
        
        const devInfo = await devInfoManager.getDeveloperInfo();
        if (!devInfo) {return;}
        
        const projectMetadata = await this.analyzeProject(data.projectPath);
        const llmProvider = vscode.workspace.getConfiguration('architector').get<string>('llmProvider', 'ollama');
        
        const sessionData: SessionData = {
            sessionId: this.sessionId,
            participantId: devInfo.participantId,
            timestamp: new Date().toISOString(),
            extensionVersion: vscode.extensions.getExtension('architector.architector-llm')?.packageJSON.version || 'unknown',
            vscodeVersion: vscode.version,
            platform: process.platform,
            
            projectLanguage: projectMetadata.language,
            projectType: projectMetadata.type,
            projectSize: projectMetadata.size,
            fileCount: projectMetadata.fileCount,
            lineCount: projectMetadata.lineCount,
            
            diagramsGenerated: data.diagramsGenerated,
            diagramTypes: this.inferDiagramTypes(data.diagramsGenerated),
            generationTimeSeconds: data.generationTimeSeconds,
            success: data.success,
            errorType: data.errorType,
            
            qualityScore: data.qualityScore,
            validationScores: data.validationScores,
            
            llmProvider: llmProvider,
            modelName: this.getModelName(llmProvider),
            
            dependencyCheckRun: this.context.globalState.get('analytics.dependencyCheckRun', false),
            aboutPageViewed: this.context.globalState.get('analytics.aboutPageViewed', false),
            setupWizardCompleted: this.context.globalState.get('setupCompleted', false)
        };
        
        // Log locally
        await this.writeToLog(sessionData);
        
        // Send to backend
        await this.sendToBackend(sessionData);
    }
    
    private async analyzeProject(projectPath: string): Promise<ProjectMetadata> {
        try {
            // Detect primary language
            const files = await vscode.workspace.findFiles('**/*.{py,js,ts,java,cpp,go,rb,php}', '**/node_modules/**', 1000);
            
            const languageCounts: Record<string, number> = {};
            for (const file of files) {
                const ext = path.extname(file.fsPath).toLowerCase();
                const lang = this.extensionToLanguage(ext);
                languageCounts[lang] = (languageCounts[lang] || 0) + 1;
            }
            
            const primaryLanguage = Object.entries(languageCounts)
                .sort((a, b) => b[1] - a[1])[0]?.[0] || 'unknown';
            
            // Detect project type
            const projectType = await this.detectProjectType(projectPath);
            
            // Determine project size
            const fileCount = files.length;
            const size = fileCount < 50 ? 'small' : fileCount < 200 ? 'medium' : fileCount < 1000 ? 'large' : 'enterprise';
            
            return {
                language: primaryLanguage,
                type: projectType,
                size,
                fileCount
            };
        } catch (error) {
            return {
                language: 'unknown',
                type: 'unknown',
                size: 'small',
                fileCount: 0
            };
        }
    }
    
    private extensionToLanguage(ext: string): string {
        const map: Record<string, string> = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.rs': 'Rust'
        };
        return map[ext] || 'Other';
    }
    
    private async detectProjectType(projectPath: string): Promise<string> {
        // Check for common project indicators
        const indicators = [
            { file: 'package.json', type: 'Node.js' },
            { file: 'requirements.txt', type: 'Python' },
            { file: 'setup.py', type: 'Python' },
            { file: 'pyproject.toml', type: 'Python' },
            { file: 'pom.xml', type: 'Java/Maven' },
            { file: 'build.gradle', type: 'Java/Gradle' },
            { file: 'go.mod', type: 'Go' },
            { file: 'Cargo.toml', type: 'Rust' },
            { file: 'Gemfile', type: 'Ruby' },
            { file: 'composer.json', type: 'PHP' }
        ];
        
        for (const indicator of indicators) {
            const files = await vscode.workspace.findFiles(indicator.file, null, 1);
            if (files.length > 0) {
                return indicator.type;
            }
        }
        
        return 'Generic';
    }
    
    private inferDiagramTypes(count: number): string[] {
        // Standard types we generate
        const types = ['class', 'sequence', 'architecture', 'component', 'interaction'];
        return types.slice(0, count);
    }
    
    private getModelName(provider: string): string {
        const models: Record<string, string> = {
            'ollama': 'deepseek-coder:6.7b',
            'deepseek': 'deepseek-coder',
            'openai': 'gpt-4',
            'claude': 'claude-3-sonnet'
        };
        return models[provider] || 'unknown';
    }
    
    private async writeToLog(data: SessionData): Promise<void> {
        try {
            const line = JSON.stringify(data) + '\n';
            fs.appendFileSync(this.logFilePath, line, 'utf-8');
        } catch (error) {
            console.error('Failed to write analytics log:', error);
        }
    }
    
    private async sendToBackend(data: SessionData): Promise<void> {
        try {
            await fetch('https://architector-analytics.onrender.com/architector/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } catch (error) {
            // Silently fail - data is already logged locally
            console.error('Failed to send analytics:', error);
        }
    }
    
    private logLocally(event: string, data: any): void {
        const localLog = {
            event,
            timestamp: new Date().toISOString(),
            data
        };
        
        const localLogPath = path.join(
            this.context.globalStorageUri.fsPath,
            'analytics',
            'local.jsonl'
        );
        
        try {
            const line = JSON.stringify(localLog) + '\n';
            fs.appendFileSync(localLogPath, line, 'utf-8');
        } catch (error) {
            console.error('Failed to write local log:', error);
        }
    }
    
    async trackEvent(event: string, properties?: Record<string, any>): Promise<void> {
        const devInfoManager = new DeveloperInfoManager(this.context);
        const hasConsent = await devInfoManager.hasConsent();
        
        if (!hasConsent) {
            this.logLocally(event, properties);
            return;
        }
        
        // Update tracked events
        if (event === 'dependencyCheck') {
            await this.context.globalState.update('analytics.dependencyCheckRun', true);
        } else if (event === 'aboutPageView') {
            await this.context.globalState.update('analytics.aboutPageViewed', true);
        }
        
        this.logLocally(event, properties);
    }
    
    async exportAnalytics(): Promise<string> {
        // Export analytics for research paper
        if (!fs.existsSync(this.logFilePath)) {
            throw new Error('No analytics data found');
        }
        
        const data = fs.readFileSync(this.logFilePath, 'utf-8');
        const sessions = data.split('\n').filter(line => line.trim()).map(line => JSON.parse(line));
        
        // Generate summary statistics
        const summary = {
            totalSessions: sessions.length,
            uniqueParticipants: new Set(sessions.map(s => s.participantId)).size,
            successRate: sessions.filter(s => s.success).length / sessions.length,
            averageQualityScore: sessions.filter(s => s.qualityScore).reduce((sum, s) => sum + (s.qualityScore || 0), 0) / sessions.filter(s => s.qualityScore).length,
            averageGenerationTime: sessions.reduce((sum, s) => sum + s.generationTimeSeconds, 0) / sessions.length,
            languageDistribution: this.countBy(sessions, 'projectLanguage'),
            projectTypeDistribution: this.countBy(sessions, 'projectType'),
            sizeDistribution: this.countBy(sessions, 'projectSize'),
            providerDistribution: this.countBy(sessions, 'llmProvider')
        };
        
        const exportPath = path.join(
            this.context.globalStorageUri.fsPath,
            'analytics',
            `export_${Date.now()}.json`
        );
        
        fs.writeFileSync(exportPath, JSON.stringify({ summary, sessions }, null, 2));
        
        return exportPath;
    }
    
    private countBy(arr: any[], key: string): Record<string, number> {
        const counts: Record<string, number> = {};
        for (const item of arr) {
            const value = item[key] || 'unknown';
            counts[value] = (counts[value] || 0) + 1;
        }
        return counts;
    }
}
