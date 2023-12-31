import code
import sys
import platform
import argparse
import runpy
import importlib
import pathlib

#a command-line interface for python which should be mostly compatible with the original one
VERSION="1.0.0"

#trick freeze into including these modules without actually importing them
#the code the if statement will be modified by the build script, and replaced
#by an unreachable import statement
if sys.copyright == "":
  pass #modules_here

def get_script_dir(path):
  script_path = pathlib.Path(path).resolve()
  return str(script_path.parent)

def mode_interactive(quiet=False):
  version = sys.version.replace("\n", "")
  banner = ""
  if not quiet:
    banner = f'Python {version} on {sys.platform}, python-static {VERSION}\n'
    banner += 'Type "help", "copyright", "credits" or "license" for more information.'
  code.interact(exitmsg="", banner=banner)

def mode_print_version():
  print(f"Python {platform.python_version()}, python-static {VERSION}")

def mode_exec_string(program, program_args):
  sys.argv = ["-c"] + program_args
  exec(program)

def mode_exec_module(module_name, program_args):
  spec = importlib.util.find_spec(module_name)
  if spec is None:
    print(f"No module named {module_name}", file=sys.stderr)
    sys.exit(1)
  sys.argv = [spec.origin] + program_args
  sys.path.append(get_script_dir(spec.origin))
  runpy.run_module(module_name, run_name="__main__")

def mode_exec_file(file_path, program_args):
  sys.argv = [file_path] + program_args
  sys.path.append(get_script_dir(file_path))
  runpy.run_path(file_path, run_name="__main__")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog="python-static",
    description="A minimal Python runtime in a single static binary.",
    epilog="These options should be mostly compatible with the original Python CLI."
  )

  parser.add_argument("-c", dest="cmd", action="store", help="run a program passed in as string")
  parser.add_argument("-m", dest="mod", action="store", help="run library module as a script")
  parser.add_argument("-V", "--version", action="store_true", help="print the Python version number and exit")
  parser.add_argument("-q", action="store_true", help="don't print version and copyright messages on interactive startup")
  parser.add_argument("args", nargs="*", action="store", help="arguments to be passed onto the script")

  args = vars(parser.parse_args())
  program_args = args["args"]

  if program_args and not args.get("cmd") and not args.get("mod"):
    exec_file = program_args.pop(0)
  else:
    exec_file = None
  
  if args.get("version"):
    mode_print_version()
  elif args.get("cmd"):
    mode_exec_string(args["cmd"], program_args)
  elif args.get("mod"):
    mode_exec_module(args["mod"], program_args)
  elif exec_file:
    mode_exec_file(exec_file, program_args)
  else:
    #no arguments
    mode_interactive(args.get("q"))