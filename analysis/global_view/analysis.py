import requests
import argparse
import pandas as pd
import json
import re
import folium
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib import colors

ip_info_properties = ["ip",\
                      "hostname",\
                      "city",\
                      "region",\
                      "country",\
                      "loc",\
                      "org",\
                      "postal",\
                      "timezone"]

class MPTCPHostsAnalysis:
    def __init__(self, src_file):
        self.src_file = src_file
        self.regex = re.compile(r"{(.*?)}", re.DOTALL)
        self.hosts_info_df = pd.DataFrame(columns=ip_info_properties)
    
    def load_hosts_from_csv(self):
        self.hosts_info_df = pd.read_csv(self.src_file)
        print(self.hosts_info_df)
    
    def load_hosts_from_json(self):
        with open(self.src_file, "r") as file:
            json_data = file.read()
        
        parse_result = self.regex.findall(json_data)
        json_data_list = ['{' + json_str + '}' for json_str in parse_result]

        for json_data in json_data_list:
            #print(json_data)
            #print(json.loads(json_data))
            #print(type(json_data))
            #print(json_data)
            data = json.loads(json_data)
            #print(data)
            self.hosts_info_df = self.hosts_info_df._append(json.loads(json_data), ignore_index=True)
        
        print(self.hosts_info_df)
        self.hosts_info_df.to_csv("hosts_info.csv", index=False)
    
    def output_top10(self):
        # extract top 10 values for column [country, region, city, org]
        df = self.hosts_info_df
        top_values = {}
        for column in df.columns:
            if column in ["country", "region", "city", "org"]:
                top_values[column] = df[column].value_counts().head(10)
        
        # aggreate to one dataframe
        top_values_df = pd.DataFrame()
        for column, values in top_values.items():
            # transfer count to percentage and add to index
            top_values_df[column] = values.index
            top_values_df[column + "_percentage"] = values.values / len(df)
            # transfer to percentage with %
            top_values_df[column + "_percentage"] = top_values_df[column + "_percentage"].apply(lambda x: "%.2f%%" % (x * 100))
        
        # save to latex
        print(top_values_df.to_latex(index=False))

        # output as table in pdf
        doc = SimpleDocTemplate("top10.pdf", pagesize=letter)
        elements = []
        data = top_values_df.values.tolist()
        table = Table(data)
        style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                           ('VALIGN',(0,0),(0,-1),'TOP'),
                           ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ])
        elements.append(table)
        doc.build(elements)

    def loadfile(self):
        if (self.src_file.endswith(".csv")):
            self.load_hosts_from_csv()
        elif (self.src_file.endswith(".json")):
            self.load_hosts_from_json()
    
    def data_anaylaysis(self):
        # 提取除了 ip 以外的每一列的前 10 个值
        df = self.hosts_info_df
        top_values = {}
        for column in df.columns:
            if column not in ["ip", "hostname", "loc", "org", "postal", "anycast"]:
                top_values[column] = df[column].value_counts().head(10)
        
        # save to csv
        for i, (column, values) in enumerate(top_values.items()):
            values.to_csv(column + ".csv")

    def geolocation_analysis(self):
        # 提取除了 ip 以外的每一列的前 10 个值
        df = self.hosts_info_df

        # 创建地图
        m = folium.Map(location=[0, 0], zoom_start=2)

        # 在地图上添加标记
        for index, row in df.iterrows():
            loc = row["loc"].split(",")
            lat = float(loc[0])
            lon = float(loc[1])
            folium.Marker([lat, lon], popup=row["ip"]).add_to(m)

        # 保存地图为 HTML 文件
        m.save("world_map.html")
    
    def geolocation_analysis2(self):
        plt.figure()
        m = Basemap(projection="mill", llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution="c")
        m.drawcoastlines()
        m.drawcountries()
        #m.drawstates()

        # 在地图上添加标记
        for index, row in self.hosts_info_df.iterrows():
            loc = row["loc"].split(",")
            lat = float(loc[0])
            lon = float(loc[1])
            x, y = m(lon, lat)
            m.plot(x, y, "ro", markersize=5)
        
        plt.title("Hosts Geolocation")
        plt.savefig("./result/world_map.pdf")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IP Address analysis")
    parser.add_argument("-I", "--input", help="input file")

    args = parser.parse_args()
    source_file = args.input

    mpanslysis = MPTCPHostsAnalysis(source_file)
    mpanslysis.loadfile()
    mpanslysis.data_anaylaysis()
    #mpanslysis.geolocation_analysis2()
    mpanslysis.output_top10()









