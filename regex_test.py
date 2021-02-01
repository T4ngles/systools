import re

with open("C:/Program Files/Blender Foundation/Blender/2.79/scripts/addons/pressure_automation/import_surrounds.py") as f:
	lines = f.readlines()

#condense = re.compile('(class)(.*)|\s*(def){1}(.*?)\):|(.*?)\(\)')

condense = re.compile('(class)(.*)|\s*(def){1}(.*?)\):|(.*?)\(\)')

for line in lines:
	if condense.match(line):
		print(condense.match(line).group())