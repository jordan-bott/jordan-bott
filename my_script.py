from "wordle/update_readme.py" import readme_content

file = open("README.md", "a")
file.write("Added to the readme")
file.close()

print("script ran")
