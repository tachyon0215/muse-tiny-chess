import sys
V=[0,100,320,330,500,900,0]
PST={
1:[0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10,-5,5,0,0,0,20,20,0,0,0,10,10,20,30,30,20,10,10,20,20,30,40,40,30,20,20,50,50,50,50,50,50,50,50,0,0,0,0,0,0,0,0],
2:[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30,-30,5,15,20,20,15,5,-30,-30,0,10,15,15,10,0,-30,-40,-20,0,0,0,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
3:[-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10,-10,5,5,10,10,5,5,-10,-10,0,5,10,10,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20],
4:[0,-5,5,10,10,5,-5,0,-5,0,0,0,0,0,0,-5,5,10,10,15,15,10,10,5,-5,0,10,15,15,10,0,-5,-5,0,5,10,10,5,0,-5,-5,0,0,5,5,0,0,-5,5,10,10,10,10,10,10,5,0,0,0,0,0,0,0,0],
5:[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,5,0,0,5,0,-10,-10,5,5,5,5,5,5,-10,0,0,5,5,5,5,0,-5,0,5,5,5,5,5,5,0,10,10,10,10,10,10,10,10,10,20,20,20,20,20,20,20,-20,-10,-10,-5,-5,-10,-10,-20],
6:[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-30,-30,-40,-40,-30,-30,-30,-20,-30,-30,-30,-30,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]}
import random
_R=random.Random(20261123)
Z=[[_R.getrandbits(64) for _ in range(13)] for _ in range(64)]
ZS=_R.getrandbits(64);ZC=[_R.getrandbits(64) for _ in range(16)];ZE=[_R.getrandbits(64) for _ in range(65)]
KN=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
KG=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
DG=[(-1,-1),(-1,1),(1,-1),(1,1)];OR=[(-1,0),(1,0),(0,-1),(0,1)]
class B:
 __slots__=('b','t','c','e','h','k','z')
 def __init__(s,b,t,c,e,h):
  s.b=b;s.t=t;s.c=c;s.e=e;s.h=h;s.k=[0,0]
  for i,p in enumerate(b):
   if p==6:s.k[0]=i
   elif p==-6:s.k[1]=i
  z=0
  for i,p in enumerate(b):
   if p:z^=Z[i][p+6]
  if t<0:z^=ZS
  z^=ZC[c]^ZE[e+1];s.z=z
def parse(fen):
 f=fen.split();b=[0]*64
 for ri,row in enumerate(f[0].split('/')):
  r=7-ri;fi=0
  for ch in row:
   if ch.isdigit():fi+=int(ch)
   else:
    p='pnbrqk'.index(ch.lower())+1;b[r*8+fi]=p if ch.isupper() else -p;fi+=1
 c=0
 if len(f)>2:
  if 'K' in f[2]:c|=1
  if 'Q' in f[2]:c|=2
  if 'k' in f[2]:c|=4
  if 'q' in f[2]:c|=8
 e=-1
 if len(f)>3 and f[3]!='-':e=(int(f[3][1])-1)*8+'abcdefgh'.index(f[3][0])
 h=int(f[4]) if len(f)>4 else 0
 return B(b,1 if f[1]=='w' else -1,c,e,h)
def A(bd,sq,by):
 f=sq&7;r=sq>>3
 pr=r-by
 if 0<=pr<8:
  for df in(-1,1):
   pf=f+df
   if 0<=pf<8 and bd[pr*8+pf]==by:return 1
 for df,dr in KN:
  nf,nr=f+df,r+dr
  if 0<=nf<8 and 0<=nr<8 and bd[nr*8+nf]==2*by:return 1
 for df,dr in KG:
  nf,nr=f+df,r+dr
  if 0<=nf<8 and 0<=nr<8 and bd[nr*8+nf]==6*by:return 1
 for dirs,ts in((DG,(3,5)),(OR,(4,5))):
  for df,dr in dirs:
   nf,nr=f+df,r+dr
   while 0<=nf<8 and 0<=nr<8:
    p=bd[nr*8+nf]
    if p:
     if p*by>0 and abs(p) in ts:return 1
     break
    nf+=df;nr+=dr
 return 0
def gen(bd,caponly=0):
 b=bd.b;t=bd.t;ms=[]
 for i,p in enumerate(b):
  if p*t<=0:continue
  a=abs(p);f=i&7;r=i>>3
  if a==1:
   d=8*t;one=i+d
   if not caponly and not b[one]:
    if (one>>3) in(0,7):
     for pr in(5,2,3,4):ms.append((i,one,pr))
    else:ms.append((i,one,0))
    two=i+2*d
    if r==(1 if t>0 else 6) and not b[two]:ms.append((i,two,0))
   for df in(-1,1):
    nf=f+df
    if 0<=nf<8:
     to=one+df;q=b[to]
     if q*t<0:
      if (to>>3) in(0,7):
       for pr in(5,2,3,4):ms.append((i,to,pr))
      else:ms.append((i,to,0))
     elif to==bd.e:ms.append((i,to,9))
  elif a in(2,6):
   for df,dr in(KN if a==2 else KG):
    nf,nr=f+df,r+dr
    if 0<=nf<8 and 0<=nr<8:
     to=nr*8+nf;q=b[to]
     if q*t<=0 and(not caponly or q*t<0):ms.append((i,to,0))
  else:
   dirs=DG if a==3 else(OR if a==4 else KG)
   for df,dr in dirs:
    nf,nr=f+df,r+dr
    while 0<=nf<8 and 0<=nr<8:
     to=nr*8+nf;q=b[to]
     if q*t>0:break
     if not caponly or q*t<0:ms.append((i,to,0))
     if q:break
     nf+=df;nr+=dr
 if not caponly:
  c=bd.c
  if t>0:
   if c&1 and not b[5] and not b[6] and b[7]==4 and not A(b,4,-1) and not A(b,5,-1) and not A(b,6,-1):ms.append((4,6,7))
   if c&2 and not b[3] and not b[2] and not b[1] and b[0]==4 and not A(b,4,-1) and not A(b,3,-1) and not A(b,2,-1):ms.append((4,2,7))
  else:
   if c&4 and not b[61] and not b[62] and b[63]==-4 and not A(b,60,1) and not A(b,61,1) and not A(b,62,1):ms.append((60,62,7))
   if c&8 and not b[59] and not b[58] and not b[57] and b[56]==-4 and not A(b,60,1) and not A(b,59,1) and not A(b,58,1):ms.append((60,58,7))
 return ms
def make(bd,m):
 fr,to,pr=m;b=bd.b[:];p=b[fr];t=bd.t;cap=b[to]
 b[fr]=0;h=bd.h+1
 if abs(p)==1 or cap or pr==9:h=0
 if pr==9:b[to-8*t]=0
 if pr and pr not in(7,9):b[to]=pr*t
 elif pr==7:
  b[to]=p
  if to==6:b[5]=4;b[7]=0
  elif to==2:b[3]=4;b[0]=0
  elif to==62:b[61]=-4;b[63]=0
  else:b[59]=-4;b[56]=0
 else:b[to]=p
 c=bd.c
 if abs(p)==6:c&=~(3 if t>0 else 12)
 if fr==7 or to==7:c&=~1
 if fr==0 or to==0:c&=~2
 if fr==63 or to==63:c&=~4
 if fr==56 or to==56:c&=~8
 e=fr+8*t if abs(p)==1 and abs(to-fr)==16 else -1
 return B(b,-t,c,e,h)
def ok(bd,m):
 nb=make(bd,m);return not A(nb.b,nb.k[0] if bd.t>0 else nb.k[1],-bd.t)
def legal(bd):
 return[m for m in gen(bd)if ok(bd,m)]
def ev(bd):
 s=0;b=bd.b;bp=0
 for i,p in enumerate(b):
  if not p:continue
  a=abs(p);sq=i if p>0 else(i^56)
  v=V[a]+PST[a][sq]
  if a==3:bp+=1 if p>0 else -1
  s+=v if p>0 else -v
 if bp>=2:s+=30
 if bp<=-2:s-=30
 return s*bd.t
TT={};nodes=0;BUDGET=24000
def qs(bd,al,be,ply):
 global nodes
 nodes+=1;stand=ev(bd)
 if nodes>BUDGET:return stand
 inc=A(bd.b,bd.k[0] if bd.t>0 else bd.k[1],-bd.t)
 if not inc:
  if stand>=be:return be
  if stand>al:al=stand
 ms=gen(bd,0 if inc else 1)
 ms=[m for m in ms if ok(bd,m)]
 if inc and not ms:return -100000+ply
 def key(m):
  q=bd.b[m[1]];return V[abs(q)]*10-abs(bd.b[m[0]]) if q else(900 if m[2]==9 else 800)
 ms.sort(key=key,reverse=True)
 for m in ms:
  sc=-qs(make(bd,m),-be,-al,ply+1)
  if sc>=be:return be
  if sc>al:al=sc
 return al
def make_null(bd):
 nb=B(bd.b[:],-bd.t,bd.c,-1,bd.h);return nb
def search(bd,depth,al,be,ply):
 global nodes
 if bd.h>=100:return 0
 if depth<=0:return qs(bd,al,be,ply)
 nodes+=1
 if nodes>BUDGET:return qs(bd,al,be,ply)
 ent=TT.get(bd.z)
 tt=None
 if ent and ent[0]>=depth:
  if ent[2]==0:return ent[1]
  if ent[2]==1 and ent[1]>al:al=ent[1]
  elif ent[2]==2 and ent[1]<be:be=ent[1]
  if al>=be:return ent[1]
 if ent:tt=ent[3]
 inc=A(bd.b,bd.k[0] if bd.t>0 else bd.k[1],-bd.t)
 ms=gen(bd)
 ms=[m for m in ms if ok(bd,m)]
 if not ms:return -100000+ply if inc else 0
 if depth>=3 and not inc and be<90000:
  evv=ev(bd)
  if evv>=be:
   sc=-search(make_null(bd),depth-3,-be,-be+1,ply+1)
   if sc>=be:return be
 kl=()
 def key(m):
  if m==tt:return 1<<30
  q=bd.b[m[1]]
  if q or m[2]==9:return(1<<20)+(V[abs(q)]*10-abs(bd.b[m[0]]) if q else 900)
  return 0
 ms.sort(key=key,reverse=True)
 best=-10**9;bm=None;flag=2
 mi=0
 for m in ms:
  red=1 if(depth>=3 and mi>=3 and not bd.b[m[1]] and not inc and m[2] in(0,7))else 0
  sc=-search(make(bd,m),depth-1-red,-be,-al,ply+1)
  if red and sc>al:sc=-search(make(bd,m),depth-1,-be,-al,ply+1)
  mi+=1
  if sc>best:best=sc;bm=m
  if sc>al:
   al=sc;flag=0
   if al>=be:
    flag=1
    break
 TT[bd.z]=(depth,best,flag,bm)
 return best
def fenkey(bd):
 return(tuple(bd.b),bd.t,bd.c,bd.e)
def choose(fen,hist=()):
 global nodes
 bd=parse(fen);ms=legal(bd)
 if len(ms)==1:return uci(ms[0])
 TT.clear();best=ms[0];total=0;depth=1
 while depth<=10:
  nodes=0;al=-10**9;cb=None;scored=[]
  for m in ms:
   nb=make(bd,m);sc=-search(nb,depth-1,-10**9,10**9,1)
   if sc>-40 and fenkey(nb)in hist:sc-=70
   scored.append((sc,m))
   if sc>al:al=sc;cb=m
   if nodes>11000:break
  total+=nodes
  if cb and len(scored)==len(ms):best=cb
  elif cb and depth==1:best=cb
  if len(scored)<len(ms)or total>15000:break
  scored.sort(key=lambda x:-x[0]);ms=[m for _,m in scored]
  if al>90000:break
  depth+=1
 return uci(best)
def uci(m):
 s='abcdefgh'[m[0]&7]+str((m[0]>>3)+1)+'abcdefgh'[m[1]&7]+str((m[1]>>3)+1)
 if m[2] and m[2] not in(7,9):s+='nbrq'[m[2]-2]
 elif m[2]==5:s+='q'
 return s

import json,os,urllib.request,urllib.error
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("no env")
def post(p,b):
 r=urllib.request.Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with urllib.request.urlopen(r)as x:return json.load(x)
while True:
 g=post("/game",{})
 if g["status"]=="done":break
 hist=set()
 while g["status"]=="your_move":
  _bd=parse(g["fen"]);hist.add(fenkey(_bd))
  mv=choose(g["fen"],hist)
  if mv not in g["legal_moves"]:mv=g["legal_moves"][0]
  g=post("/move",{"game":g["game"],"move":mv})
