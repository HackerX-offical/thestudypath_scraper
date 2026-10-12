import requests
import re
import os
from bs4 import BeautifulSoup
from PIL import Image
import io
from urllib.parse import urljoin
import concurrent.futures

class StudyPathScraper:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36'
        }
        
        self.image_headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.thestudypath.com/',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36'
        }
        
        self.base_url = "https://www.thestudypath.com"
        
    def get_exercise_pages(self):
        """Get all exercise page URLs"""
        main_page = "https://www.thestudypath.com/class-9/rs-aggarwal-solutions/chapter-15-volume-and-surface-area-of-solids/"
        
        try:
            response = requests.get(main_page, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            exercise_pages = {}
            
            # Find all exercise links
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                
                # Match exercise patterns
                if 'exercise-15a' in href.lower() or 'exercise-15A' in href:
                    exercise_pages['Exercise_15A'] = href
                elif 'exercise-15b' in href.lower() or 'exercise-15B' in href:
                    exercise_pages['Exercise_15B'] = href
                elif 'exercise-15c' in href.lower() or 'exercise-15C' in href:
                    exercise_pages['Exercise_15C'] = href
                elif 'exercise-15d' in href.lower() or 'exercise-15D' in href:
                    exercise_pages['Exercise_15D'] = href
                elif 'multiple-choice' in href.lower() or 'mcq' in href.lower():
                    exercise_pages['MCQs'] = href
            
            # Ensure URLs are absolute
            for name, url in exercise_pages.items():
                if not url.startswith('http'):
                    exercise_pages[name] = urljoin(self.base_url, url)
            
            return exercise_pages
            
        except Exception as e:
            print(f"Error getting exercise pages: {e}")
            return {}

    def extract_image_urls(self, page_url):
        """Extract all image URLs from an exercise page"""
        try:
            response = requests.get(page_url, headers=self.headers)
            response.raise_for_status()
            
            # Update referer for image requests
            self.image_headers['referer'] = page_url
            
            soup = BeautifulSoup(response.content, 'html.parser')
            image_urls = []
            
            # Pattern 1: Direct img tags with the specific pattern
            img_tags = soup.find_all('img', src=True)
            
            for img in img_tags:
                src = img['src']
                
                # Look for the specific pattern from your curl example
                if 'RS-Aggarwal-Solutions-Class-9-Chapter-15' in src:
                    if not src.startswith('http'):
                        src = urljoin(self.base_url, src)
                    image_urls.append(src)
            
            # Pattern 2: Look for images in content
            content_div = soup.find('div', class_=re.compile(r'entry-content|post-content|content', re.I))
            if content_div:
                for img in content_div.find_all('img', src=True):
                    src = img['src']
                    if not src.startswith('http'):
                        src = urljoin(self.base_url, src)
                    if src not in image_urls:
                        image_urls.append(src)
            
            # Sort URLs to ensure correct order
            image_urls.sort()
            
            print(f"Found {len(image_urls)} images on {page_url}")
            return image_urls
            
        except Exception as e:
            print(f"Error extracting images from {page_url}: {e}")
            return []

    def download_image(self, url, idx, exercise_name):
        """Download a single image"""
        try:
            response = requests.get(url, headers=self.image_headers, stream=True)
            response.raise_for_status()
            
            # Extract filename from URL or create one
            filename = url.split('/')[-1]
            if not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filename = f"{exercise_name}_page_{idx:03d}.jpg"
            
            return {
                'index': idx,
                'filename': filename,
                'content': response.content,
                'size': len(response.content)
            }
            
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return None

    def download_all_images(self, exercise_name, page_url):
        """Download all images for an exercise"""
        print(f"\n{'='*60}")
        print(f"Processing: {exercise_name}")
        print(f"URL: {page_url}")
        
        # Get image URLs
        image_urls = self.extract_image_urls(page_url)
        
        if not image_urls:
            print(f"No images found for {exercise_name}")
            return []
        
        print(f"Downloading {len(image_urls)} images...")
        
        # Download images concurrently
        downloaded_images = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for idx, url in enumerate(image_urls, 1):
                futures.append(
                    executor.submit(self.download_image, url, idx, exercise_name)
                )
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    downloaded_images.append(result)
                    print(f"  Downloaded: {result['filename']} ({result['size']/1024:.1f} KB)")
        
        # Sort by index
        downloaded_images.sort(key=lambda x: x['index'])
        
        return downloaded_images

    def save_as_pdf(self, images_data, output_path):
        """Convert images to PDF"""
        try:
            image_objects = []
            
            for img_data in images_data:
                img = Image.open(io.BytesIO(img_data['content']))
                
                # Convert to RGB if necessary (for PDF)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                image_objects.append(img)
            
            if image_objects:
                # Save first image
                image_objects[0].save(
                    output_path,
                    "PDF",
                    resolution=100.0,
                    save_all=True,
                    append_images=image_objects[1:]
                )
                
                print(f" PDF saved: {output_path}")
                return True
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
        
        return False

    def scrape_all_exercises(self):
        """Main function to scrape all exercises"""
        print("Starting Study Path Scraper...")
        print("This script will download all exercises as PDFs")
        print("="*60)
        
        # Create directories
        base_dir = "study_path_chapter_15"
        images_dir = os.path.join(base_dir, "images")
        pdfs_dir = os.path.join(base_dir, "pdfs")
        
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(pdfs_dir, exist_ok=True)
        
        # Get exercise pages
        exercise_pages = self.get_exercise_pages()
        
        if not exercise_pages:
            print("No exercise pages found!")
            return
        
        print(f"Found {len(exercise_pages)} exercise pages")
        
        # Process each exercise
        for exercise_name, page_url in exercise_pages.items():
            print(f"\n{'='*60}")
            print(f"PROCESSING: {exercise_name}")
            
            # Download all images
            images_data = self.download_all_images(exercise_name, page_url)
            
            if not images_data:
                continue
            
            # Save individual images
            print(f"\nSaving individual images...")
            for img_data in images_data:
                img_path = os.path.join(images_dir, img_data['filename'])
                with open(img_path, 'wb') as f:
                    f.write(img_data['content'])
            
            # Convert to PDF
            print(f"\nCreating PDF...")
            pdf_filename = f"{exercise_name}.pdf"
            pdf_path = os.path.join(pdfs_dir, pdf_filename)
            
            self.save_as_pdf(images_data, pdf_path)
            
            # Cleanup temporary images
            for img_data in images_data:
                temp_path = os.path.join(images_dir, img_data['filename'])
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        print(f"\n{'='*60}")
        print("PROCESS COMPLETED!")
        print(f"PDFs saved in: {os.path.abspath(pdfs_dir)}")
        print(f"Individual images saved in: {os.path.abspath(images_dir)}")
        print(f"\nFiles downloaded:")
        for filename in os.listdir(pdfs_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(pdfs_dir, filename)
                size = os.path.getsize(filepath) / 1024 / 1024
                print(f"  • {filename} ({size:.2f} MB)")

    def generate_direct_image_urls(self, exercise):
        """Generate direct image URLs based on the pattern from your curl example"""
        base_pattern = "https://www.thestudypath.com/wp-content/uploads/2025/04/RS-Aggarwal-Solutions-Class-9-Chapter-15-Volumes-and-Surface-Area-of-Solids-Exercise-{exercise}_{page:05d}.jpg"
        
        # Map exercise names to URL patterns
        exercise_map = {
            'Exercise_15A': '15A',
            'Exercise_15B': '15B',
            'Exercise_15C': '15C',
            'Exercise_15D': '15D',
            'MCQs': 'MCQs'
        }
        
        exercise_code = exercise_map.get(exercise, exercise)
        urls = []
        
        # Try different page numbers
        for page_num in range(1, 51):  # Try up to 50 pages
            url = base_pattern.format(exercise=exercise_code, page=page_num)
            
            # Test if URL exists
            try:
                response = requests.head(url, headers=self.image_headers, timeout=3)
                if response.status_code == 200:
                    urls.append(url)
                    print(f"Found: {url}")
            except:
                continue
        
        return urls

def main():
    # Install required packages if not already installed
    required_packages = ['requests', 'beautifulsoup4', 'pillow']
    
    import subprocess
    import sys
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Run the scraper
    scraper = StudyPathScraper()
    scraper.scrape_all_exercises()

if __name__ == "__main__":
    main()