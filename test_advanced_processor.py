#!/usr/bin/env python3
import requests
import json
import time
import sys

def test_chat_generation():
    """Test the fixed AdvancedAIProcessor via chat API"""
    
    url = "http://localhost:5000/api/chat"
    
    # Test with a simple project request
    data = {
        "message": "Создайте простое приложение с красивым дизайном - HTML страница с CSS стилями и JavaScript анимациями",
        "session_id": f"test_session_{int(time.time())}"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing AdvancedAIProcessor via chat API...")
    print(f"📡 Sending request to {url}")
    print(f"💬 Message: {data['message']}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            
            # Check if project was generated
            if 'project_id' in result:
                project_id = result['project_id']
                print(f"🎯 Generated Project ID: {project_id}")
                
                # Check project files
                if 'files' in result:
                    files = result['files']
                    print(f"📁 Generated {len(files)} files:")
                    
                    file_checks = {
                        'index.html': False,
                        'styles.css': False,
                        'script.js': False
                    }
                    
                    for filename, content in files.items():
                        print(f"\n📄 {filename} ({len(content)} chars)")
                        
                        # Check file content type correctness
                        if filename == 'index.html':
                            if '<!DOCTYPE html>' in content and '<html' in content:
                                print("  ✅ HTML content detected correctly")
                                file_checks['index.html'] = True
                            else:
                                print("  ❌ Invalid HTML content")
                                print(f"  Content preview: {content[:200]}...")
                                
                        elif filename == 'styles.css':
                            if ('body' in content or 'html' in content or '{' in content) and not '<html' in content:
                                print("  ✅ CSS content detected correctly")
                                file_checks['styles.css'] = True
                            else:
                                print("  ❌ Invalid CSS content (contains HTML?)")
                                print(f"  Content preview: {content[:200]}...")
                                
                        elif filename == 'script.js':
                            if ('function' in content or 'const' in content or 'var' in content or 'let' in content) and not '<html' in content:
                                print("  ✅ JavaScript content detected correctly")
                                file_checks['script.js'] = True
                            else:
                                print("  ❌ Invalid JavaScript content (contains HTML?)")
                                print(f"  Content preview: {content[:200]}...")
                    
                    # Summary
                    print("\n🔍 File Type Detection Summary:")
                    correct_files = sum(file_checks.values())
                    total_files = len(file_checks)
                    
                    for filename, is_correct in file_checks.items():
                        status = "✅" if is_correct else "❌"
                        print(f"  {status} {filename}")
                    
                    if correct_files == total_files:
                        print(f"\n🎉 SUCCESS: All {total_files} files have correct content types!")
                        print("✅ AdvancedAIProcessor file type detection bug is FIXED!")
                        return True
                    else:
                        print(f"\n⚠️  PARTIAL SUCCESS: {correct_files}/{total_files} files have correct content types")
                        print("❌ AdvancedAIProcessor file type detection bug still exists")
                        return False
                else:
                    print("❌ No files in response")
                    return False
            else:
                print("❌ No project_id in response")
                print(f"Response: {result}")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Response text: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_chat_generation()
    sys.exit(0 if success else 1)