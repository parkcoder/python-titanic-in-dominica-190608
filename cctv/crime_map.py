from cctv.data_reader import DataReader
import folium

class CrimeMap:
    def __init__(self):
        self.dr = DataReader()

    def hook(self):
        self.create_map()

    def create_map(self):
        print('---------1 ---------')
        self.dr.context = './data/'
        self.dr.fname = 'saved/police_norm.csv'
        pn = self.dr.csv_to_dframe()
        print(pn)
        self.dr.fname = 'geo_simple.json'
        geo_str = self.dr.json_load()
        map = folium.Map(location=[37.5502, 126.982],
                         zoom_start=12,
                         tiles='Stamen Toner')
        map.choropleth(
            geo_data=geo_str,
            name='choropleth',
            data=tuple(zip(pn['구별'], pn['범죄'])),
            key_on='feature.id',
            fill_color='PuRd'
        )
        map.save(self.dr.context+'saved/seoul_crime_map.html')

