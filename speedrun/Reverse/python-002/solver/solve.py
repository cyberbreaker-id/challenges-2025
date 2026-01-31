import zlib

compressed = open('flag.png.cbc', 'rb').read()
decompressed = zlib.decompress(compressed[::-1])
open('flag.png', 'wb').write(decompressed)
