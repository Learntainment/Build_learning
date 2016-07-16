#! /bin/bash

function pause(){
	read -n 1 -p "$*" INP
        if [ "$INP" != '' ]; then
                echo -ne '\b \n'
        fi
}
DEPLOY_PATH=$(pwd)
if [ -n "$2" ]; then
    CHECKOUT_BRANCH=$2
else
    CHECKOUT_BRANCH="master"
fi
function check_file()
{
    CONTEXT_LIST=$(ls)
    array_list=($CONTEXT_LIST)
    number=${#array_list[@]}
    local i=0
    local sum=0
    while ((i<$number))
    do
        if [ "${array_list[i]}" = "ceph" ]; then
            let sum++
            ceph_flag=1
        elif [ "${array_list[i]}" = "fio" ]; then
            let sum++
            fio_flag=1
        elif [ "${array_list[i]}" = "hyperstash" ]; then
            let sum++
            hyperstash_flag=1
        elif [ "${array_list[i]}" = "rocksdb" ]; then
            let sum++
            rocksdb_flag=1
        fi
        let i++
    done
    return $sum
}
function double_check_file()
{
    CONTEXT_LIST=$(ls)
    array_list=($CONTEXT_LIST)
    number=${#array_list[@]}
    local i=0
    local sum=0
    while ((i<$number))
    do
        if [ "${array_list[i]}" = "ceph" ]; then
            let sum++
        elif [ "${array_list[i]}" = "fio" ]; then
            let sum++
        elif [ "${array_list[i]}" = "hyperstash" ]; then
            let sum++
        elif [ "${array_list[i]}" = "rocksdb" ]; then
            let sum++
        fi
        let i++
    done
    return $sum
}
#pause 'Press any key to continue...'
if [ "$1" != "clean" ]; then

    #check file status

    CPU_NUM=$(cat /proc/cpuinfo | grep 'processor' | wc -l)
    let COMPILE_NUM=CPU_NUM/2
    check_file_result=0
    hyperstash_result=0
    hyperstash_test_result=0
    ceph_result=0
    vstart_result=0
    data_store_device_result=0
    rocksdb_flag=0
    ceph_flag=0
    fio_flag=0
    hyperstash_flag=0

    #get the ls list

    check_file
    check_file_result=$?

    #check flag and install

    if [ $check_file_result != 4 ]; then
        if [ $rocksdb_flag = 0 ]; then
            echo "miss rocksdb and install rocksdb"
            git clone https://github.com/facebook/rocksdb.git
            cd $DEPLOY_PATH/rocksdb/
            make shared_lib && make install
            cd $DEPLOY_PATH/
        fi
        if [ $ceph_flag = 0 ]; then
            echo "miss ceph and install ceph"
            pip uninstall -y ceph-detect-init
            pip uninstall -y ceph-disk
            git clone git://192.168.13.8/ceph_int.git ceph
            cd $DEPLOY_PATH/ceph/
            git checkout v10.2.2 -b test
            ./install-deps.sh
            ./autogen.sh
            ./configure
            make -j$COMPILE_NUM && make install

            #Error Handle

            ceph_result=$?
            if [ $ceph_result != 0 ]; then
                echo "Install ceph failed"
                exit 1
            fi
            cd $DEPLOY_PATH/
        fi
        if [ $hyperstash_flag = 0 ]; then
            echo "miss hyperstash and install hyperstash"
            tsocks git clone git@github.com:Intel-bigdata/hyperstash.git
            cd $DEPLOY_PATH/hyperstash/
            git remote add yuanhui git@github.com:Ericyuanhui/hyperstash.git
            git remote add zhouyuan git@github.com:zhouyuan/hyperstash.git
            git remote add chendi git@github.com:xuechendi/hyperstash.git
            cp -r $DEPLOY_PATH/ceph/src/include/rbd /usr/local/include/
            cp -r $DEPLOY_PATH/ceph/src/include/rados/ /usr/local/include/
            cd $DEPLOY_PATH/
        fi
        if [ $fio_flag = 0 ]; then
            echo "miss fio and install fio"
            tsocks git clone git@github.com:axboe/fio.git
            #install fio
            cd $DEPLOY_PATH/fio/
            ./configure
            make -j$COMPILE_NUM && make install
            cd $DEPLOY_PATH/
        fi
    else
        echo "have all package finish!"
    fi

    #Error Handle

    double_check_file
    check_file_result=$?
    if [ $check_file_result != 4 ]; then
        echo "Download Repository Failed"
        exit 1
    fi

    #Install hyperstash
    #CHECKOUT_BRANCH is for your own branch for test

    echo "Install Hyperstash"
    cd $DEPLOY_PATH/hyperstash
    if [ "$1" = "yuanhui" ]; then
        tsocks git fetch yuanhui
        git checkout yuanhui/$CHECKOUT_BRANCH
    elif [ "$1" = "zhouyuan" ]; then
        tsocks git fetch zhouyuan
        git checkout zhouyuan/$CHECKOUT_BRANCH
    elif [ "$1" = "chendi" ]; then
        tsocks git fetch chendi
        git checkout chendi/$CHECKOUT_BRANCH
    else
        git checkout master -B test
    fi
    #apply patch for librbd
    cp $DEPLOY_PATH/hyperstash/librbd-hyperstash.patch $DEPLOY_PATH/ceph/
    cd $DEPLOY_PATH/ceph/; git clean -fd; git reset --hard
    git apply librbd-hyperstash.patch
    cd $DEPLOY_PATH/
    mkdir -p /etc/rbc/
    cp $DEPLOY_PATH/hyperstash/rbc.conf /etc/rbc/.

    #Hyperstash unittest

    cd $DEPLOY_PATH/hyperstash
    make test
    hyperstash_test_result=$?
    if [ $hyperstash_test_result != 0 ]; then
        echo "Hyperstash unittest failed"
        exit 1
    fi
    make clean
    make && make install

    #Error Handle

    hyperstash_result=$?
    if [ $hyperstash_result != 0 ]; then
        echo "Install hyperstash failed"
        exit 1
    fi

    #apply patch for ceph librbd

    if [ $hyperstash_flag = 0 ]; then
        echo "Install patch for ceph"
        cd $DEPLOY_PATH/ceph/
        make clean
        make uninstall
        cp -r $DEPLOY_PATH/ceph/src/include/rbd /usr/local/include/
        cp -r $DEPLOY_PATH/ceph/src/include/rados/ /usr/local/include/
        make -j$COMPILE_NUM && make install

        #Error Handle

        ceph_result=$?
        if [ $ceph_result != 0 ]; then
            echo "Install ceph patch failed"
            exit 1
        fi
    else
        echo "Have applied patch"
    fi

    #Deploy v ceph

    echo "Deploy ceph cluster"
    cd $DEPLOY_PATH/ceph/src/
    ./vstart.sh -n -X

    #Error Handle

    vstart_result=$?
    if [ $vstart_result != 0 ]; then
        echo "vstart failed"
        exit 1
    fi

    mkdir -p /etc/ceph && cp ceph.conf /etc/ceph/ceph.conf
    ldconfig

    # start fio job

    for rbd_name in `rbd ls`
    do
        rbd rm $rbd_name
    done

    rbd create testimage --size 81920M
    data_store_dev=$(fdisk -l | grep 200.0)

    #Error Handle

    data_store_device_result=$?
    if [ $data_store_device_result != 0 ]; then
        echo "unmount data device"
        exit 1
    fi
    data_dev_list=($data_store_dev)
    sed -i '/DataStoreDev/c DataStoreDev='${data_dev_list[1]:0:8}'' /etc/rbc/rbc.conf

    #TODO hack for multi-volume tests
    cp /etc/rbc/rbc.conf /etc/rbc/testimage.conf
#sed -i '/DataStoreDev/c DataStoreDev=/dev/sdb' /etc/rbc/testimage.conf

    fio $DEPLOY_PATH/fio.conf &>$DEPLOY_PATH/fio_result.txt

    #clean up

    cd $DEPLOY_PATH/ceph/src/
    ./stop.sh
    cd $DEPLOY_PATH/
    rm -rf hyperstash
    exit 0
else
    #clean the environment
    cd $DEPLOY_PATH/ceph/
    make clean
    make uninstall
    cd $DEPLOY_PATH/hyperstash/
    make clean
    make uninstall
    cd $DEPLOY_PATH/
    rm -rf ceph hyperstash fio rocksdb *.txt
    echo "Clean finish"
    exit 0
fi
