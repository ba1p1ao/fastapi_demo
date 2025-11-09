from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `email` VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    `password_hash` VARCHAR(255) NOT NULL  COMMENT '密码哈希',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `files` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL  COMMENT '文件名',
    `description` LONGTEXT NOT NULL  COMMENT '文件描述',
    `filename` VARCHAR(500) NOT NULL  COMMENT '存储的文件名',
    `file_path` VARCHAR(500) NOT NULL  COMMENT '文件存储路径',
    `file_size` INT NOT NULL  COMMENT '文件大小（字节）',
    `category` VARCHAR(4) NOT NULL  COMMENT '文件分类',
    `subcategory` VARCHAR(50)   COMMENT '文件子分类',
    `download_count` INT NOT NULL  COMMENT '下载次数' DEFAULT 0,
    `like_count` INT NOT NULL  COMMENT '点赞数' DEFAULT 0,
    `collect_count` INT NOT NULL  COMMENT '收藏数' DEFAULT 0,
    `permission` VARCHAR(7) NOT NULL  COMMENT '文件权限' DEFAULT 'public',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `author_id` INT NOT NULL COMMENT '作者',
    CONSTRAINT `fk_files_users_c3dd6c6a` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    KEY `idx_files_categor_cc5a45` (`category`, `subcategory`),
    KEY `idx_files_downloa_ab43b4` (`download_count`),
    KEY `idx_files_created_e0978a` (`created_at`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `collections` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `file_id` INT NOT NULL COMMENT '文件',
    `user_id` INT NOT NULL COMMENT '用户',
    UNIQUE KEY `uid_collections_user_id_b83180` (`user_id`, `file_id`),
    CONSTRAINT `fk_collecti_files_770b7519` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_collecti_users_5600ea46` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `comments` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `content` LONGTEXT NOT NULL  COMMENT '评论内容',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `file_id` INT NOT NULL COMMENT '文件',
    `user_id` INT NOT NULL COMMENT '用户',
    CONSTRAINT `fk_comments_files_e17abb26` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comments_users_24d9ac18` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `likes` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `file_id` INT NOT NULL COMMENT '文件',
    `user_id` INT NOT NULL COMMENT '用户',
    UNIQUE KEY `uid_likes_user_id_6569a2` (`user_id`, `file_id`),
    CONSTRAINT `fk_likes_files_542d8f1b` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_likes_users_a61ca3f4` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `shares` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `share_token` VARCHAR(100) NOT NULL UNIQUE COMMENT '分享令牌',
    `share_link` VARCHAR(500) NOT NULL  COMMENT '分享链接',
    `password` VARCHAR(50)   COMMENT '提取密码',
    `expire_at` DATETIME(6)   COMMENT '过期时间',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `file_id` INT NOT NULL COMMENT '文件',
    CONSTRAINT `fk_shares_files_65460b45` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
