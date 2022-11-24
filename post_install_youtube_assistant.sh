#!/bin/bash
if [ $1 ]; then
    echo $1
    if [ $2 ]; then
    ## xóa cache login cũ
    echo "step 0 - xóa cache login cũ"
    ssh-keygen -f "/root/.ssh/known_hosts" -R "[127.0.0.1]:6000"
    rm -f /root/.ssh/known_hosts

    current_mac=$1
    ## lay dia chi mac bo di dau :
    current_mac_upper=$(echo ${current_mac^^} | sed -e 's/://g')
    echo $current_mac_upper

    ## đổi mac sang số
    mac_id=$(( 16#$current_mac_upper ))
    echo $mac_id

    ## lấy 8 chữ số cuối địa chỉ mac
    short_mac=${current_mac_upper:(-4)}
    echo "4 chữ số cuối địa chỉ mac: " $short_mac

    ## đổi các chữ thành số 9
    short_mac_4=${short_mac//[A-Z]/9}

    #ví dụ mac là 900EB34210D5 thì pass ssh là javis951095. Pass HA là js9585

    ## pass HA là dãy số gồm js + chữ số đầu + chữ số cuối + 2 chữ số cuối địa chỉ mac thay chữ bằng số 8
    ## pass ssh là dãy số gồm javis+ chữ số đầu + chữ số cuối + 4 chữ số cuối của địa chỉ mac đã thay chữ bằng số 9
    ssh_pass_final="javis"${current_mac_upper:0:1}${current_mac_upper:(-1)}$short_mac_4
    echo "step 1 - Pass ssh may khach: " $ssh_pass_final
    ## cài đặt youtube assistant trên máy khách
    mac_upper=$(sshpass -p $ssh_pass_final ssh -p 6000 -o StrictHostKeyChecking=no root@127.0.0.1 "bash -s" < youtube_assistant.sh $2)
    else
        echo "./post_install_youtube_assistant.sh A81905E9608A 2022.8.5"
    fi
else
    echo "./post_install_youtube_assistant.sh A81905E9608A 2022.8.5"
fi