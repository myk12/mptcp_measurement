# 设置输出格式为PDF
set terminal pdfcairo enhanced font "Arial,12" size 16cm,8cm

# 创建全球地理图
set output "world_map.pdf"

# 设置绘图区域
set xrange [-180:180]
set yrange [-90:90]

# 绘制地图背景（使用世界地图数据文件world.dat）
plot "world.dat" with lines lc rgb "black" lw 0.5 notitle

# 绘制数据点（使用loc列的经纬度坐标）
plot "mptcp_hosts_info.csv" using 6:7 with points lc rgb "red" pt 7 ps 1 notitle

# 创建排名前二十的国家和地区图
set output "top_countries.pdf"

# 设置绘图区域
set bmargin 5

# 排序数据并选择前20个
system("tail -n +2 mptcp_hosts_info.csv | sort -t',' -k5 -r | head -n 20 > top_countries.tmp")

# 绘制条形图
plot "top_countries.tmp" using 5:xtic(6) with boxes lc rgb "blue" notitle

# 清除临时文件
system("rm top_countries.tmp")

