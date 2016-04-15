from loaddata import loadData
from leaves import leaves
def dist(a,b):
    l=len(a)
    x=0
    for i in range(l):
        x+=(a[i]-b[i])**2
    return x**(0.5)

def avg(a):
    b=[0 for i in range(m)]
    c=0
    for i in a:
        for j in range(m):
            b[j]+=num[i-1][j]*nY[i-1]
        c+=nY[i-1]
    return [i/c for i in b]

if __name__ == '__main__':
    global num,nY,m
    data=loadData('dataset/yeast/yeast-10dobscv-1tra.dat')
    X,Y=data.getData()

    l=len(X)
    m=data.getFeature()
    k=data.getK()
    num=[[0 for j in range(m)] for i in range(k)]
    nY=[0 for i in range(k)]
    for i in range(l):
        for j in range(m):
            num[Y[i]][j]+=X[i][j]
            nY[Y[i]]+=1
    for i in range(k):
        for j in range(m):
            num[i][j]/=nY[i]
    dst=[[0 for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(k):
            dst[i][j]=dist(num[i],num[j])
        print(dst[i])

    lv=leaves(k).getAll()
    tmp=[]
    for i in lv:
    #for i in [[1, 8, 4, 5, 2, 3, 6, 7, 9, 10],[1, 9, 4, 5, 2, 3, 6, 7, 8, 10],[1, 2, 9, 10, 3, 4, 5, 6, 7, 8]]:
        x=[dist(avg([i[j]]),avg([i[j+1]])) for j in range(0,k,2)]
        y=0
        for j in x: y+=j
        tmp.append((i,y/5))
        #print(i,dist(avg(a),avg(b)))

    tmp=sorted(tmp,key=lambda x: (x[1],x[0]))
    [print(i) for i in tmp]
