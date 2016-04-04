def fun(num):
    l=len(num)
    tar=[]
    for i in range(l):
        tmp=[j for j in num[i]]
        for j in range(i+1,l):
            x=0
            for k in num[j]:
                if k in tmp:
                    x+=1
            if x==0:
                for k in num[j]:
                    tmp.append(k)
                tar.append(num[i]+num[j])
    return tar[:]

def rec(n,num):
    if n==1:
        return num
    return rec(n/2,fun(num))

def prob(a,b,tar):
    tar[a][b]=0.5

n=8
num=[[i] for i in range(1,n+1)]
x3=rec(8,num)
print (len(x3))
[print (i) for i in x3]
p=[[0]*n]*n
[prob(i,j,p) for i in range(n) for j in range(n) if i!=j]
[print(i) for i in p]
