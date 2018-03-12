import base64
import zlib

tstr = open("favicon.ico","rb").read();
tstr = zlib.compress(tstr);
tstr = base64.b64encode(tstr);
print(str);
