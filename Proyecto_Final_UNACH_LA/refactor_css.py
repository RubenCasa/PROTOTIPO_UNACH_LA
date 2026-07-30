import re

file_path = '06_Dashboard_React/src/index.css'

with open(file_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Refactor Sidebar
css = css.replace('background: rgba(17, 24, 39, 0.95);', 'background: rgba(255, 255, 255, 0.95);')
css = css.replace('background: rgba(255, 255, 255, 0.04);', 'background: rgba(0, 0, 0, 0.04);')

# Refactor Hero
css = css.replace('background: linear-gradient(135deg, #0b1120 0%, #0c2d4a 30%, #1a1040 70%, #2d0a1e 100%);', 'background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 30%, #f3e8ff 70%, #fdf4ff 100%);')
css = css.replace('background: linear-gradient(180deg, rgba(11,17,32,0.4) 0%, rgba(11,17,32,0.8) 60%, rgba(11,17,32,1) 100%);', 'background: linear-gradient(180deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.8) 60%, rgba(255,255,255,1) 100%);')
css = css.replace('color: white;', 'color: #ffffff;') # Buttons usually stay white text if they have gradient bg
css = css.replace('background: rgba(255, 255, 255, 0.05);', 'background: rgba(0, 0, 0, 0.03);')
css = css.replace('border: 1px solid rgba(255, 255, 255, 0.08);', 'border: 1px solid rgba(0, 0, 0, 0.05);')

# Dashboard Section borders
css = css.replace('border-bottom: 1px solid rgba(255, 255, 255, 0.05);', 'border-bottom: 1px solid rgba(0, 0, 0, 0.05);')
css = css.replace('border-bottom: 1px solid rgba(255, 255, 255, 0.03);', 'border-bottom: 1px solid rgba(0, 0, 0, 0.03);')

# Risk Bar
css = css.replace('background: rgba(255, 255, 255, 0.06);', 'background: rgba(0, 0, 0, 0.06);')

# Scrollbar
css = css.replace('background: rgba(255, 255, 255, 0.1);', 'background: rgba(0, 0, 0, 0.1);')
css = css.replace('background: rgba(255, 255, 255, 0.2);', 'background: rgba(0, 0, 0, 0.2);')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS Light Theme refactoring completed.")
