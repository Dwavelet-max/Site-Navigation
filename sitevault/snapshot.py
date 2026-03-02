import os
import re
import uuid
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def save_html_snapshot(url, save_dir, user_id=None):
    """保存网页HTML内容，包含内联CSS和相对路径图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.encoding = response.apparent_encoding or 'utf-8'
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        base_url = url
        
        for img in soup.find_all('img'):
            img_src = img.get('src')
            if img_src and not img_src.startswith(('http://', 'https://', 'data:')):
                img_url = urljoin(base_url, img_src)
                try:
                    img_resp = requests.get(img_url, headers=headers, timeout=10, verify=False)
                    if img_resp.status_code == 200:
                        ext = os.path.splitext(img_url)[1] or '.png'
                        if not ext or len(ext) < 2:
                            ext = '.png'
                        img_data = img_resp.content
                        img_tag = f'data:image/{ext[1:]};base64,'
                        img_tag += __import__('base64').b64encode(img_data).decode('utf-8')
                        img['src'] = img_tag
                except:
                    pass
        
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href and not href.startswith(('http://', 'https://')):
                css_url = urljoin(base_url, href)
                try:
                    css_resp = requests.get(css_url, headers=headers, timeout=10, verify=False)
                    if css_resp.status_code == 200:
                        style_tag = soup.new_tag('style')
                        style_tag.string = css_resp.text
                        link.replace_with(style_tag)
                except:
                    pass
        
        folder_name = str(uuid.uuid4())[:8]
        if user_id:
            folder_name = f"{user_id}_{folder_name}"
        folder_path = os.path.join(save_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        html_file = os.path.join(folder_path, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return folder_name
    except Exception as e:
        print(f"保存HTML失败: {e}")
        return None
