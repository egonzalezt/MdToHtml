import argparse
import sys
import os
import markdown
import re
import base64
from datetime import datetime

def convert_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Error converting image {image_path} to base64: {e}")
        return None

def convert_md_to_html(md_file_path, template_path='template.html', css_path='styles.css', encoding='utf-8', image_to_base64=True, use_dark_mode=False, dark_mode_css_path=None):
    try:
        # Read the content from the Markdown file with the specified encoding
        with open(md_file_path, 'r', encoding=encoding) as md_file:
            md_content = md_file.read()

        # Convert images to base64 if enabled
        if image_to_base64:
            # Find all images in Markdown (including those with HTML)
            image_pattern_md = re.compile(r'!\[.*?\]\((.*?)\)')
            image_pattern_html = re.compile(r'<img.*?src=["\'](.*?)["\'].*?>')
            
            images_md = image_pattern_md.findall(md_content)
            images_html = image_pattern_html.findall(md_content)

            all_images = images_md + images_html

            # Convert each image to base64 and replace in Markdown content
            for image_path in all_images:
                if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    continue  # Ignore if not an image

                base64_image = convert_image_to_base64(image_path)
                if base64_image:
                    ext = os.path.splitext(image_path)[1][1:]  # Get the image extension
                    data_uri = f"data:image/{ext};base64,{base64_image}"

                    if image_path in images_md:
                        md_content = md_content.replace(image_path, data_uri)
                    elif image_path in images_html:
                        md_content = md_content.replace(image_path, data_uri)

        # Convert Markdown to HTML with extensions for code highlighting
        html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])

        # Read the HTML template
        with open(template_path, 'r', encoding=encoding) as template_file:
            template_content = template_file.read()

        # Read the CSS file content
        with open(css_path, 'r', encoding=encoding) as css_file:
            css_content = css_file.read()

        # Add dark mode CSS if enabled and specified
        if use_dark_mode:
            if dark_mode_css_path:
                with open(dark_mode_css_path, 'r', encoding=encoding) as dark_css_file:
                    dark_mode_css_content = dark_css_file.read()
                css_content += dark_mode_css_content
            else:
                print("Warning: Dark mode enabled but no dark mode CSS file provided.")

        # Insert the generated HTML content into the template
        full_html_content = template_content.replace("{{ content }}", html_content)

        # Add the timestamp in the specified section in RFC 850 format
        current_time = datetime.utcnow().strftime('%A, %d-%b-%y %H:%M:%S UTC')
        full_html_content = full_html_content.replace("{{ generated_at }}", f"Generated at {current_time}")

        # Insert the CSS content into the template
        full_html_content = full_html_content.replace("{{ styles }}", f"<style>{css_content}</style>")

        # Create an HTML file with the same name as the Markdown file
        html_file_path = os.path.splitext(md_file_path)[0] + '.html'

        # Check if the HTML file already exists
        if os.path.exists(html_file_path):
            user_response = input(f"The HTML file '{html_file_path}' already exists. Do you want to override it? (y/n): ")
            if user_response.lower() != 'y':
                print("Conversion aborted. HTML file was not overwritten.")
                return None

        # Write the HTML content to the file
        with open(html_file_path, 'w', encoding=encoding) as html_file:
            html_file.write(full_html_content)

        return html_file_path
    except UnicodeDecodeError:
        print(f"Error: Unable to decode the file '{md_file_path}' using encoding '{encoding}'")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: The file '{md_file_path}', '{template_path}', '{css_path}', or '{dark_mode_css_path}' was not found")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML with optional template and CSS.')
    parser.add_argument('--md-path', required=True, help='Path to the Markdown file')
    parser.add_argument('--template-path', default='template.html', help='Path to the HTML template file (default: template.html)')
    parser.add_argument('--css-path', default='styles.css', help='Path to the CSS file (default: styles.css)')
    parser.add_argument('--encoding', default='utf-8', help='Encoding of the files (default: utf-8)')
    parser.add_argument('--image-to-base64', choices=['1', 'true', 'True', '0', 'false', 'False'], default='1', help='Convert images to base64 in HTML (default: 1)')
    parser.add_argument('--use-dark-mode', choices=['1', 'true', 'True', '0', 'false', 'False'], default='0', help='Use dark mode in HTML (default: 0)')
    parser.add_argument('--dark-mode-css', default='dark-mode.css', help='Path to optional CSS file for dark mode')

    args = parser.parse_args()

    md_file_path = args.md_path
    template_path = args.template_path
    css_path = args.css_path
    encoding = args.encoding
    image_to_base64 = args.image_to_base64.lower() in ['1', 'true']
    use_dark_mode = args.use_dark_mode.lower() in ['1', 'true']
    dark_mode_css_path = args.dark_mode_css

    html_output_path = convert_md_to_html(md_file_path, template_path, css_path, encoding, image_to_base64, use_dark_mode, dark_mode_css_path)
    if html_output_path:
        print(f"The Markdown file '{md_file_path}' was converted to HTML and saved as '{html_output_path}'")

if __name__ == "__main__":
    main()
