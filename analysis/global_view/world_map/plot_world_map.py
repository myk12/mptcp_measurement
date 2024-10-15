import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# 读取两个数据文件
scaned_data_file = 'scaned_result.dat'
org_data_file = 'org_result.dat'

def read_lat_lon(file):
    lats, lons = [], []
    with open(file, 'r') as f:
        for line in f:
            lat, lon = map(float, line.strip().split())
            lats.append(lat)
            lons.append(lon)
    return lats, lons

scaned_lats, scaned_lons = read_lat_lon(scaned_data_file)
org_lats, org_lons = read_lat_lon(org_data_file)

# 创建两个子图，一行两列
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(12, 3.7))

# 绘制扫描结果地图
axes[0].set_title("MPTCP Organization Results")
m1 = Basemap(ax=axes[0], projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution="c")
m1.drawcoastlines()
m1.drawcountries()
m1.scatter(org_lons, org_lats, s=1, latlon=True, c='red', marker='o')

# 绘制原始数据地图
axes[1].set_title("MPTCP Organization (red) & Scaned (blue) Results")
m2 = Basemap(ax=axes[1], projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution="c")
m2.drawcoastlines()
m2.drawcountries()
m2.scatter(org_lons, org_lats, s=1, latlon=True, c='red', marker='o')
m2.scatter(scaned_lons, scaned_lats, s=1, latlon=True, c='blue', marker='o')


# 保存为PDF文件
plt.tight_layout()
plt.savefig('geographic_locations_basemap.pdf', dpi=300)

