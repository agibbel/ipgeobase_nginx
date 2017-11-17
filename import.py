#!/usr/bin/python -Es
import urllib2
import zipfile
import os
from StringIO import StringIO

u = urllib2.urlopen("http://ipgeobase.ru/files/db/Main/geo_files.zip")
if u.getcode() != 200:
    error("Connection error: %s" % u.getcode)
pd = StringIO()
fs = int(u.info().getheaders("Content-Length")[0])
print "Downloading: %s" % (fs)
ds = 0
bs = 8192
while True:
    b = u.read(bs)
    if not b:
        break
    ds += len(b)
    pd.write(b)
    s = r"%10d  [%3.2f%%]" % (ds, ds * 100. / fs)
    s = s + chr(8)*(len(s)+1)
    print s,
print "Unpacking...          "
with zipfile.ZipFile(pd) as z, open("/etc/nginx/geo", 'w') as f:
    ec = z.read("cities.txt")
    ls = ec.splitlines()
    ct = []
    for l in ls:
        v = l.split("\t")
        while len(ct) <= int(v[0]):
            ct.append([])
        ct[int(v[0])] = [v[1].decode('cp1251').encode('utf8'), v[2].decode('cp1251').encode('utf8'), v[4], v[5]]
    ed = z.read("cidr_optim.txt")
    ls = ed.splitlines()
    f.write("geo $country {\n\tranges;\n\tdefault ZZ;\n")
    for l in ls:
        v = l.split("\t")
        f.write("\t" + v[2].replace(" ", "") + " " + v[3] + ";\n")
    f.write("}\n")
    f.write("geo $city {\n\tranges;\n\tdefault N/A;\n")
    for l in ls:
        v = l.split("\t")
        if v[4] != "-":
            f.write("\t" + v[2].replace(" ", "") + " \"" + ct[int(v[4])][0].replace("\"", "") + "\";\n")
    f.write("}\n")
    f.write("geo $region {\n\tranges;\n\tdefault N/A;\n")
    for l in ls:
        v = l.split("\t")
        if v[4] != "-":
            f.write("\t" + v[2].replace(" ", "") + " \"" + ct[int(v[4])][1].replace("\"", "") + "\";\n")
    f.write("}\n")
    f.write("geo $latitude {\n\tranges;\n\tdefault 0.0;\n")
    for l in ls:
        v = l.split("\t")
        if v[4] != "-":
            f.write("\t" + v[2].replace(" ", "") + " " + ct[int(v[4])][2] + ";\n")
    f.write("}\n")
    f.write("geo $longitude {\n\tranges;\n\tdefault 0.0;\n")
    for l in ls:
        v = l.split("\t")
        if v[4] != "-":
            f.write("\t" + v[2].replace(" ", "") + " " + ct[int(v[4])][3] + ";\n")
    f.write("}\n")
    f.close()
    os.system("nginx -s reload")
