import os
import sys
import zlib

def main(argc=len(sys.argv), argv=sys.argv):
  if argc != 2:
    print("Usage: %s cdxtract.exe" % argv[0])
    return 1

  in_path = os.path.abspath(argv[1])
  basename = os.path.basename(in_path)
  name, ext = os.path.splitext(basename)

  out_dir = os.path.dirname(argv[0])
  out_name = "%s_fixed%s" % (name, ext) # mind = blown, in Windows 7 at least, it looks like executables with "patch" in the name will prompt UAC!
  out_path = os.path.join(out_dir, out_name)

  with open(in_path, "rb") as f:
    data = bytearray( f.read() )

  if zlib.crc32(data) != 0xDAAEC780:
    print("The supplied executable is not supported!")
    print("Only CDXtract 4.5 is currently supported.")
    print("Also, make sure to unpack the exe before passing it.")
    return 1

  # update branch (jz 0x40BE1F) to account for relocated instructions
  data[0xBDAB : 0xBDAD] = b"\x74\x72"

  # move code down 3 bytes to make room for pushing a word instead of a byte
  data[0xBE09 : 0xBE25] = data[0xBE06 : 0xBE22]

  # replace original timeSetEvent parameter "fuEvent" value 0x1, adding 0x100 flag (TIME_KILL_SYNCHRONOUS)
  data[0xBE04 : 0xBE09] = b"\x68\x01\x01\x00\x00"

  with open(out_path, "wb") as f:
    f.write(data)

if __name__ == "__main__":
  main()
