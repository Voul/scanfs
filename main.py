import scanfs
import optparse
import os
import json

def x_parse():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", action="store", dest="CONFIG", default="/etc/scanfs.conf")
    return parser


if __name__ == "__main__":
    parser = x_parse()
    (options, args) = parser.parse_args()
    if not os.path.isfile(options.CONFIG):
        exit()

    with open(options.CONFIG, "r") as f:
        content = f.read()

    jd = json.loads(content)
    if "db" not in jd.keys() \
            or "scanpath" not in jd.keys():
        exit()
    if "scanexclude" in jd.keys():
        scanfs.scanexclude = jd["scanexclude"]
    if "rmexclude" in jd.keys():
        scanfs.rmexclude = jd["rmexclude"]
    pass