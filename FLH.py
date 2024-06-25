# Winbond Voice Editor extractor (uwu)
print("Winbond Voice Editor File Extractor.")
import pathlib,struct,sys
# Usage Statement
def usage():
	print("Usage: %s <.flh file> <destination directory>" % sys.argv[0])
	exit()
# WAV read for output loop
def read_wav_chunk(fp):
	global headernum
	headernum = headernum + 1 
	foo = fp.read(0x54)
	data_size, header = struct.unpack('<I80s', foo)
	data = fp.read(data_size)
	assert len(data) == data_size, f"Header #%s is too small.\nExpected: {data_size}\nRead:{len(data)}" % headernum
	return data_size, header, data
# User Input: *.FLH file for Winbond Voice Editor
try:
	filein = sys.argv[1]
except:
	usage()
# User Input: Output directory (Currently, we panic if the given path doesn't exist.)
try:
	destination = sys.argv[2]
except:
	usage()
# debug print paths input
#print("Provided file: " + filein + "\n" + "Output directory: " + destination)
# open file and read into buffer
filebuffer = open(filein, 'rb')
print("File opened.")
# Read # of WAVs, little-endian
header_chunks = int.from_bytes(filebuffer.read(4), 'little')
print(str(header_chunks) + " files specified.")
# Read table of WAV names
first_headers = [filebuffer.read(0x52) for i in range(0, header_chunks)]
# Read table of sound/POST status definitions(?)
funny_headers = struct.unpack('80s'*151, filebuffer.read(0x50*151))
# 0x12E of padding(???)
padding = filebuffer.read(0x12E)
# WAV Output Loop
headernum = 0
wavs = [read_wav_chunk(filebuffer) for i in range(0, header_chunks)]
for i in wavs:
	# 1 is the header part, . just cheats the \ from messing pathlib
	name = '.' + i[1].split(b'\x00')[0].decode()
	out = (pathlib.Path(destination) / pathlib.PureWindowsPath(name)).absolute()
	out.parent.mkdir(parents=True, exist_ok=True)	
	with out.open('wb') as o:
		# 2 is data
		print(out)
		o.write(i[2])