#!/usr/bin/env python3
import sys
import os
sys.path.append('backend')

from advanced_ai_processor import AdvancedAIProcessor, RequestType

def test_direct_processor():
    """Test the AdvancedAIProcessor directly to verify file type detection fix"""
    
    print("🧪 Testing AdvancedAIProcessor directly...")
    
    # Create processor instance
    processor = AdvancedAIProcessor()
    
    # Test project generation request
    test_message = "Создайте простое приложение с красивым дизайном - HTML страница с CSS стилями и JavaScript анимациями"
    
    print(f"💬 Test message: {test_message}")
    print("🤖 Analyzing request...")
    
    # Analyze the request
    analysis = processor.analyze_user_request(test_message)
    print(f"📊 Request analysis: {analysis}")
    
    if analysis.request_type == RequestType.CREATE_NEW_PROJECT:
        print("✅ Request correctly identified as CREATE_NEW_PROJECT")
        
        # Create a simple progress callback
        def progress_callback(message, percentage=None):
            if percentage is not None:
                print(f"📈 Progress ({percentage}%): {message}")
            else:
                print(f"📈 Progress: {message}")
        
        print("🔧 Generating project...")
        try:
            project = processor.generate_project(analysis, progress_callback=progress_callback)
            
            if project and hasattr(project, 'files') and project.files:
                print(f"🎯 Generated project with {len(project.files)} files")
                
                # Check file content types
                file_checks = {
                    'index.html': False,
                    'styles.css': False,
                    'script.js': False
                }
                
                for filename, content in project.files.items():
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
                        # CSS should contain CSS syntax and NOT contain HTML tags
                        has_css_syntax = any(x in content.lower() for x in ['body', 'html', '{', '}', 'color:', 'font-', 'margin', 'padding'])
                        has_html_tags = '<html' in content.lower() or '<!doctype' in content.lower()
                        
                        if has_css_syntax and not has_html_tags:
                            print("  ✅ CSS content detected correctly")
                            file_checks['styles.css'] = True
                        else:
                            print(f"  ❌ Invalid CSS content (has_css_syntax={has_css_syntax}, has_html_tags={has_html_tags})")
                            print(f"  Content preview: {content[:200]}...")
                            
                    elif filename == 'script.js':
                        # JavaScript should contain JS syntax and NOT contain HTML tags
                        has_js_syntax = any(x in content for x in ['function', 'const', 'var', 'let', '()', '{', '}'])
                        has_html_tags = '<html' in content.lower() or '<!doctype' in content.lower()
                        
                        if has_js_syntax and not has_html_tags:
                            print("  ✅ JavaScript content detected correctly")
                            file_checks['script.js'] = True
                        else:
                            print(f"  ❌ Invalid JavaScript content (has_js_syntax={has_js_syntax}, has_html_tags={has_html_tags})")
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
                    if correct_files > 0:
                        print("🔧 Some files are correct - the fix is partially working")
                    else:
                        print("❌ AdvancedAIProcessor file type detection bug still exists")
                    return False
                    
            else:
                print("❌ No project generated or no files in project")
                return False
                
        except Exception as e:
            print(f"❌ Error generating project: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print(f"❌ Request not identified as CREATE_NEW_PROJECT (got {analysis.request_type})")
        return False

if __name__ == "__main__":
    success = test_direct_processor()
    sys.exit(0 if success else 1)