import re
class loadData:
    def __init__(self,fname='in.dat'):
        try:
            self.file=open(fname,'r')
        except:
            print("load file error")
        self.cls={}
        self.X=[]
        self.Y=[]
        self.k=2

    def load(self):
        for str in self.file:
            if re.match('@\w*',str)!=None:
                if re.match('@attribute \w*{',str)!=None:
                    st=str.index('{')+1
                    j=0
                    for i in re.split(',',str[st:-2]):
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
    dat=loadData('dataset/yeast/yeast-10dobscv-1tra.dat')
    #dat=loadData('dataset/led7digit/led7digit-10dobscv-1tra.dat')
    dat.load()
    #dat.show()
