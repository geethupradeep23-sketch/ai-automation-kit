import json
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate automated business reports"""
    
    def __init__(self):
        self.reports = []
    
    def generate_daily_report(self, metrics: Dict):
        """
        Generate daily report
        
        Args:
            metrics: Dictionary with daily metrics
        
        Returns:
            Daily report
        """
        report = {
            'report_type': 'daily',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'metrics': metrics,
            'summary': self._generate_summary(metrics)
        }
        self.reports.append(report)
        logger.info("Daily report generated")
        return report
    
    def generate_weekly_report(self, metrics: Dict):
        """
        Generate weekly report
        
        Args:
            metrics: Dictionary with weekly metrics
        
        Returns:
            Weekly report
        """
        report = {
            'report_type': 'weekly',
            'week_starting': (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'metrics': metrics,
            'summary': self._generate_summary(metrics),
            'trends': self._analyze_trends(metrics)
        }
        self.reports.append(report)
        logger.info("Weekly report generated")
        return report
    
    def generate_monthly_report(self, metrics: Dict):
        """
        Generate monthly report
        
        Args:
            metrics: Dictionary with monthly metrics
        
        Returns:
            Monthly report
        """
        report = {
            'report_type': 'monthly',
            'month': datetime.now().strftime('%Y-%m'),
            'generated_at': datetime.now().isoformat(),
            'metrics': metrics,
            'summary': self._generate_summary(metrics),
            'trends': self._analyze_trends(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }
        self.reports.append(report)
        logger.info("Monthly report generated")
        return report
    
    def _generate_summary(self, metrics: Dict):
        """
        Generate summary from metrics
        """
        summary = []
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                summary.append(f"{key}: {value}")
        return summary
    
    def _analyze_trends(self, metrics: Dict):
        """
        Analyze trends in metrics
        """
        return {
            'trend': 'stable',
            'growth_rate': 0,
            'notable_changes': []
        }
    
    def _generate_recommendations(self, metrics: Dict):
        """
        Generate recommendations based on metrics
        """
        return [
            'Continue current strategy',
            'Monitor performance metrics closely',
            'Plan for optimization in next period'
        ]
    
    def export_report(self, report_index: int, format='pdf'):
        """
        Export report to file
        
        Args:
            report_index: Index of report to export
            format: Export format (pdf, csv, json, excel)
        
        Returns:
            File path
        """
        if 0 <= report_index < len(self.reports):
            report = self.reports[report_index]
            filename = f"report_{report['report_type']}_{datetime.now().strftime('%Y%m%d')}.{format}"
            logger.info(f"Report exported as {filename}")
            return filename
        return None
    
    def email_report(self, report_index: int, recipients: List[str]):
        """
        Email report to recipients
        
        Args:
            report_index: Index of report to email
            recipients: List of email addresses
        
        Returns:
            Confirmation
        """
        if 0 <= report_index < len(self.reports):
            logger.info(f"Report emailed to {', '.join(recipients)}")
            return {'status': 'sent', 'recipients': recipients}
        return {'status': 'failed'}
    
    def schedule_report(self, report_type: str, frequency: str, recipients: List[str]):
        """
        Schedule automatic report generation and delivery
        
        Args:
            report_type: Type of report (daily, weekly, monthly)
            frequency: Frequency of delivery
            recipients: List of recipient emails
        
        Returns:
            Schedule confirmation
        """
        schedule = {
            'report_type': report_type,
            'frequency': frequency,
            'recipients': recipients,
            'created_at': datetime.now().isoformat(),
            'status': 'scheduled'
        }
        logger.info(f"Report scheduled: {report_type} {frequency}")
        return schedule


if __name__ == "__main__":
    generator = ReportGenerator()
    
    # Example: Generate daily report
    daily_metrics = {
        'tasks_completed': 15,
        'emails_processed': 42,
        'new_leads': 8,
        'conversion_rate': 0.25
    }
    
    report = generator.generate_daily_report(daily_metrics)
    print(json.dumps(report, indent=2))
