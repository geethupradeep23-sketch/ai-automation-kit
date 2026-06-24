import os
import json
from dotenv import load_dotenv
import openai
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

class CaptionGenerator:
    """Generate AI-powered social media captions"""
    
    def __init__(self, brand_voice='professional'):
        self.brand_voice = brand_voice
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load caption templates"""
        return {
            'product_launch': 'Introduce a new product with excitement and key benefits',
            'behind_the_scenes': 'Share behind-the-scenes content showing company culture',
            'educational': 'Educational content that provides value to audience',
            'announcement': 'Important company announcements',
            'engagement': 'Engagement-focused content asking questions or calls-to-action'
        }
    
    def generate_caption(self, topic, platform='instagram', tone='friendly', length='medium'):
        """
        Generate a caption for a specific topic
        
        Args:
            topic: Topic or description for the caption
            platform: Target platform (instagram, twitter, linkedin, facebook)
            tone: Tone of voice (friendly, professional, humorous, inspirational)
            length: Caption length (short, medium, long)
        
        Returns:
            Generated caption with hashtags
        """
        length_guide = {
            'short': '50-80 characters',
            'medium': '100-150 characters',
            'long': '200-300 characters'
        }
        
        platform_specs = {
            'instagram': 'Include 10-15 relevant hashtags',
            'twitter': 'Keep under 280 characters, include 2-3 hashtags',
            'linkedin': 'Professional tone, include industry hashtags',
            'facebook': 'Longer format, include call-to-action'
        }
        
        prompt = f"""
        Generate a social media caption for {platform} about: {topic}
        
        Brand voice: {self.brand_voice}
        Tone: {tone}
        Length: {length_guide.get(length, 'medium')}
        Platform requirements: {platform_specs.get(platform, '')}
        
        Include relevant emojis and hashtags.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            caption = response.choices[0].message['content']
            logger.info(f"Generated caption for {platform}")
            return caption
        
        except Exception as e:
            logger.error(f"Caption generation failed: {str(e)}")
            return None
    
    def generate_hashtags(self, topic, platform='instagram', count=15):
        """
        Generate relevant hashtags
        
        Args:
            topic: Topic for hashtag generation
            platform: Target platform
            count: Number of hashtags to generate
        
        Returns:
            List of hashtags
        """
        prompt = f"""
        Generate {count} relevant, high-performing hashtags for {platform} about: {topic}
        
        Return as comma-separated list starting with #
        Focus on mix of: popular hashtags, niche hashtags, trending hashtags
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )
            
            hashtags = response.choices[0].message['content']
            logger.info(f"Generated {count} hashtags")
            return hashtags
        
        except Exception as e:
            logger.error(f"Hashtag generation failed: {str(e)}")
            return ""
    
    def generate_alt_text(self, image_description):
        """
        Generate descriptive alt text for images
        
        Args:
            image_description: Description of the image
        
        Returns:
            SEO-optimized alt text
        """
        prompt = f"""
        Generate concise, descriptive alt text (50-125 characters) for accessibility:
        {image_description}
        
        Alt text should:
        - Be descriptive but concise
        - Include relevant keywords
        - Be SEO-friendly
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=150
            )
            
            alt_text = response.choices[0].message['content']
            logger.info("Generated alt text")
            return alt_text
        
        except Exception as e:
            logger.error(f"Alt text generation failed: {str(e)}")
            return image_description


if __name__ == "__main__":
    generator = CaptionGenerator(brand_voice='professional')
    
    # Example: Generate caption
    caption = generator.generate_caption(
        'New AI automation features launched',
        platform='instagram',
        tone='excited',
        length='medium'
    )
    print("Generated Caption:")
    print(caption)
    print()
    
    # Example: Generate hashtags
    hashtags = generator.generate_hashtags('AI automation', 'instagram', 15)
    print("Generated Hashtags:")
    print(hashtags)
