set terminal pdfcairo enhanced font 'Times,12' size 8cm, 16cm
set output "barchart.pdf"
set style fill pattern 1
set datafile separator ","
#set grid
#unset border
set grid

# 设置柱状图样式
set style data histograms
set style histogram clustered
set boxwidth 0.5  # 设置柱子宽度
set xtics rotate by -30

# 设置 x 轴标签

# 设置 y 轴标签
set ylabel "Number of MPTCP-capable Hosts"

# 设置 x 轴刻度标签
set xtics rotate by -45

# 忽略第一行（标题行）数据
set multiplot layout 3,1
set title "City Rank"
plot "city.csv" every ::1 using 2:xtic(1) with boxes notitle

set title "Country Rank"
plot "country.csv" every ::1 using 2:xtic(1) with boxes notitle

set title "Region Rank"
plot "region.csv" every ::1 using 2:xtic(1) with boxes notitle
unset multiplot
```
