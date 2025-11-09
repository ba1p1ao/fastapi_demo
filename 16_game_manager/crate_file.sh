#!/bin/bash

# 创建主目录结构
mkdir -p files/games files/tools files/mods

# 更智能的文件大小生成函数
create_smart_size_file() {
    local file_path=$1
    local category=$2  # games, tools, mods
    
    # 根据文件类型设置不同的大小倾向
    case $category in
        "games")
            # 游戏文件倾向于更大 (1-5MB)
            local min_size=1024    # 1MB
            local max_size=5120    # 5MB
            ;;
        "tools")
            # 工具文件大小变化较大 (0.1-3MB)
            local min_size=100     # 0.1MB
            local max_size=3072    # 3MB
            ;;
        "mods")
            # 模组文件通常较小 (0.05-2MB)
            local min_size=50      # 0.05MB
            local max_size=2048    # 2MB
            ;;
    esac
    
    # 生成随机大小
    local size_kb=$(( RANDOM % (max_size - min_size + 1) + min_size ))
    
    # 创建文件
    dd if=/dev/urandom of="$file_path" bs=1024 count=$size_kb 2>/dev/null
    
    local actual_size=$(du -h "$file_path" | cut -f1)
    echo "创建: $file_path (大小: $actual_size)"
}

echo "开始创建文件结构..."

# 创建games文件
echo -e "\n创建游戏文件 (倾向于 1-5MB):"
create_smart_size_file "files/games/gta5_complete.zip" "games"
create_smart_size_file "files/games/minecraft_1.19.zip" "games"
create_smart_size_file "files/games/csgo_full.zip" "games"
create_smart_size_file "files/games/witcher3_goty.zip" "games"
create_smart_size_file "files/games/civilization6_deluxe.zip" "games"
create_smart_size_file "files/games/forza_horizon5.zip" "games"
create_smart_size_file "files/games/fifa23_complete.zip" "games"
create_smart_size_file "files/games/elden_ring.zip" "games"
create_smart_size_file "files/games/stardew_valley.zip" "games"
create_smart_size_file "files/games/sekiro_shadows.zip" "games"

# 创建tools文件
echo -e "\n创建工具文件 (倾向于 0.1-3MB):"
create_smart_size_file "files/tools/cheat_engine_7.4.zip" "tools"
create_smart_size_file "files/tools/unity_editor.zip" "tools"
create_smart_size_file "files/tools/obs_studio.zip" "tools"
create_smart_size_file "files/tools/nvidia_optimizer.zip" "tools"
create_smart_size_file "files/tools/vscode_portable.zip" "tools"
create_smart_size_file "files/tools/cpu_optimizer.zip" "tools"
create_smart_size_file "files/tools/save_editor.zip" "tools"
create_smart_size_file "files/tools/photoshop_cc.zip" "tools"
create_smart_size_file "files/tools/localization_tool.zip" "tools"
create_smart_size_file "files/tools/directx_repair.zip" "tools"

# 创建mods文件
echo -e "\n创建模组文件 (倾向于 0.05-2MB):"
create_smart_size_file "files/mods/minecraft_shaders.zip" "mods"
create_smart_size_file "files/mods/gta5_traffic_mod.zip" "mods"
create_smart_size_file "files/mods/witcher3_hd_textures.zip" "mods"
create_smart_size_file "files/mods/skyrim_new_lands.zip" "mods"
create_smart_size_file "files/mods/cyberpunk_ui_mod.zip" "mods"
create_smart_size_file "files/mods/sekiro_difficulty.zip" "mods"
create_smart_size_file "files/mods/fallout4_survival.zip" "mods"
create_smart_size_file "files/mods/sims4_careers.zip" "mods"
create_smart_size_file "files/mods/gta5_first_person.zip" "mods"
create_smart_size_file "files/mods/minecraft_tech_mod.zip" "mods"

echo -e "\n=== 创建完成 ==="
echo "目录结构:"
find files/ -type f | sort

echo -e "\n详细文件信息:"
ls -lh files/games/
ls -lh files/tools/ 
ls -lh files/mods/

echo -e "\n磁盘使用情况:"
du -csh files/ files/games/ files/tools/ files/mods/