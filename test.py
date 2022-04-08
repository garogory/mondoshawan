import folium
import gpxpy
import numpy as np
from scipy.signal import argrelextrema, find_peaks

def mean(points):
    return sum(points)/len(points)

def conversion(sec):
   sec_value = sec % (24 * 3600)
   hour_value = sec_value // 3600
   sec_value %= 3600
   minu = sec_value // 60
   sec_value %= 60
   return hour_value, minu, sec_value

def gpxify(filename):
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    return gpx

class myRun(object):
    def __init__(self, gpx):
        self.gpx = gpx
        self.data = {}
        self.latitudes = []
        self.longitudes = []
        self.distances2d = []
        self.distances3d = []
        self.elevations = []
        self.maxima = []
        self.peaks = []
        self.maxpos = []
        self.distances2d.append(0.0)
        self.distances3d.append(0.0)
        self.compute_fields()
        self.compute_integrals()

    def compute_fields(self):
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    self.latitudes.append(point.latitude)
                    self.longitudes.append(point.longitude)
                    self.elevations.append(point.elevation)
                    try:
                        self.distances2d.append(point.distance_2d(tota))
                        self.distances3d.append(point.distance_3d(tota))
                    except:
                        pass
                    tota = point

    def compute_integrals(self):
        self._min_alt()
        self._max_alt()
        self._up_hill()
        self._down_hill()
        self._duration()
        self._distance_2D()
        self._distance_3D()
        self._latitude()
        self._longitude()
        self._elevation()
        self._splits_2D()
        self._splits_3D()
        self._maxima()
        self._peaks()
        self._maxpos()

    def _maxima(self):
        key = "maximas"
        peaks, _ = find_peaks(self.elevations, distance=10)
        self.maxima = [[peak, self.elevations[peak]] for peak in peaks]
        self.data[key] = self.maxima

    def get_dist(self, index):
        sumdist = 0.0
        for item in self.distances3d[:index+1]:
             sumdist += item
        return sumdist
    def _peaks(self):
        key = "peaks"
        peaks, _ = find_peaks(self.elevations, distance=500)
        self.peaks = [[self.latitudes[peak], self.longitudes[peak]] for peak in peaks]
        self.data[key] = self.peaks

    def _maxpos(self):
        key = "maxpos"
        peaks, _ = find_peaks(self.elevations, distance=500)

        self.maxpos = [[self.get_dist(peak), self.elevations[peak]] for peak in peaks]
        self.data[key] = self.maxpos

    def _min_alt(self):
        key = "min_alt"
        self.data[key] = self.gpx.get_elevation_extremes().minimum

    def _max_alt(self):
        key = "max_alt"
        self.data[key] = self.gpx.get_elevation_extremes().minimum

    def _up_hill(self):
        key = "up_fill"
        self.data[key] = self.gpx.get_uphill_downhill().uphill

    def _down_hill(self):
        key = "down_fill"
        self.data[key] = self.gpx.get_uphill_downhill().downhill

    def _duration(self):
        key = "duration"
        h, m, s = conversion(gpx.get_duration())
        self.data[key] = {'h':h, 'm': m, 's':s}

    def _distance_2D(self):
        key = "distance_2D"
        self.data[key] = self.gpx.length_2d()

    def _distance_3D(self):
        key = "distance_3D"
        self.data[key] = self.gpx.length_3d()

    def _latitude(self):
        key = "latitude"
        self.data[key] = self.latitudes

    def _longitude(self):
        key = "longitude"
        self.data[key] = self.longitudes

    def _elevation(self):
        key = "elevation"
        self.data[key] = self.elevations

    def _splits_2D(self):
        key = "splits_2D"
        self.data[key] = self.distances2d

    def _splits_3D(self):
        key = "splits_3D"
        self.data[key] = self.distances3d

class myMap(object):
    def __init__(self, myrun):
        xcenter = mean(myrun.latitudes)
        ycenter = mean(myrun.longitudes)
        self.m = folium.Map(location=[xcenter, ycenter],
                            zoom_start=13)
        self.run = myrun
        self.add_start()
        self.add_max()
        self.add_end()
        self.add_trace()

    def add_max(self):
        msg = "Max "
        tooltip = "Max" 

        for item in self.run.peaks:
            init = [item[0], item[1]]
            folium.Marker(init,
                          popup=msg,
                          tooltip=tooltip,
                          icon=folium.Icon(color='blue', icon='info-sign')).add_to(self.m)

    def add_start(self):
        msg = "Start "
        tooltip = "Start" 
        init = [self.run.latitudes[0], self.run.longitudes[0]]
        folium.Marker(init, 
                      popup=msg,
                      tooltip=tooltip,
                      icon=folium.Icon(color='green', icon='play', prefix='fa')).add_to(self.m)

    def add_end(self):
        msg = "End "
        tooltip = "End" 
        end = [self.run.latitudes[-1], self.run.longitudes[-1]]
        folium.Marker(end,
                      popup=msg,
                      tooltip=tooltip,
                      icon=folium.Icon(color='red', icon='stop', prefix='fa')).add_to(self.m)

    def add_trace(self):
        loc = [(item, item2) for item, item2 in zip(self.run.latitudes, self.run.longitudes)]
        folium.PolyLine(loc,
                        color='black',
                        weight=8,
                        opacity=0.8).add_to(self.m)
    def save(self, output):
        self.m.save(output)

def plot_deniv(run):
    
    import plotly.graph_objects as go
    import numpy as np
    
    fig = go.Figure()
    elevations = run.elevations 
    maxpos=  run.maxpos
    xdata = [0.0]
    for item in run.distances3d:
        previous = xdata[len(xdata)-1]
        xdata.append(previous+item)
    print(maxpos)
    xdata2 = [item[0] for item in maxpos]
    ydata = [item[1] for item in maxpos]
    fig.add_trace(go.Scatter(
        x=xdata[:-1],
        y=elevations,
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Deniv',
    ))
    for x, y in zip(xdata2, ydata):
        fig.add_annotation(
            x=x, y=y)
#    fig.update_traces(mode='lines')
    fig.show()

if __name__ == "__main__":
    filename = "Semi_marathon_trail_de_la_Vanoise.gpx"
    gpx = gpxify(filename)
    myrun = myRun(gpx)
    mymap = myMap(myrun)
    mymap.save('index.html')
    plot_deniv(myrun)
