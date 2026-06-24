import json
import csv
from datetime import datetime
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentBuilder:
    """Build bulk content from templates and data sources"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.generated_content = []
    
    def _load_templates(self):
        """Load content templates"""
        return {
            'blog_to_social': {
                'instagram': 'Check out our latest blog: {title}\n\n{excerpt}\n\nLink in bio 🔗\n\n{hashtags}',
                'twitter': '{title}\n\n{excerpt}\n\n{link}\n\n{hashtags}',
                'linkedin': '{title}\n\n{excerpt}\n\n{link}\n\n{hashtags}'
            },
            'product_launch': {
                'instagram': '🎉 Introducing {product_name}!\n\n{description}\n\n{call_to_action}\n\n{hashtags}',
                'twitter': '🎉 {product_name} is here! {description} {link} {hashtags}',
                'linkedin': 'Excited to announce {product_name}! {description}\n\n{call_to_action}\n\n{hashtags}'
            }
        }
    
    def generate_from_template(self, template_name: str, platform: str, data: Dict):
        """
        Generate content from template
        
        Args:
            template_name: Name of template
            platform: Target platform
            data: Dictionary with template variables
        
        Returns:
            Generated content
        """
        try:
            template = self.templates[template_name][platform]
            content = template.format(**data)
            
            logger.info(f"Generated content from {template_name} for {platform}")
            self.generated_content.append({
                'platform': platform,
                'template': template_name,
                'content': content,
                'generated_at': datetime.now().isoformat()
            })
            return content
        
        except KeyError as e:
            logger.error(f"Template not found: {str(e)}")
            return None
    
    def batch_generate(self, template_name: str, platforms: List[str], data_list: List[Dict]):
        """
        Generate content in bulk
        
        Args:
            template_name: Template to use
            platforms: List of platforms
            data_list: List of data dictionaries
        
        Returns:
            List of generated content
        """
        results = []
        for data in data_list:
            for platform in platforms:
                content = self.generate_from_template(template_name, platform, data)
                if content:
                    results.append({
                        'platform': platform,
                        'content': content
                    })
        
        logger.info(f"Batch generated {len(results)} pieces of content")
        return results
    
    def load_csv_data(self, csv_file_path: str) -> List[Dict]:
        """
        Load data from CSV file
        
        Args:
            csv_file_path: Path to CSV file
        
        Returns:
            List of dictionaries
        """
        data = []
        try:
            with open(csv_file_path, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            logger.info(f"Loaded {len(data)} rows from {csv_file_path}")
            return data
        
        except Exception as e:
            logger.error(f"CSV loading failed: {str(e)}")
            return []
    
    def export_content(self, format='csv', filename='generated_content'):
        """
        Export generated content
        
        Args:
            format: Export format (csv, json)
            filename: Output filename
        
        Returns:
            File path
        """
        filepath = f"{filename}.{format}"
        
        try:
            if format == 'csv':
                with open(filepath, 'w', newline='') as f:
                    if self.generated_content:
                        writer = csv.DictWriter(f, fieldnames=self.generated_content[0].keys())
                        writer.writeheader()
                        writer.writerows(self.generated_content)
            
            elif format == 'json':
                with open(filepath, 'w') as f:
                    json.dump(self.generated_content, f, indent=2)
            
            logger.info(f"Exported {len(self.generated_content)} items to {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return None


if __name__ == "__main__":
    builder = ContentBuilder()
    
    # Example: Generate from template
    data = {
        'title': 'How to Automate Your Social Media',
        'excerpt': 'Learn best practices for social media automation...',
        'link': 'https://example.com/blog',
        'hashtags': '#socialmedia #automation #AI'
    }
    
    content = builder.generate_from_template('blog_to_social', 'instagram', data)
    print("Generated Content:")
    print(content)
