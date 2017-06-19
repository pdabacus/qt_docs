#!/usr/bin/python3

import os

def binary_search(arr, e):
	low = 0
	mid = -1
	high = len(arr)-1
	found = False
	tooLow = True
	while not found and low <= high:
		mid = int((low + high)/2)
		if arr[mid] == e:
			found = True
		elif arr[mid] > e:
			high = mid - 1
			tooLow = True
		else:
			low = mid + 1
			tooLow = False
	if found:
		return mid, mid
	elif tooLow:
		return high, mid
	else:
		return mid, low

def insert(arr, e):
	a,b = binary_search(arr, e)
	if len(arr) == 0:
		arr += [e]
	elif a < b:
		arr.insert(b, e)

def main():
	docs = "docs/"
	oldfiles = []
	newfiles = [x for x in open("files.txt", "r").read().split("\n") if len(x) > 3]

	while newfiles != oldfiles:
		oldfiles = newfiles
		newfiles = ["index.html"]
		for path in oldfiles:
			if os.path.exists(docs+path):
				href = [h for h in open(docs+path, "r").read().split(" ") if "href" in h and ".html" in h and "#" not in h and "/" not in h]
				for h in href:
					hs = h.split('"')
					if len(hs) >= 2:
						insert(newfiles, hs[1])

	open("files.txt", "w").write("\n".join(newfiles) + "\n")

if __name__ == '__main__':
	main()
