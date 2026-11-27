import argparse
from math import dist,sin,cos,pi

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import json
# from distutils.util import strtobool

# 左
def area1(K,R,current,add=1):
    (Kx,Ky)=K
    rest=0
    if current+add>Ky-2*R:
        c=Ky-2*R
        rest=current+add-c
        p=(0,R)
    else:
        c=current+add
        p=(0,Ky-R-c)
    return p,c,rest

# 左下
def area2(K,R,current,add=1):
    rest=0
    if current+add>pi*R/2:
        c=pi*R/2
        rest=current+add-c
        p=(R,0)
    else:
        c=current+add
        p=(R-R*cos(c/R),R-R*sin(c/R))
    return p,c,rest

# 下
def area3(K,R,current,add=1):
    (Kx,Ky)=K
    rest=0
    if current+add>Kx-2*R:
        c=Kx-2*R
        rest=current+add-c
        p=(K[0]-R,0)
    else:
        c=current+add
        p=(R+c,0)
    return p,c,rest

# 右下
def area4(K,R,current,add=1):
    rest=0
    if current+add>pi*R/2:
        c=pi*R/2
        rest=current+add-c
        p=(K[0],R)
    else:
        c=current+add
        p=(K[0]-R+R*sin(c/R),R-R*cos(c/R))
    return p,c,rest

# 右
def area5(K,R,current,add=1):
    (Kx,Ky)=K
    rest=0
    if current+add>Ky-2*R:
        c=Ky-2*R
        rest=current+add-c
        p=(K[0],K[1]-R)
    else:
        c=current+add
        p=(K[0],R+c)
    return p,c,rest

# 右上
def area6(K,R,current,add=1):
    rest=0
    if current+add>pi*R/2:
        c=pi*R/2
        rest=current+add-c
        p=(K[0]-R,K[1])
    else:
        c=current+add
        p=(K[0]-R+R*cos(c/R),K[1]-R+R*sin(c/R))
    return p,c,rest

# 上
def area7(K,R,current,add=1):
    (Kx,Ky)=K
    rest=0
    if current+add>Kx-2*R:
        c=Kx-2*R
        rest=current+add-c
        p=(R,K[1])
    else:
        c=current+add
        p=(K[0]-R-c,K[1])
    return p,c,rest

# 左上
def area8(K,R,current,add=1):
    rest=0
    if current+add>pi*R/2:
        c=pi*R/2
        rest=current+add-c
        p=(0,K[1]-R)
    else:
        c=current+add
        p=(R-R*sin(c/R),K[1]-R+R*cos(c/R))
    return p,c,rest

# エリア関数リスト
f=(area8,area1,area2,area3,area4,area5,area6,area7)

# PQの移動
def move(K,ps,qs,vflag=True):
    ps,qs=moveQ(ps,qs)
    ps=moveP(K,ps,vflag)
    return ps,qs

# Q移動と距離計算
def moveQ(ps,qs):
    for iq,q in enumerate(qs):
        stop=True
        if "stop" in q:
            stop=q["stop"]
        # QからPへの距離
        ds=[dist(p["xy"],q["xy"]) for p in ps]
        for ip,d in enumerate(ds):
            # dmin更新
            ps[ip]["dmin"]=min(ps[ip]["dmin"],d)

        # Qからの[最短P,その距離]
        ip,d = min(enumerate(ds),key=lambda x:x[1])
        pxy=ps[ip]["xy"]
        qxy=qs[iq]["xy"]
        # 移動距離
        l=max(min(d-q["r"],q["v"]),0) if stop else q["v"]
        # 移動処理
        if 0<d and 0<l:
            qs[iq]["xy"]=[(pxy[0]-qxy[0])*l/d+qxy[0],(pxy[1]-qxy[1])*l/d+qxy[1]]
        if "v_add" in q:
            q["xy"]=[xy+add for xy,add in zip(q["xy"],q["v_add"])]
        # 攻撃スコア加算
        ps[ip]["A"]+=(q["v"]-l) if stop else 1 if d<q["r"] else 0
    return ps,qs

# P移動
def moveP(K,ps,vflag):
    for i,p in enumerate(ps):
        vp=0
        # P移動有り判定
        if vflag:
            # P待機判定
            if p["wait"]>0:
                p["wait"]-=1
            else:
                vp=p["v"]

        # エリア位置計算
        while True:
            (p["xy"],p["c"],rest)=f[p["area"]%8](K,p["R"],p["c"],vp)
            # エリアをまたぐ場合
            if rest!=0:
                p["area"]=(p["area"]+1)%8
                p["c"]=rest
                vp=0
                continue
            break
        ps[i]=p
    return ps

    
def main(filename,plot=False,save=False,savegif=False):

    # 設定ファイルロード
    with open(filename, mode='r') as fi:
        jl = json.load(fi)
    K=jl["map"]
    ps=jl["ps"]
    for p in ps:
        p["c"]=p["offset"]
        p["A"]=0
        p["dmin"]=K[0]
        p["xy"]=[0,0]
    qs=jl["qs"]
    time=jl["time"]
    video=jl["video"]

    # プロット用
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    # fig, ax = plt.subplots() 
    ax.set_xlim(-0.1*K[0],1.1*K[0])
    ax.set_ylim(-0.1*K[1],1.1*K[1])
    ax.grid()
    ax.plot([0,K[0],K[0],0,0],[0,0,K[1],K[1],0],"-m")

    # initialize
    # A=0 # 攻撃スコア
    ims=[] # プロットイメージ
    counter=0 # プロットカウンター
    d=K[0]
    # offsetの反映
    ps=moveP(K,ps,False)
    # (ps,qs,A,d)=move(K,ps,qs,A,d) # offset(c)の反映
    routePs=[[[],[]] for p in ps]
    routeQs=[[[],[]] for q in qs]
    p0xy0=ps[0]["xy"]
    loopCounter=0
    loopLimit=time["loopLimit"] if "loopLimit" in time else 0

    # プロット
    def plotPQ(ps,qs):

        for ip,p in enumerate(ps):
            routePs[ip][0].append(p["xy"][0])
            routePs[ip][1].append(p["xy"][1])
        for iq,q in enumerate(qs):
            routeQs[iq][0].append(q["xy"][0])
            routeQs[iq][1].append(q["xy"][1])

        # pl=ax.plot([routePs[ip][0][0]],[routePs[ip][1][0]],"bo")
        # PQ初期位置
        pl=ax.plot([routeP[0][0] for routeP in routePs],[routeP[1][0] for routeP in routePs],"bo")
        pl+=ax.plot([routeQ[0][0] for routeQ in routeQs],[routeQ[1][0] for routeQ in routeQs],"ro")

        # PQ軌跡
        for routeP in routePs:
            pl+=ax.plot(routeP[0],routeP[1],"b-")
        for routeQ in routeQs:
            pl+=ax.plot(routeQ[0],routeQ[1],"r-")
        # pl+=ax.plot([p[0]],[p[1]],"bo")
        # PQ現在位置
        pl+=ax.plot([p["xy"][0] for p in ps],[p["xy"][1] for p in ps],"bo")
        pl+=ax.plot([q["xy"][0] for q in qs],[q["xy"][1] for q in qs],"ro")
        ims.append(pl)

    # if 0==time["ignore"]:
    #     plotPQ(ps,qs)
    #     i+=1

    # PQ移動 無視分
    for _ in range(time["ignore"]):
        (ps,qs)=move(K,ps,qs)

    # 移動量などリセット
    for p in ps:
        p["A"]=0
        p["dmin"]=K[0]
    p0xy0=ps[0]["xy"]

    # PQ移動 計算分
    for _ in range(time["count"]):
        # プロット
        if 0 == counter%video["speed"]:
            plotPQ(ps,qs)
        counter+=1

        # PQ移動処理
        p0xyPre=ps[0]["xy"]
        (ps,qs)=move(K,ps,qs)
        p0xyPost=ps[0]["xy"]

        # 周回判定
        if pointBetween(p0xy0,p0xyPre,p0xyPost) and _>1:
            # print(p0xy0,p0xyPre,p0xyPost)
            loopCounter+=1
        if loopLimit>0 and loopCounter>=loopLimit:
            break


    # 結果出力
    for ip,p in enumerate(ps):
        print(f"P{ip}")
        print(f"PQ最小距離：{p['dmin']}")
        print(f"攻撃される量 ：{p['A']}")
        print(f"攻撃率[/s]：{p['A']/counter}")
        print()
    print(f"時間[s] 　：{counter}")

    # for q in qs:
    #     print(f"{q['xy']}")

    # プロット表示・保存
    if plot:
        plt.show()
    if filename[-5:]==".json":
        filename=filename[:-5]
    if save:
        anim = ArtistAnimation(fig, ims,interval=20)
        anim.save(f"{filename}.mp4", writer="ffmpeg", dpi=80)
    if savegif:
        anim = ArtistAnimation(fig, ims,interval=20)
        anim.save(f"{filename}.gif",writer="pillow")
    plt.close()


def pointBetween(target,pre,post):
    for i in range(2):
        if pre[i]==target[i] or post[i]==target[i]:
            continue
        if ((pre[i]>target[i]) ^ ((post[i]>target[i]))):
            continue
        return False
    return True

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("setting_json",help="設定JSON")
    parser.add_argument("-p",'--plot', action='store_true',help="プロット表示")
    parser.add_argument("-s",'--save', action='store_true',help="動画保存(MP4)")
    parser.add_argument("-sg",'--savegif', action='store_true',help="動画保存(GIF)")
    args=parser.parse_args()

    main(args.setting_json,args.plot,args.save,args.savegif)

