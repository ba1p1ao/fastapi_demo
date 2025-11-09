#!/bin/bash

# 创建测试文件和目录的脚本
# 在项目根目录下运行此脚本

# 设置上传目录
UPLOAD_DIR="`pwd`/uploads"

echo "开始创建测试文件和目录..."

# 创建上传目录
mkdir -p $UPLOAD_DIR

# 设置文件权限
chmod -R 755 $UPLOAD_DIR
