import numpy as np
from time import sleep

A=1
B=1
screen_width=40
R2=2
R1=1
K2=5
theta_spacing=0.07
phi_spacing=0.02
K1=screen_width*K2*3/(8*(R1+R2))
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")



def render_frame(A,B):
  output=np.full((screen_width,screen_width)," ")
  zbuffer=np.zeros((screen_width,screen_width))
  cosA=np.cos(A)
  cosB=np.cos(B)
  sinA=np.sin(A)
  sinB=np.sin(B)

  t=np.arange(0,2*np.pi,theta_spacing)
  
  p=np.arange(0,2*np.pi,phi_spacing)
  cost=np.cos(t)
  cosp=np.cos(p)
  sint=np.sin(t)
  sinp=np.sin(p)
        

  t1=R2+R1*cost
  t2=R1*cosA*sint
  t3=R1*sinA*sint

  x=(np.outer((cosB*cosp)+(sinA*sinB*sinp),t1)-(t2*sinB)).T
  y=(np.outer((sinB*cosp)-(cosB*sinA*sinp),t1)+(t2*cosB)).T
  z=(K2+(cosA*np.outer(t1,sinp))+(R1*sinA*sint[:, np.newaxis])).T

  ooz=np.reciprocal(z).T

  xp =  (screen_width/2 + K1*ooz*x).astype(int);
  yp =  (screen_width/2 - K1*ooz*y).astype(int);

  n1=(np.outer(cosp,cost)*sinB).T
  n2=cosA*np.outer(cost,sinp)
  n3=sinA*sint
  n5=cosA*sint
  n6=np.outer(cost,sinp)*sinA
  n4=cosB*(n5[:, np.newaxis]-n6)

  L=n1-n2-n3[:, np.newaxis]+n4
  luminance_index = np.clip(np.round(L * 8), 0, len(illumination) - 1).astype(int)
  chars=illumination[luminance_index]
  mask_L=L>=0

  for i in range(90):
    mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  
    zbuffer[xp[i][mask], yp[i][mask]] = ooz[i][mask]
    output[xp[i][mask], yp[i][mask]] = chars[i][mask]
    
  return output
        


def pprint(array: np.ndarray) -> None:
    """Pretty print the frame."""
    print(*[" ".join(row) for row in array], sep="\n")


if __name__ == "__main__":
    for _ in range(screen_width * screen_width):
        A += theta_spacing
        B += phi_spacing
        print("\x1b[2J\x1b[H")
        pprint(render_frame(A, B))
        sleep(0.09)