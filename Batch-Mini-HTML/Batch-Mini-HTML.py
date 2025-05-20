import os
import re

def minify_html(html):
    scripts = re.findall(r'<(script|style)(.*?)>(.*?)</\1>', html, flags=re.DOTALL)
    placeholders = []
    for i, (tag, attrs, content) in enumerate(scripts):
        placeholder = f"___PLACEHOLDER_{i}___"
        full_block = f"<{tag}{attrs}>{content}</{tag}>"
        html = html.replace(full_block, placeholder)
        placeholders.append((placeholder, full_block))

    html = html.replace('\n', '').replace('\r', '').replace('\t', '')
    html = re.sub(r'>\s+<', '><', html)
    html = re.sub(r'\s{2,}', ' ', html)

    for placeholder, original in placeholders:
        html = html.replace(placeholder, original)

    return html.strip()

def batch_minify_html_files(folder):
    print(f"\n🔍 Scanning folder: {folder}")
    files = os.listdir(folder)

    html_files = [f for f in files if f.lower().endswith(('.html', '.htm'))]
    print(f"Found HTML files: {html_files}")

    if not html_files:
        print("⚠️ No HTML files found.")
        return

    for filename in html_files:
        print(f"Processing file: {filename}")
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_html = f.read()

            minified_html = minify_html(original_html)

            output_filename = f"minified_{filename}"
            output_path = os.path.join(folder, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(minified_html)

            print(f"✅ Created: {output_filename}")
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.abspath(__file__))
    batch_minify_html_files(folder_path)
    input("\n🎉 Done. Press Enter to exit...")
