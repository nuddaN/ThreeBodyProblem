import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


m_earth=5.9722*10**24   #[kg] 
m_sun=1.98847*10**30    #[kg]
r=149597870700          #[m]
G=6.6743*10**(-11)      #[m3 kg-1 s-2]


totTime=60*60*24*365*2
ts=60*60*24
theta0=0
x0=r
y0=0

theta=[]
theta.append(theta0)

x=[]
y=[]

x.append(x0)
y.append(y0)

ax=[]
ay=[]

vx=[]
vy=[]

vx.append(0)
vy.append(-30000)

timeV=range(0, totTime, ts)

for i in range(1, len(timeV), 1):#

    ax.append(-G*m_sun/(math.sqrt(x[i-1]**2+y[i-1]**2)**2)*math.cos(theta[i-1]))
    ay.append(-G*m_sun/(math.sqrt(x[i-1]**2+y[i-1]**2)**2)*math.sin(theta[i-1]))
    vx.append(vx[i-1] + ax[i-1]*ts)
    vy.append(vy[i-1] + ay[i-1]*ts)
    x.append(x[i-1]+vx[i]*ts)
    y.append(y[i-1]+vy[i]*ts)
    theta.append(math.atan2(y[i],x[i]))

# plt.figure()
# plt.plot(timeV,theta)
# plt.suptitle('Theta')
# plt.show()

plt.figure()
plt.scatter(x,y)
plt.suptitle('Earth Position')
plt.show()

# plt.figure()
# plt.plot(timeV,vx)
# plt.plot(timeV,vy)
# plt.suptitle('Vx Speed')
# plt.show()


# plt.figure()
# plt.scatter(timeV,ax)
# plt.show()
# plt.suptitle('Ax Acceleration')

fig, ax = plt.subplots()
scat = ax.scatter(x[0], y[0], c="b", s=5)
line2 = ax.plot(x[0], y[0])[0]
ax.set(xlim=[min(x), max(x)], ylim=[min(y), max(y)], xlabel='x', ylabel='y')
ax.legend()


def update(frame):
    # for each frame, update the data stored on each artist.
    x_ani = x[:frame]
    y_ani = y[:frame]
    # update the scatter plot:
    data = np.stack([x_ani, y_ani]).T
    scat.set_offsets(data)
    # update the line plot:
    line2.set_xdata(x_ani[:frame])
    line2.set_ydata(y_ani[:frame])
    return (scat, line2)


ani = animation.FuncAnimation(fig=fig, func=update, frames=365*2, interval=30)
plt.show()
