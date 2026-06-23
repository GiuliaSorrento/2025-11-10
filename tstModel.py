from model.model import Model

mm = Model()
mm.buildGraph("Santa Cruz Bikes", 7)
n,a = mm.getGraphDetails()
print(n,a)
archi = mm.getTop5Archi()
for aa in archi:
    print(aa)