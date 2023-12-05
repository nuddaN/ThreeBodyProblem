import numpy as np
from numpy import linalg as LA
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import spiceypy as spice
import datetime


class body:
    
    G=6.6743*10**(-11)          #[m3 kg-1 s-2]

    def __init__(self, x, y, z, vx0, vy0, vz0, mass, simTime):
        
        self.m=mass
        
        self.r=np.zeros((simTime,3))
        self.r[0]=[x,y,z]
        
        self.v=np.zeros((simTime,3))
        self.v[0]=[vx0, vy0, vz0]
        
        self.F=np.zeros((simTime,3))
    
    def computeGravityForce(self,other,simIndx):
        d=(self.r[simIndx-1]-other.r[simIndx-1])
        d_norm=LA.norm(d)
        F=-self.G*self.m*other.m*d/d_norm**3
        return F
    
    def computePosition(self,planets,ts,simIndx):

        for planet in planets:
            if self == planet or self.m==1.98847*10**30:
                continue
            
            self.F[simIndx] = self.F[simIndx] + self.computeGravityForce(planet,simIndx)
            self.v[simIndx] = self.v[simIndx-1] + self.F[simIndx] / self.m * ts
            self.r[simIndx] = self.r[simIndx-1] + self.v[simIndx] * ts




def main():
    m_earth=5.9722*10**24               #[kg] 
    m_sun=1.98847*10**30                #[kg]
    m_moon=7.34767309*10**22            #[kg]
    m_mercury=0.33010*10**24            #[kg]
    ts=60*60*24                            #[s]
    totTime=60*60*24*365#365*2          #[s] 1 year
    timeV=range(0, totTime, ts)         #[s] Time vector


    date_today=datetime.datetime.today()
    date_today=date_today.strftime("%Y-%m-%dT00:00:00") 
    spice.furnsh("C:\\Python\ThreeBodyProblem\\ThreeBodyProblem\\kernels\\lsk\\naif0012.tls")
    spice.furnsh("C:\\Python\\ThreeBodyProblem\\ThreeBodyProblem\\kernels\\spk\\de432s.bsp")
    et_today_midnight=spice.utc2et(date_today)
    earth_sun_distance, earth_sun_light_time=spice.spkgeo(targ=399, et=et_today_midnight,
                                ref="ECLIPJ2000", obs=10)
    earth_sun_distance=earth_sun_distance*1000
    moon_sun_distance, mercury_sun_light_time=spice.spkgeo(targ=301, et=et_today_midnight,
                                ref="ECLIPJ2000", obs=10)
    moon_sun_distance=moon_sun_distance*1000
    mercury_sun_distance, mercury_sun_light_time=spice.spkgeo(targ=199, et=et_today_midnight,
                                ref="ECLIPJ2000", obs=10)
    mercury_sun_distance=mercury_sun_distance*1000

    sun=body(0,0,0,0,0,0,m_sun,len(timeV))
    earth=body(earth_sun_distance[0], earth_sun_distance[1], earth_sun_distance[2],
                earth_sun_distance[3], earth_sun_distance[4], earth_sun_distance[5],
                m_earth,len(timeV))
    moon=body(moon_sun_distance[0], moon_sun_distance[1], moon_sun_distance[2],
                moon_sun_distance[3], moon_sun_distance[4], moon_sun_distance[5],
                m_moon,len(timeV))
    mercury=body(mercury_sun_distance[0], mercury_sun_distance[1], mercury_sun_distance[2],
                mercury_sun_distance[3], mercury_sun_distance[4], mercury_sun_distance[5],
                m_mercury,len(timeV))

    planets=[sun,earth,moon,mercury]

    for i in range(1, len(timeV), 1):
        for planet in planets:
            planet.computePosition(planets,ts,i)

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(earth.r[:,[0]], earth.r[:,[1]], earth.r[:,[2]],label='EARTH')
    ax.plot3D(moon.r[:,[0]], moon.r[:,[1]], moon.r[:,[2]],label='MOON')
    ax.legend()

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(earth.r[:,[0]], earth.r[:,[1]], earth.r[:,[2]],label='EARTH')
    ax.plot3D(moon.r[:,[0]], moon.r[:,[1]], moon.r[:,[2]],label='MOON')
    ax.plot3D(mercury.r[:,[0]], mercury.r[:,[1]], mercury.r[:,[2]],label='MERCURY')
    ax.legend()
  
    x=np.squeeze(np.asarray(earth.r[:,[0]]))
    y=np.squeeze(np.asarray(earth.r[:,[1]]))
    z=np.squeeze(np.asarray(earth.r[:,[2]]))

    x2=np.squeeze(np.asarray(moon.r[:,[0]]))
    y2=np.squeeze(np.asarray(moon.r[:,[1]]))
    z2=np.squeeze(np.asarray(moon.r[:,[2]]))

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    line, = ax.plot(x[0], y[0], z[0])
    line2, = ax.plot(x2[0], y2[0], z2[0])
    ax.legend()
    
    ax.set_xlim3d([min(x), max(x)])
    ax.set_xlabel('X')

    ax.set_ylim3d([min(y), max(y)])
    ax.set_ylabel('Y')

    ax.set_zlim3d([min(z2), max(z2)])
    ax.set_zlabel('Z')

    def update(frame):
        line.set_data_3d(x[:frame],y[:frame],z[:frame])
        line2.set_data_3d(x2[:frame],y2[:frame],z2[:frame])
        return (line)

    ani = animation.FuncAnimation(fig=fig, func=update, frames=365, interval=30)
    plt.show()

main()






