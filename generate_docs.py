"""Generate Module Documentation

This script generates HTML documentation for all project modules.

Functions:
    generate_module_doc(module_name: str, output_dir: str = 'docs'): Generate documentation for a single module
    generate_docs(): Generate documentation for all modules
"""

import os
import sys
import importlib
import inspect

def generate_module_doc(module_name: str, output_dir: str = 'docs'):
    """Generate HTML documentation for a single module
    
    Args:
        module_name: Module name
        output_dir: Output directory
    """
    try:
        module = importlib.import_module(module_name)
        
        doc = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{module_name} Documentation</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
        }}
        .function {{
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .class {{
            margin: 30px 0;
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
<h1>{module_name} Module Documentation</h1>

<h2>Module Description</h2>
<pre>{module.__doc__ or 'No documentation available'}</pre>

<h2>Classes</h2>
"""
        # Get all classes
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                doc += f"""
<div class="class">
<h3>class {name}</h3>
<pre>{obj.__doc__ or 'No documentation available'}</pre>
"""
                # Get class methods
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    if not method_name.startswith('_'):
                        doc += f"""
<div class="function">
<h4>Method: {method_name}</h4>
<pre>{method.__doc__ or 'No documentation available'}</pre>
</div>
"""
                doc += "</div>"

        doc += "<h2>Functions</h2>"
        
        # Get all functions
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if obj.__module__ == module_name:
                doc += f"""
<div class="function">
<h3>{name}</h3>
<pre>{obj.__doc__ or 'No documentation available'}</pre>
</div>
"""

        doc += """
</body>
</html>
"""

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Write file
        output_file = os.path.join(output_dir, f"{module_name.split('.')[-1]}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)
            
        print(f"Successfully generated documentation: {output_file}")
        
    except Exception as e:
        print(f"Error generating documentation for {module_name}: {e}")

def generate_docs():
    """Generate documentation for all modules"""
    # Add current directory to Python path
    sys.path.insert(0, os.path.abspath('.'))
    
    # List of modules to document
    modules = [
        'modules.auth',
        'modules.user',
        'modules.weather',
        'modules.styles'
    ]
    
    # Generate documentation for each module
    for module in modules:
        generate_module_doc(module)
    
    # Generate index page
    index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Forecast System Documentation</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
    </style>
</head>
<body>
    <h1>Weather Forecast System Documentation</h1>
    <ul>
"""
    
    for module in modules:
        module_name = module.split('.')[-1]
        index_html += f'        <li><a href="{module_name}.html">{module} Module</a></li>\n'
    
    index_html += """
    </ul>
</body>
</html>
"""
    
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

if __name__ == '__main__':
    generate_docs() 