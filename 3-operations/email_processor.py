import re
import json
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailProcessor:
    """Automate email processing and management"""
    
    def __init__(self):
        self.processed_emails = []
        self.auto_responses = {}
    
    def classify_email(self, email_content: str, subject: str):
        """
        Classify incoming emails
        
        Args:
            email_content: Email body
            subject: Email subject
        
        Returns:
            Classification category
        """
        keywords = {
            'support': ['help', 'issue', 'problem', 'broken', 'error'],
            'sales': ['demo', 'pricing', 'quote', 'purchase', 'buy'],
            'partnership': ['partner', 'collaboration', 'integrate', 'api'],
            'feedback': ['feedback', 'suggestion', 'improvement', 'feature'],
            'newsletter': ['unsubscribe', 'newsletter', 'promotion'],
        }
        
        combined_text = (subject + ' ' + email_content).lower()
        
        scores = {}
        for category, keywords_list in keywords.items():
            scores[category] = sum(1 for kw in keywords_list if kw in combined_text)
        
        category = max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'
        logger.info(f"Email classified as: {category}")
        return category
    
    def extract_data(self, email_content: str):
        """
        Extract structured data from email
        
        Args:
            email_content: Email body
        
        Returns:
            Extracted data dictionary
        """
        data = {
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_content),
            'phone_numbers': re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', email_content),
            'urls': re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content),
            'extracted_at': datetime.now().isoformat()
        }
        logger.info(f"Extracted data: {len(data['emails'])} emails, {len(data['phone_numbers'])} phones")
        return data
    
    def generate_auto_response(self, category: str, sender_email: str):
        """
        Generate automatic response email
        
        Args:
            category: Email category
            sender_email: Recipient email
        
        Returns:
            Auto response email
        """
        templates = {
            'support': f"Thank you for contacting support. We'll get back to you within 24 hours.",
            'sales': f"Thank you for your interest! A sales representative will reach out shortly.",
            'partnership': f"We appreciate your partnership interest. Let's schedule a call to discuss.",
            'feedback': f"Thank you for your feedback! We appreciate your input.",
            'general': f"Thank you for reaching out. We'll respond shortly."
        }
        
        response = {
            'to': sender_email,
            'subject': f'Re: Your inquiry - Auto Response',
            'body': templates.get(category, templates['general']),
            'generated_at': datetime.now().isoformat(),
            'is_auto_response': True
        }
        logger.info(f"Auto response generated for {category}")
        return response
    
    def process_inbox(self, emails: List[Dict]):
        """
        Process multiple emails
        
        Args:
            emails: List of email dictionaries
        
        Returns:
            Processing results
        """
        results = []
        for email in emails:
            category = self.classify_email(email.get('body', ''), email.get('subject', ''))
            extracted_data = self.extract_data(email.get('body', ''))
            
            result = {
                'from': email.get('from'),
                'subject': email.get('subject'),
                'category': category,
                'extracted_data': extracted_data,
                'processed_at': datetime.now().isoformat()
            }
            results.append(result)
            self.processed_emails.append(result)
        
        logger.info(f"Processed {len(emails)} emails")
        return results
    
    def set_auto_response(self, category: str, template: str):
        """
        Set custom auto-response for email category
        
        Args:
            category: Email category
            template: Auto-response template
        """
        self.auto_responses[category] = template
        logger.info(f"Auto-response set for {category}")
    
    def get_statistics(self):
        """
        Get email processing statistics
        
        Returns:
            Statistics dictionary
        """
        stats = {
            'total_processed': len(self.processed_emails),
            'by_category': {},
            'processed_at': datetime.now().isoformat()
        }
        
        for email in self.processed_emails:
            cat = email['category']
            stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
        
        logger.info(f"Statistics: {stats['total_processed']} emails processed")
        return stats


if __name__ == "__main__":
    processor = EmailProcessor()
    
    # Example: Process emails
    sample_emails = [
        {
            'from': 'customer@example.com',
            'subject': 'Need help with my account',
            'body': 'I am having issues logging into my account. Please help!'
        },
        {
            'from': 'inquiry@company.com',
            'subject': 'Interested in partnership',
            'body': 'We would like to discuss integration possibilities. Contact: 555-123-4567'
        }
    ]
    
    results = processor.process_inbox(sample_emails)
    print(json.dumps(results, indent=2))
