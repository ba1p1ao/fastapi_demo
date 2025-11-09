#!/bin/bash

# 创建测试文件和目录的脚本
# 在项目根目录下运行此脚本

# 设置上传目录
UPLOAD_DIR="uploads"

echo "开始创建测试文件和目录..."

# 创建上传目录
mkdir -p $UPLOAD_DIR

# 创建主要目录结构
mkdir -p $UPLOAD_DIR/文档
mkdir -p $UPLOAD_DIR/图片
mkdir -p $UPLOAD_DIR/压缩包
mkdir -p $UPLOAD_DIR/用户文件/user1
mkdir -p $UPLOAD_DIR/用户文件/user2
mkdir -p $UPLOAD_DIR/用户文件/user3

# 创建文档文件
echo "这是项目计划书的内容" > $UPLOAD_DIR/文档/项目计划书.pdf
echo "这是需求文档的内容" > $UPLOAD_DIR/文档/需求文档.docx
echo "这是测试报告的内容" > $UPLOAD_DIR/文档/测试报告.xlsx
echo "这是README文件的内容" > $UPLOAD_DIR/文档/README.txt

# 创建图片文件（使用base64编码的小图片）
echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" | base64 -d > $UPLOAD_DIR/图片/风景图片1.jpg
echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" | base64 -d > $UPLOAD_DIR/图片/产品照片.png
echo "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" | base64 -d > $UPLOAD_DIR/图片/图标.gif

# 创建压缩包文件
tar -czf $UPLOAD_DIR/压缩包/源代码.zip -C $UPLOAD_DIR/文档/ .
tar -czf $UPLOAD_DIR/压缩包/备份文件.rar -C $UPLOAD_DIR/图片/ .
tar -czf $UPLOAD_DIR/压缩包/资料合集.7z -C $UPLOAD_DIR/文档/ .

# 创建用户个人文件
echo "这是user1的个人简历" > $UPLOAD_DIR/用户文件/user1/个人简历.pdf
echo "这是user1的照片" > $UPLOAD_DIR/用户文件/user1/照片.jpg
tar -czf $UPLOAD_DIR/用户文件/user1/作业.zip -C $UPLOAD_DIR/文档/ .

echo "这是user2的报告" > $UPLOAD_DIR/用户文件/user2/报告.docx
echo "这是user2的数据" > $UPLOAD_DIR/用户文件/user2/数据.xlsx

echo "这是user3的演示文稿" > $UPLOAD_DIR/用户文件/user3/演示文稿.pptx
echo "这是user3的截图" > $UPLOAD_DIR/用户文件/user3/截图.png
tar -czf $UPLOAD_DIR/用户文件/user3/资料.tar.gz -C $UPLOAD_DIR/文档/ .

# 设置文件权限
chmod -R 755 $UPLOAD_DIR

echo "测试文件和目录创建完成！"
echo "上传目录结构："
find $UPLOAD_DIR -type f | sort