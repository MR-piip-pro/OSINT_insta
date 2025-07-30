#!/usr/bin/env python3
"""
🔍 أداة OSINT المحسنة لـ Instagram
نسخة محسنة مع طرق استخراج أفضل
"""

import requests
import json
import re
import os
from datetime import datetime
from urllib.parse import urljoin

class ImprovedOSINT:
    """
    أداة OSINT محسنة لـ Instagram
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """إعداد الجلسة مع headers محسنة"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def print_banner(self):
        """طباعة شعار الأداة"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                🔍 أداة OSINT المحسنة                        ║
║         Instagram Intelligence Tool (Improved)               ║
║                                                              ║
║  أداة استخبارات رقمية محسنة لجمع المعلومات من Instagram    ║
║  مع طرق استخراج متقدمة - للأغراض التعليمية والبحثية فقط    ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def extract_instagram_data(self, username: str):
        """استخراج بيانات Instagram بطريقة محسنة"""
        try:
            print(f"🔍 جاري جمع بيانات Instagram للمستخدم: {username}")
            
            # URL حساب Instagram
            url = f"https://www.instagram.com/{username}/"
            
            # إجراء الطلب
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # استخراج البيانات الأساسية
            data = {
                'username': username,
                'url': url,
                'status': 'found',
                'timestamp': datetime.now().isoformat()
            }
            
            page_text = response.text
            
            # تحليل محسن للبيانات
            self._extract_basic_info(data, page_text)
            self._extract_meta_data(data, page_text)
            self._extract_account_info(data, page_text)
            
            print("✅ تم جمع بيانات Instagram بنجاح")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return None
        except Exception as e:
            print(f"❌ خطأ في استخراج البيانات: {e}")
            return None
    
    def _extract_basic_info(self, data, page_text):
        """استخراج المعلومات الأساسية"""
        # البحث عن عنوان الصفحة
        title_match = re.search(r'<title>(.*?)</title>', page_text)
        if title_match:
            data['title'] = title_match.group(1)
        
        # البحث عن الوصف
        desc_match = re.search(r'<meta name="description" content="(.*?)"', page_text)
        if desc_match:
            data['description'] = desc_match.group(1)
        
        # البحث عن صورة الملف الشخصي
        img_match = re.search(r'<meta property="og:image" content="(.*?)"', page_text)
        if img_match:
            data['profile_image'] = img_match.group(1)
    
    def _extract_meta_data(self, data, page_text):
        """استخراج البيانات الوصفية"""
        # البحث عن نوع الحساب بطريقة محسنة
        private_indicators = ['private', 'هذا الحساب خاص', 'this account is private']
        verified_indicators = ['verified', 'موثق', 'حساب موثق']
        
        page_lower = page_text.lower()
        
        if any(indicator in page_lower for indicator in private_indicators):
            data['account_type'] = 'private'
        elif any(indicator in page_lower for indicator in verified_indicators):
            data['account_type'] = 'verified'
        else:
            data['account_type'] = 'public'
        
        # البحث عن البيانات في JSON embedded
        json_patterns = [
            r'"followers":\s*(\d+)',
            r'"following":\s*(\d+)',
            r'"posts":\s*(\d+)',
            r'"biography":\s*"([^"]*)"',
            r'"full_name":\s*"([^"]*)"'
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, page_text)
            if match:
                if 'followers' in pattern:
                    data['followers'] = match.group(1)
                elif 'following' in pattern:
                    data['following'] = match.group(1)
                elif 'posts' in pattern:
                    data['posts'] = match.group(1)
                elif 'biography' in pattern:
                    data['biography'] = match.group(1)
                elif 'full_name' in pattern:
                    data['full_name'] = match.group(1)
    
    def _extract_account_info(self, data, page_text):
        """استخراج معلومات الحساب"""
        # البحث عن عدد المتابعين (أنماط متعددة)
        followers_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:followers|متابع)',
            r'(\d+(?:,\d+)*)\s*متابع',
            r'(\d+(?:,\d+)*)\s*Follower',
            r'"followers_count":\s*(\d+)',
            r'"edge_followed_by":\s*{\s*"count":\s*(\d+)'
        ]
        
        for pattern in followers_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match and 'followers' not in data:
                data['followers'] = match.group(1)
                break
        
        # البحث عن عدد المنشورات
        posts_patterns = [
            r'(\d+)\s*(?:posts|منشور)',
            r'(\d+)\s*منشور',
            r'"posts_count":\s*(\d+)',
            r'"edge_owner_to_timeline_media":\s*{\s*"count":\s*(\d+)'
        ]
        
        for pattern in posts_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match and 'posts' not in data:
                data['posts'] = match.group(1)
                break
        
        # البحث عن عدد المتابَعين
        following_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:following|يتبع)',
            r'(\d+(?:,\d+)*)\s*يتبع',
            r'"following_count":\s*(\d+)',
            r'"edge_follow":\s*{\s*"count":\s*(\d+)'
        ]
        
        for pattern in following_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match and 'following' not in data:
                data['following'] = match.group(1)
                break
    
    def search_social_presence(self, username: str):
        """البحث عن وجود الحساب في مواقع أخرى"""
        print(f"🌍 جاري البحث عن وجود الحساب في مواقع أخرى...")
        
        sites = [
            'linkedin.com',
            'twitter.com',
            'tiktok.com',
            'facebook.com',
            'youtube.com',
            'github.com',
            'medium.com',
            'reddit.com'
        ]
        
        results = {}
        
        for site in sites:
            try:
                url = f"https://{site}/{username}"
                response = self.session.get(url, timeout=10)
                results[site] = {
                    'found': response.status_code == 200,
                    'url': url,
                    'status_code': response.status_code
                }
                print(f"  {site}: {'✅' if response.status_code == 200 else '❌'}")
            except Exception as e:
                results[site] = {
                    'found': False,
                    'url': f"https://{site}/{username}",
                    'error': str(e)
                }
                print(f"  {site}: ❌ (خطأ)")
        
        return results
    
    def download_profile_image(self, image_url: str, username: str):
        """تحميل صورة الملف الشخصي"""
        try:
            print(f"📸 جاري تحميل صورة الملف الشخصي...")
            
            # إنشاء مجلد الصور إذا لم يكن موجوداً
            os.makedirs('output/images', exist_ok=True)
            
            # تحميل الصورة
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            # حفظ الصورة
            image_path = f"output/images/{username}_profile.jpg"
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ تم تحميل الصورة: {image_path}")
            return image_path
            
        except Exception as e:
            print(f"❌ خطأ في تحميل الصورة: {e}")
            return None
    
    def generate_report(self, username: str, data, social_data=None, image_path=None):
        """إنشاء تقرير شامل"""
        # إنشاء مجلد التقارير
        os.makedirs('output/reports', exist_ok=True)
        
        # إنشاء التقرير
        report = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'instagram_data': data,
            'social_presence': social_data,
            'image_path': image_path,
            'summary': self._generate_summary(data, social_data, image_path)
        }
        
        # حفظ التقرير
        report_path = f"output/reports/{username}_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 تم إنشاء التقرير: {report_path}")
        return report_path
    
    def _generate_summary(self, data, social_data=None, image_path=None):
        """إنشاء ملخص النتائج"""
        summary = {
            'account_found': data is not None,
            'has_profile_image': 'profile_image' in data and data['profile_image'],
            'has_description': 'description' in data and data['description'],
            'social_sites_found': 0
        }
        
        if social_data:
            summary['social_sites_found'] = sum(1 for site_data in social_data.values() if site_data.get('found', False))
        
        return summary
    
    def print_results_summary(self, data, social_data=None, image_path=None):
        """طباعة ملخص النتائج"""
        print("\n" + "="*60)
        print("📊 ملخص النتائج")
        print("="*60)
        
        if data:
            print(f"👤 اسم المستخدم: @{data.get('username', 'N/A')}")
            print(f"📝 العنوان: {data.get('title', 'N/A')}")
            print(f"🔐 نوع الحساب: {data.get('account_type', 'N/A')}")
            print(f"📄 الوصف: {data.get('description', 'N/A')}")
            print(f"👥 المتابعون: {data.get('followers', 'N/A')}")
            print(f"👥 المتابَعون: {data.get('following', 'N/A')}")
            print(f"📸 المنشورات: {data.get('posts', 'N/A')}")
            print(f"👤 الاسم الكامل: {data.get('full_name', 'N/A')}")
            print(f"📝 السيرة الذاتية: {data.get('biography', 'N/A')}")
            
            if social_data:
                print(f"\n🌍 المواقع الاجتماعية:")
                for site, site_data in social_data.items():
                    status = "✅" if site_data.get('found') else "❌"
                    print(f"  {site}: {status}")
            
            if image_path:
                print(f"\n📸 صورة الملف الشخصي: {image_path}")
        else:
            print("❌ لم يتم العثور على البيانات")
        
        print("="*60)
    
    def run_analysis(self, username: str, social_search=False, image_download=False):
        """تشغيل التحليل الكامل"""
        self.print_banner()
        
        # جمع بيانات Instagram
        data = self.extract_instagram_data(username)
        
        social_data = None
        image_path = None
        
        if social_search:
            social_data = self.search_social_presence(username)
        
        if image_download and data and 'profile_image' in data:
            image_path = self.download_profile_image(data['profile_image'], username)
        
        # إنشاء التقرير
        report_path = self.generate_report(username, data, social_data, image_path)
        
        # طباعة الملخص
        self.print_results_summary(data, social_data, image_path)
        
        print(f"✅ تم إكمال التحليل! التقرير محفوظ في: {report_path}")

def main():
    """الدالة الرئيسية"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
🔍 أداة OSINT المحسنة لـ Instagram

📋 الاستخدام:
  python simple_osint_improved.py <username> [options]

🔧 الخيارات:
  --social-search     البحث في المواقع الاجتماعية
  --image-download    تحميل صورة الملف الشخصي

📝 أمثلة:
  python simple_osint_improved.py instagram_user
  python simple_osint_improved.py username --social-search --image-download

⚠️  تحذير: هذا الأداة للأغراض التعليمية والبحثية فقط
        """)
        return
    
    username = sys.argv[1]
    social_search = '--social-search' in sys.argv
    image_download = '--image-download' in sys.argv
    
    osint = ImprovedOSINT()
    osint.run_analysis(username, social_search, image_download)

if __name__ == "__main__":
    main() 