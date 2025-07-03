#tetas
# git submodule add https://github.com/Boots-bots/Settings.git settings
# git submodule status
# git submodule update --init --recursive
# git submodule update --remote --merge

# conversores
# comversor pot a %
def por(x):
    return x*100/255

# conversor de pixeles a cm
L = 72 #cm longitud del tubo ±1
resolución = 590 # pixeles en el eje x
def pixacm(x):
  return x*L/resolución
kc = 3.5
Tc = 5
print(pixacm(5)) 