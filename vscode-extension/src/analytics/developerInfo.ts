/**
 * Developer Information Manager
 * Collects optional developer information for research purposes
 */

import * as vscode from 'vscode';

export interface DeveloperInfo {
    fullName: string;
    email: string;
    designation: string;
    experienceLevel: 'junior' | 'mid' | 'senior' | 'principal' | 'lead' | 'architect' | 'other';
    organization?: string;
    country?: string;
    consentTimestamp: string;
    consentVersion: string;
    participantId: string; // Anonymous UUID
}

export class DeveloperInfoManager {
    constructor(private context: vscode.ExtensionContext) {}
    
    async hasConsent(): Promise<boolean> {
        const consent = this.context.globalState.get<boolean>('research.hasConsent', false);
        return consent;
    }
    
    async getDeveloperInfo(): Promise<DeveloperInfo | undefined> {
        return this.context.globalState.get<DeveloperInfo>('research.developerInfo');
    }
    
    async showConsentDialog(): Promise<boolean> {
        const consent = await vscode.window.showInformationMessage(
            '📊 Research Study Consent\n\n' +
            '**Study:** "From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"\n' +
            '**Researcher:** Engr. Hammad Khurshid, NUST Pakistan\n\n' +
            '**Your participation helps improve this tool and contributes to academic research.**\n\n' +
            '✅ What we collect:\n' +
            '• Your professional information (name, email, role)\n' +
            '• Usage statistics (generation time, success rate)\n' +
            '• Project metadata (language, size, type)\n' +
            '• Performance metrics (quality scores, diagram counts)\n\n' +
            '❌ What we DON\'T collect:\n' +
            '• Your source code or file contents\n' +
            '• Proprietary project details\n' +
            '• Passwords or API keys\n\n' +
            '**Your data will be:**\n' +
            '• Used for academic research only\n' +
            '• Stored securely and encrypted\n' +
            '• Retained for research period (2 years)\n' +
            '• Included in anonymized form in research paper\n\n' +
            '**You can:**\n' +
            '• Withdraw consent anytime\n' +
            '• Request data deletion\n' +
            '• Contact researcher: engr.hammadkhurshid@gmail.com',
            { modal: true },
            'View Privacy Policy',
            'I Consent',
            'Decline'
        );
        
        if (consent === 'View Privacy Policy') {
            await vscode.commands.executeCommand('architector-llm.showPrivacyPolicy');
            // Ask again after viewing policy
            return await this.showConsentDialog();
        }
        
        if (consent === 'I Consent') {
            await this.collectDeveloperInfo();
            return true;
        }
        
        await this.context.globalState.update('research.hasConsent', false);
        await this.context.globalState.update('research.declinedAt', new Date().toISOString());
        return false;
    }
    
    private async collectDeveloperInfo(): Promise<void> {
        // Generate anonymous participant ID
        const participantId = this.generateParticipantId();
        
        // Collect information step by step
        const fullName = await vscode.window.showInputBox({
            prompt: 'Your full name',
            placeHolder: 'e.g., John Doe',
            ignoreFocusOut: true,
            validateInput: (value) => value.trim() ? null : 'Name is required'
        });
        if (!fullName) return;
        
        const email = await vscode.window.showInputBox({
            prompt: 'Your email address',
            placeHolder: 'e.g., john.doe@example.com',
            ignoreFocusOut: true,
            validateInput: (value) => {
                if (!value) return 'Email is required';
                if (!value.includes('@')) return 'Please enter a valid email';
                return null;
            }
        });
        if (!email) return;
        
        const designation = await vscode.window.showInputBox({
            prompt: 'Your job title/designation',
            placeHolder: 'e.g., Software Engineer, Developer, Student',
            ignoreFocusOut: true,
            validateInput: (value) => value.trim() ? null : 'Designation is required'
        });
        if (!designation) return;
        
        const experienceLevel = await vscode.window.showQuickPick([
            { label: 'Junior Developer', detail: '0-2 years experience', value: 'junior' },
            { label: 'Mid-Level Developer', detail: '2-5 years experience', value: 'mid' },
            { label: 'Senior Developer', detail: '5-8 years experience', value: 'senior' },
            { label: 'Principal Engineer', detail: '8+ years experience', value: 'principal' },
            { label: 'Tech Lead / Manager', detail: 'Leadership role', value: 'lead' },
            { label: 'Architect', detail: 'Architecture role', value: 'architect' },
            { label: 'Student', detail: 'Currently studying', value: 'other' },
            { label: 'Other', detail: 'Other role', value: 'other' }
        ], {
            placeHolder: 'Select your experience level',
            ignoreFocusOut: true
        });
        if (!experienceLevel) return;
        
        const organization = await vscode.window.showInputBox({
            prompt: 'Organization/Company (optional)',
            placeHolder: 'e.g., NUST, Google, Independent',
            ignoreFocusOut: true
        });
        
        const country = await vscode.window.showInputBox({
            prompt: 'Country (optional)',
            placeHolder: 'e.g., Pakistan, USA, India',
            ignoreFocusOut: true
        });
        
        // Store developer information
        const developerInfo: DeveloperInfo = {
            fullName,
            email,
            designation,
            experienceLevel: experienceLevel.value as any,
            organization: organization || undefined,
            country: country || undefined,
            consentTimestamp: new Date().toISOString(),
            consentVersion: '1.0',
            participantId
        };
        
        await this.context.globalState.update('research.developerInfo', developerInfo);
        await this.context.globalState.update('research.hasConsent', true);
        
        // Send initial registration to backend
        await this.registerParticipant(developerInfo);
        
        vscode.window.showInformationMessage(
            '✅ Thank you for participating in our research! Your contribution is valuable.',
            'Great!'
        );
    }
    
    private generateParticipantId(): string {
        // Generate UUID v4
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    
    private async registerParticipant(info: DeveloperInfo): Promise<void> {
        try {
            // Send to research backend
            await fetch('https://architector-analytics.onrender.com/architector/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    participantId: info.participantId,
                    fullName: info.fullName,
                    email: info.email,
                    designation: info.designation,
                    experienceLevel: info.experienceLevel,
                    organization: info.organization,
                    country: info.country,
                    consentTimestamp: info.consentTimestamp,
                    consentVersion: info.consentVersion,
                    extensionVersion: vscode.extensions.getExtension('architector.architector-llm')?.packageJSON.version
                })
            });
        } catch (error) {
            // Silently fail - don't block user if backend is down
            console.error('Failed to register participant:', error);
        }
    }
    
    async revokeConsent(): Promise<void> {
        const confirm = await vscode.window.showWarningMessage(
            'Are you sure you want to withdraw from the research study? Your data will be deleted.',
            { modal: true },
            'Yes, Withdraw',
            'Cancel'
        );
        
        if (confirm === 'Yes, Withdraw') {
            const devInfo = await this.getDeveloperInfo();
            if (devInfo) {
                // Send deletion request to backend
                try {
                    await fetch('https://architector-analytics.onrender.com/architector/delete', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ participantId: devInfo.participantId })
                    });
                } catch (error) {
                    console.error('Failed to delete participant data:', error);
                }
            }
            
            await this.context.globalState.update('research.hasConsent', false);
            await this.context.globalState.update('research.developerInfo', undefined);
            
            vscode.window.showInformationMessage('Your consent has been withdrawn and data deleted.');
        }
    }
    
    async updateDeveloperInfo(): Promise<void> {
        const hasConsent = await this.hasConsent();
        if (!hasConsent) {
            vscode.window.showInformationMessage('You are not currently participating in the research study.');
            return;
        }
        
        await this.collectDeveloperInfo();
        vscode.window.showInformationMessage('Your information has been updated.');
    }
}
