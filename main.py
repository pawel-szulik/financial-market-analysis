import os
import webbrowser

os.system("jupyter nbconvert --to html --template lab --theme=dark notebooks/analysis.ipynb")

webbrowser.open("notebooks/analysis.html")