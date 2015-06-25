import sys, os, shutil, subprocess, fhash

ZIP_LIST = [
	"3rd_party/boost",
	"3rd_party/FreeImage",
	"3rd_party/freetype2",
	"3rd_party/llvm",
	"3rd_party/threadpool",
	'resources/astro_boy',
	'resources/complex_mesh',
	'resources/cup',
	'resources/font',
	'resources/morph',
	'resources/sponza_hq',
	'resources/sponza_lq',
	'resources/ssm',
	'resources/texture_and_blending',
]

RAW_LIST = [
	"basic_tools/linux/7z"		,
	"basic_tools/linux/7z.so"	,
	"basic_tools/win32/7z.dll"	,
	"basic_tools/win32/7z.exe"	,
]

def ToPath(posixpath):
	return os.path.join( *posixpath.split('/') )
	
ZIP_BIN   = ToPath("basic_tools/win32/7z.exe")
SIG_FILE  = ToPath("sig.txt")

if __name__ == "__main__":
	dstPath = ToPath("../release")
	srcPath = ToPath("../workshop")
	
	fileHash = []
	
	zipBinFullPath  = os.path.join(srcPath, ZIP_BIN)
	sigFileFullPath = os.path.join(dstPath, SIG_FILE)
	with open("log.txt", "a") as f:
		f.write("GenPackage - Start\n")
		for zipSource in ZIP_LIST:
			zipSrcFullPath = os.path.join( srcPath, ToPath(zipSource) )
			zipDstFullPath = os.path.join( dstPath, ToPath(zipSource + ".7z") )
			print("Compressing <%s>" % zipSource)
			o = subprocess.check_output([zipBinFullPath, "a", zipDstFullPath, zipSrcFullPath])
			f.writelines(o)
			if o.split('\n')[-2].strip() != "Everything is Ok":
				print "Error occured. details are in log.txt"
				sys.exit(1)
			print("Hashing <%s>" % zipSource)
			hashCode = fhash.hash_file(zipDstFullPath)
			fileHash.append( (zipSource, hashCode) )
			
	for rawSource in RAW_LIST:
		rawSrcFullPath = os.path.join( srcPath, ToPath(rawSource) )
		rawDstFullPath = os.path.join( dstPath, ToPath(rawSource) )
		print("Copying <%s>" % rawSource)
		if os.path.isfile(rawSrcFullPath):
			dirName = os.path.dirname(rawDstFullPath)
			if not os.path.isdir(dirName):
				os.makedirs(dirName)
			shutil.copyfile(rawSrcFullPath, rawDstFullPath)
			print("Hashing <%s>" % rawSource)
			hashCode = fhash.hash_file(rawDstFullPath)
			fileHash.append( (rawSource, hashCode) )
		else:
			print("File is not existed.")
			
	print('Writing file hash code')
	with open(sigFileFullPath, "w") as sigFile:
		for fName, hashCode in fileHash:
			sigFile.write(fName + '\n')
			sigFile.write(hashCode + '\n')
	
	print("Packaging Done")