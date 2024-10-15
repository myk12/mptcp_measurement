#!/bin/bash

# log into IPInfo.io
token="df978f03d05296"
curl -u $token: ipinfo.io

# parse file
while getopts "I:O:" opt; do
    case $opt in
        I)
            input_file=$OPTARG
            ;;
        O)
            output_file=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            echo "Usage: $0 -I input_file -O output_file" >&2
            exit 1
            ;;
    esac
done

if [-z "$input_file"]; then
    echo "Input file is required!" >&2
    exit 1
fi

if [-z "$output_file"]; then
    output_file="ip_info.json"
fi

# 获取输入文件的总行数
total_lines=$(wc -l < "$input_file")

# 遍历输入文件的每一行并显示进度条
err_count=0
while IFS= read -r line; do
    # 提取JSON中的IP地址
    ip=$(echo "$line" | jq -r '.saddr')

    # 查询IP地址信息并添加到数组中
    # try three times
    info=$(curl -s "ipinfo.io/$ip?token=$token")
    if [ -z "$info" ]; then
        info=$(curl -s "ipinfo.io/$ip?token=$token")
    fi
    if [ -z "$info" ]; then
        info=$(curl -s "ipinfo.io/$ip?token=$token")
    fi
    if [ -z "$info" ]; then
        echo "{\"$ip\"}" >&2
	err_count=$error_count + 1
    fi

    # save to output file
    echo "$info" >> "$output_file"

    # 更新进度条
    ((++count))
    echo -ne $'\e[1A'
    echo -ne $info
    echo -ne "\nProgress: $count / $total_lines\r"
done < "$input_file"

echo "Progress: $total_lines / $total_lines"
echo "Process completed!"

