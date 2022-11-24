#!/bin/bash
if [ $1 ]; then
    echo "version $1"
    version=$1
    cd /root
    ## Download youtube-assistant
    echo "Download youtube_assistant version $1"
    wget https://github.com/javishome/youtube-assistant/archive/refs/tags/v${version}.tar.gz
    ## Giải nén
    tar -xf v${version}.tar.gz
    ## Xoá thư mục youtube_assistant trong custorm components
    rm -rf /usr/share/hassio/homeassistant/custom_components/youtube_assistant
    ## Copy thư mục youtube_assistant vào custorm components trên HA
    cp -rf youtube-assistant-${version}/custom_components/youtube_assistant /usr/share/hassio/homeassistant/custom_components
    ## Xoá các file tải
    rm -r youtube-assistant-${version}
    rm -f youtube-assistant-${version}.tar.*
    rm -f v${version}.tar.*
    ## Khai báo youtube assistant trong file configuration
    File="/usr/share/hassio/homeassistant/configuration.yaml"
    if ! [[ $(grep "youtube_assistant:" $File) ]] ; then
        echo -e "\nyoutube_assistant:" >> /usr/share/hassio/homeassistant/configuration.yaml
    fi
    ## Restart homeassistant
    echo "Restart homeassistant"
    docker restart homeassistant
    echo "Restart homeassistant success"
else
    echo "./youtube_assistant.sh 2022.8.5 or 2022.7.4"
fi
exit 0