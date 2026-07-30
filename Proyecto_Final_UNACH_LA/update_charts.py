import glob
import os

files = glob.glob('06_Dashboard_React/src/components/**/*.jsx', recursive=True)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replacement for chart grids to switch from white transparent to black transparent
    new_content = content.replace("rgba(255, 255, 255, 0.04)", "rgba(0, 0, 0, 0.06)")
    new_content = new_content.replace("rgba(255, 255, 255, 0.05)", "rgba(0, 0, 0, 0.05)")
    new_content = new_content.replace("rgba(255, 255, 255, 0.06)", "rgba(0, 0, 0, 0.08)")
    new_content = new_content.replace("rgba(255, 255, 255, 0.08)", "rgba(0, 0, 0, 0.1)")
    new_content = new_content.replace("rgba(255, 255, 255, 0.2)", "rgba(0, 0, 0, 0.15)")
    
    # Tooltip backgrounds
    new_content = new_content.replace("backgroundColor: 'rgba(17, 24, 39, 0.95)'", "backgroundColor: 'rgba(255, 255, 255, 0.95)'")
    new_content = new_content.replace("titleColor: '#fff'", "titleColor: '#0f172a'")
    new_content = new_content.replace("bodyColor: '#cbd5e1'", "bodyColor: '#334155'")
    new_content = new_content.replace("borderColor: 'rgba(255, 255, 255, 0.1)'", "borderColor: 'rgba(0, 0, 0, 0.1)'")

    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file}")

print("Done updating charts")
