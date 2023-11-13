import code

#trick freeze into including these modules without actually importing them
#the code the if statement will be modified by the build script, and replaced
#by an unreachable import statement
if False:
  pass #modules_here

if __name__ == "__main__":
  code.interact()