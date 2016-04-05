import re
class loadData:
    def __init__(self,fname='in.dat'):
        self.file=open(fname,'r')
        self.cls={}
        self.X=[]
        self.Y=[]
        self.k=2

    def load(self):
        for str in self.file:
            if re.match('@\w*',str)!=None:
                if re.match('@attribute Class',str)!=None:
                    j=0
                    for i in re.split(',',str[17:-2]):
                        self.cls[i]=j
                        j+=1
                    #print (self.cls)
                    self.k=j;
            else:
                #print (str)
                tmp=re.split(", ",str[:-1])
                self.X.append([float(i) for i in tmp[:-1]])
                self.Y.append(self.cls[tmp[-1]])

    def show(self):
        n=len(self.X)
        [print(self.X[i],self.Y[i]) for i in range(n)]

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getK(self):
        return self.k    

if __name__=='__main__':
    dat=loadData()
    dat.load()
    dat.show()
