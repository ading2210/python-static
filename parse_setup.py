import pathlib
import sys
import re

#parse the Modules/Setup file and generate a valid Modules/Setup.local file to allow static linking

#these are just the ones that failed to compile on my system
excluded_modules = ["_testcapi", "_testinternalcapi", "nis", "_dbm", "_ssl", "_gdbm"]

setup_path = pathlib.Path(sys.argv[1]).resolve()
setup_text = setup_path.read_text()

enabled_regex = r"^([^\s#]+?) (.+?\.c.*?)(#|$)"
disabled_regex = r"^#([^\s#]+?) (.+?\.c.*?)(#|$)"

enabled_matches = re.findall(enabled_regex, setup_text, flags=re.M)
disabled_matches = re.findall(disabled_regex, setup_text, flags=re.M)
all_matches = enabled_matches + disabled_matches

new_setup = "*static*"
for module, args, end in all_matches:
  if module in excluded_modules: 
    continue
  new_setup += f"\n{module} {args}"

#new_setup += "\n\n*disabled*"
#for module, args, end in disabled_matches:  
#  new_setup += f"\n{module} {args}"

print(new_setup)