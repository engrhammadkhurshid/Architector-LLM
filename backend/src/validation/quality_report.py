"""
Quality Report Generator
Generates comprehensive quality reports for diagram validation results.
"""

from typing import Dict, List, Any
from datetime import datetime


class QualityReportGenerator:
    """Generates quality reports from validation results."""
    
    def generate(
        self,
        validation_results: Dict[str, Any],
        diagram_results: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Generate comprehensive quality report in Markdown format.
        
        Args:
            validation_results: Results from DiagramValidator
            diagram_results: Original diagram generation results
            metadata: Optional generation metadata
            
        Returns:
            Markdown-formatted quality report
        """
        report = self._generate_header(metadata)
        report += self._generate_executive_summary(validation_results)
        report += self._generate_score_table(validation_results)
        report += self._generate_issues_section(validation_results)
        report += self._generate_recommendations(validation_results)
        report += self._generate_coverage_analysis(validation_results, diagram_results)
        report += self._generate_footer()
        
        return report
    
    def _generate_header(self, metadata: Dict) -> str:
        """Generate report header."""
        meta = metadata or {}
        timestamp = meta.get('generated_at', datetime.now().isoformat())
        version = meta.get('semantic_version', '1.0.0')
        
        return f"""# Architecture Documentation Quality Report

**Generated:** {timestamp}  
**Version:** {version}  
**Report Type:** Diagram Quality Assessment

---

"""
    
    def _generate_executive_summary(self, validation_results: Dict) -> str:
        """Generate executive summary."""
        total = len(validation_results)
        validated = sum(1 for v in validation_results.values() if v.get('validated'))
        
        # Calculate average scores
        all_scores = [v.get('overall_score', 0) for v in validation_results.values() if v.get('validated')]
        avg_overall = sum(all_scores) / len(all_scores) if all_scores else 0
        
        # Score dimensions
        syntax_scores = [v['scores'].get('syntax', 0) for v in validation_results.values() if v.get('validated')]
        completeness_scores = [v['scores'].get('completeness', 0) for v in validation_results.values() if v.get('validated')]
        clarity_scores = [v['scores'].get('clarity', 0) for v in validation_results.values() if v.get('validated')]
        accuracy_scores = [v['scores'].get('accuracy', 0) for v in validation_results.values() if v.get('validated')]
        
        avg_syntax = sum(syntax_scores) / len(syntax_scores) if syntax_scores else 0
        avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0
        avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0
        avg_accuracy = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0
        
        # Quality rating
        quality_rating = self._get_quality_rating(avg_overall)
        rating_emoji = self._get_rating_emoji(avg_overall)
        
        return f"""## Executive Summary

{rating_emoji} **Overall Quality Rating:** {quality_rating} ({avg_overall:.1f}/100)

### Key Metrics

- **Total Diagrams:** {total}
- **Successfully Validated:** {validated}
- **Average Overall Score:** {avg_overall:.1f}/100

### Score Breakdown

| Dimension | Average Score | Status |
|-----------|--------------|--------|
| **Syntax** | {avg_syntax:.1f}/100 | {self._get_status_emoji(avg_syntax)} {self._get_score_status(avg_syntax)} |
| **Completeness** | {avg_completeness:.1f}/100 | {self._get_status_emoji(avg_completeness)} {self._get_score_status(avg_completeness)} |
| **Clarity** | {avg_clarity:.1f}/100 | {self._get_status_emoji(avg_clarity)} {self._get_score_status(avg_clarity)} |
| **Accuracy** | {avg_accuracy:.1f}/100 | {self._get_status_emoji(avg_accuracy)} {self._get_score_status(avg_accuracy)} |

---

"""
    
    def _generate_score_table(self, validation_results: Dict) -> str:
        """Generate detailed score table."""
        section = "## Detailed Diagram Scores\n\n"
        section += "| Diagram Type | Overall | Syntax | Completeness | Clarity | Accuracy | Status |\n"
        section += "|--------------|---------|--------|--------------|---------|----------|---------|\n"
        
        # Sort by overall score descending
        sorted_results = sorted(
            validation_results.items(),
            key=lambda x: x[1].get('overall_score', 0),
            reverse=True
        )
        
        for diagram_type, result in sorted_results:
            if not result.get('validated'):
                continue
            
            overall = result.get('overall_score', 0)
            scores = result.get('scores', {})
            
            syntax = scores.get('syntax', 0)
            completeness = scores.get('completeness', 0)
            clarity = scores.get('clarity', 0)
            accuracy = scores.get('accuracy', 0)
            
            status = self._get_status_emoji(overall)
            diagram_name = diagram_type.replace('_', ' ').title()
            
            section += f"| {diagram_name} | {overall:.1f} | {syntax:.1f} | {completeness:.1f} | {clarity:.1f} | {accuracy:.1f} | {status} |\n"
        
        section += "\n---\n\n"
        return section
    
    def _generate_issues_section(self, validation_results: Dict) -> str:
        """Generate issues section grouped by severity."""
        section = "## Issues Found\n\n"
        
        # Collect all issues
        critical_issues = []
        warnings = []
        info = []
        
        for diagram_type, result in validation_results.items():
            if not result.get('validated'):
                continue
            
            issues = result.get('issues', [])
            overall_score = result.get('overall_score', 100)
            diagram_name = diagram_type.replace('_', ' ').title()
            
            for issue in issues:
                if overall_score < 60:
                    critical_issues.append((diagram_name, issue))
                elif overall_score < 80:
                    warnings.append((diagram_name, issue))
                else:
                    info.append((diagram_name, issue))
        
        # Critical issues
        if critical_issues:
            section += "### 🔴 Critical Issues (Score < 60)\n\n"
            for diagram, issue in critical_issues:
                section += f"- **{diagram}:** {issue}\n"
            section += "\n"
        
        # Warnings
        if warnings:
            section += "### 🟡 Warnings (Score 60-79)\n\n"
            for diagram, issue in warnings:
                section += f"- **{diagram}:** {issue}\n"
            section += "\n"
        
        # Info
        if info:
            section += "### 🟢 Minor Issues (Score 80+)\n\n"
            for diagram, issue in info:
                section += f"- **{diagram}:** {issue}\n"
            section += "\n"
        
        if not critical_issues and not warnings and not info:
            section += "*No issues found. All diagrams meet quality standards.*\n\n"
        
        section += "---\n\n"
        return section
    
    def _generate_recommendations(self, validation_results: Dict) -> str:
        """Generate actionable recommendations."""
        section = "## Recommendations\n\n"
        
        # Group recommendations by diagram
        has_recommendations = False
        
        for diagram_type, result in validation_results.items():
            if not result.get('validated'):
                continue
            
            recommendations = result.get('recommendations', [])
            if recommendations:
                has_recommendations = True
                diagram_name = diagram_type.replace('_', ' ').title()
                section += f"### {diagram_name}\n\n"
                for rec in recommendations:
                    section += f"- {rec}\n"
                section += "\n"
        
        if not has_recommendations:
            section += "*No specific recommendations. Diagrams are well-formed.*\n\n"
        
        section += "---\n\n"
        return section
    
    def _generate_coverage_analysis(self, validation_results: Dict, diagram_results: Dict) -> str:
        """Generate coverage analysis."""
        section = "## Coverage Analysis\n\n"
        
        # Analyze what aspects are well-covered vs missing
        categories = {}
        for diagram_type, result in diagram_results.items():
            if result.get('success'):
                category = result.get('metadata', {}).get('category', 'Other')
                categories[category] = categories.get(category, 0) + 1
        
        section += "### Diagram Coverage by Category\n\n"
        section += "| Category | Diagram Count | Coverage |\n"
        section += "|----------|--------------|----------|\n"
        
        total_diagrams = sum(categories.values())
        for category, count in sorted(categories.items()):
            percentage = (count / total_diagrams * 100) if total_diagrams > 0 else 0
            section += f"| {category} | {count} | {percentage:.1f}% |\n"
        
        section += "\n"
        
        # Quality by category
        section += "### Quality by Category\n\n"
        category_scores = {}
        for diagram_type, val_result in validation_results.items():
            if not val_result.get('validated'):
                continue
            
            diagram_result = diagram_results.get(diagram_type, {})
            category = diagram_result.get('metadata', {}).get('category', 'Other')
            
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(val_result.get('overall_score', 0))
        
        for category, scores in sorted(category_scores.items()):
            avg = sum(scores) / len(scores)
            status = self._get_status_emoji(avg)
            section += f"- **{category}:** {avg:.1f}/100 {status}\n"
        
        section += "\n---\n\n"
        return section
    
    def _generate_footer(self) -> str:
        """Generate report footer."""
        return """## How to Improve Scores

### Syntax (Target: 95+)
- Ensure proper Mermaid diagram type declaration
- Check for balanced brackets/parentheses
- Validate diagram-specific syntax requirements

### Completeness (Target: 85+)
- Include all required elements for diagram type
- Add attributes, methods, or properties where applicable
- Show relationships and connections between entities

### Clarity (Target: 80+)
- Keep diagrams focused (5-20 nodes optimal)
- Avoid over-complexity
- Use clear, descriptive labels

### Accuracy (Target: 80+)
- Ensure diagram matches actual codebase
- Include all major components/classes
- Verify relationships reflect real dependencies

---

*Generated by Architector-LLM Quality Validation System*
"""
    
    def _get_quality_rating(self, score: float) -> str:
        """Get quality rating from score."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Fair"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _get_rating_emoji(self, score: float) -> str:
        """Get emoji for rating."""
        if score >= 90:
            return "🟢"
        elif score >= 80:
            return "🟡"
        elif score >= 70:
            return "🟠"
        else:
            return "🔴"
    
    def _get_status_emoji(self, score: float) -> str:
        """Get status emoji for score."""
        if score >= 85:
            return "✅"
        elif score >= 70:
            return "⚠️"
        else:
            return "❌"
    
    def _get_score_status(self, score: float) -> str:
        """Get status text for score."""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Needs Work"
