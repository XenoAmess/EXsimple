import base64
import zlib

str = open("favicon.ico","rb").read();
str = zlib.compress(str);
str = base64.b64encode(str);
print(str);
