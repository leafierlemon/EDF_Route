import argparse
from math import dist,sin,cos,pi


def squarel(K,r,_xy,l=0):
    (x,y)=_xy
    
    for k in range(1,K+1):
        d=dist((x,y),(k,0))
        if r<d:
            x=(x-k)*r/d+k
            y=(y-0)*r/d+0
            l+=d-r
    return (K,l,(y,K-x))



def circle4(R,s,r,xy,l=0):
    for k in range(s):
        # print(xy)
        (x,y)=xy
        xy=(x*cos(-pi/2/s)-y*sin(-pi/2/s),
            x*sin(-pi/2/s)+y*cos(-pi/2/s))
        d=dist(xy,(R,0))
        # print(xy)
        if r<d:
            (x,y)=xy
            xy=((x-R)*r/d+(R),
                (y-0)*r/d+0)
            l+=d-r
        # print(xy)
    return (pi/2*R,l,xy)

def circle1(R,K,r,xy,l=0):
    for k in range(K):
        # print(xy)
        (x,y)=xy
        xy=(x*cos(-1/R)-y*sin(-1/R),
            x*sin(-1/R)+y*cos(-1/R))
        d=dist(xy,(R,0))
        # print(xy)
        if r<d:
            (x,y)=xy
            xy=((x-R)*r/d+(R),
                (y-0)*r/d+0)
            l+=d-r
        # print(xy)
    return (K,l,xy)

def mix(Ks,R,r,xy):
    l=0
    (ks,l,xy)=squarel(Ks,r,xy,l)
    (x,y)=xy
    # print(xy)
    xy=(R-x,-y)
    # print(xy)
    (kc,l,xy)=circle4(R,1+2*R,r,xy,l)
    (x,y)=xy
    # print(xy)
    xy=(y,R-x)
    # print(xy)
    return (ks+kc,l,xy)
    

def main(K,R,r,step):
    # print("square")
    # xy=(0,r)
    # for i in range(step):
    #     (k,l,xy)=squarel(K,r,xy)
    # # print("step:"+str(i))
    # # print(" L"+str(l))
    # print(" rate:"+str(l/k))        
    # print(" xy:"+str(xy))
    # print("")
    # print("circle")
    # xy=(K/2,-r)
    # for i in range(step):
    #     (k,l,xy)=circle4(K/2,K,r,xy)
    # # print("step:"+str(i))
    # # print(" L:"+str(l))
    # print(" rate:"+str(l/k))        
    # print(" xy:"+str(xy))
    # xy=(0,r)
    # print("")

    # print("square:0.0 circle:.5")
    # for i in range(step):
    #     (k,l,xy)=mix(K*0//10,K*5//10,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.1 circle:.45")
    # for i in range(step):
    #     (k,l,xy)=mix(K*10//100,K*45//100,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.2 circle:.4")
    # for i in range(step):
    #     (k,l,xy)=mix(K*2//10,K*4//10,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.3 circle:.35")
    # for i in range(step):
    #     (k,l,xy)=mix(K*30//100,K*35//100,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.4 circle:.3")
    # for i in range(step):
    #     (k,l,xy)=mix(K*4//10,K*3//10,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.5 circle:.25")
    # for i in range(step):
    #     (k,l,xy)=mix(K*50//100,K*25//100,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.6 circle:.2")
    # for i in range(step):
    #     (k,l,xy)=mix(K*6//10,K*2//10,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.7 circle:.15")
    # for i in range(step):
    #     (k,l,xy)=mix(K*70//100,K*15//100,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.8 circle:.1")
    # for i in range(step):
    #     (k,l,xy)=mix(K*8//10,K*1//10,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:0.9 circle:.05")
    # for i in range(step):
    #     (k,l,xy)=mix(K*90//100,K*5//100,r,xy)
    # print(" rate:"+str(l/k))        
    # print("")
    # print("square:1.0 circle:.0")
    # for i in range(step):
    #     (k,l,xy)=mix(K*10//10,K*0//10,r,xy)
    # print(" rate:"+str(l/k))        
    # # print(" k"+str(k))
    # # print(" L"+str(l))
    # # print(" rate:"+str(l/k))        
    # # print(" xy:"+str(xy))
    # print("")
    print(f"square:{K-2*R} circle:{R}")
    xy=(0,r)
    for i in range(step):
        (k,l,xy)=mix(K-2*R,R,r,xy)
    print(" rate:"+str(1-l/k))        
    print("")
        



if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("K")
    parser.add_argument("R")
    parser.add_argument("r")
    parser.add_argument("step")
    args=parser.parse_args()

    main(int(args.K),int(args.R),int(args.r),int(args.step))
