import code
import sys

#trick freeze into including these modules without actually importing them
#the code the if statement will be modified by the build script, and replaced
#by an unreachable import statement
if sys.copyright == "":
  pass #modules_here

if __name__ == "__main__":
  code.interact()