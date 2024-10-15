# 使用grep命令提取数据行
grep -oP "add_marker_ll\(\K[^)]+" input | tr -d "'" | sed 's/,/ /g' > extracted_data.txt

# 在提取的数据前添加标题行
echo "Latitude Longitude Src Type Country Location" > output.csv

# 使用awk命令将提取的数据写入CSV文件
awk '{print $1 "," $2 "," $3 "," $4 "," $5 "," $6}' extracted_data.txt >> output.csv

# 删除中间文件
rm extracted_data.txt

