# Create your views here.

with open(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\old.csv', 'r',encoding="utf8", errors='ignore') as t1, open(r'C:\Users\rishith\Desktop\Patch-Remainder-master\backend\mysite\core\new.csv', 'r', encoding="utf8", errors='ignore') as t2:
	fileone = t1.readlines()
	filetwo = t2.readlines()
print("Reading Complete")
with open(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\update.csv', 'w', encoding="utf8", errors='ignore') as outFile:
	for line in filetwo[:1000]:
		if line not in fileone[:1000]:
			outFile.write(line)
