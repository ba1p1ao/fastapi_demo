from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `is_admin` BOOL NOT NULL  DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `files` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `path` VARCHAR(1000) NOT NULL,
    `size` INT NOT NULL  DEFAULT 0,
    `is_directory` BOOL NOT NULL  DEFAULT 0,
    `mime_type` VARCHAR(100),
    `upload_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `modified_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `owner_id` INT NOT NULL,
    `parent_id` INT,
    CONSTRAINT `fk_files_users_dfac26a2` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_files_files_bd364469` FOREIGN KEY (`parent_id`) REFERENCES `files` (`id`) ON DELETE CASCADE,
    KEY `idx_files_owner_i_217f6b` (`owner_id`, `parent_id`)
) CHARACTER SET utf8mb4 COMMENT='文件表';
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
    "eJztmd1T4jAQwP8Vp0864zmIfM29Icqc5yk3ivdw4HRCG0rGNKltesg5/O+XpN8lYEFQPH"
    "kCNrtt9pdssrs8azY1IfaO2ghDT/u696wRYEP+JTtwuKcBx0nEQsDAAEvNYawy8JgLDMaF"
    "Q4A9yEUm9AwXOQxRIlT7fq3aqPf9ChzW+n6jUWsIO5Ma3BARi6sQH2Mu8gl69KHOqAXZCL"
    "p8oHfPxYiY8ElOtNfT6JhAV0emeIQDXEiY+HEv9JwHfYggNjMeBZpSrrOJI2UXhLWlopjG"
    "QDco9m2SKDsTNqIk1kaECakF+YsBg+LxzPWFn2LaIY/I9cCFRCWYe8rGhEPgY5Y4nYUVCW"
    "fhGJQI0Hw2wZJZ4i3HfEC+v3xcqVcaJ7VKfRo4lXgcqEu/r7vaVI4DBgINSTWhJT9neLVG"
    "wFUDi/RzyPhE88giQIuYRYIEWrKj1kTNBk86hsRiIwGtWl1A61fzpvWtebPPtQ4ktgSTA7"
    "j9Epgi/Y+J6bhUKhXgJNTyoDz0V7Gf5sZfpP5yBK6LU+m1EfgljrzGSrGYOqk83UQuNBh1"
    "J7PMTinFEJA551bONMdvwG03BVB95heGuIDQaafzQ8zae8SIQTUzG9kwcHOJaMwYrRSS4V"
    "n+nhFZLCDz8eg7mAKuj1TH/Bl3WIyoqeVMc9zM0PYo+rKlB5sLgdkheBIu4gKK3Yur89tu"
    "8+qn8MSe8F0oGTW752Jkv3YgKVCPWa60Sgy6vzXxXOAzqhM61oGZuv8jaeRcdjtTE/G5rL"
    "ZAM8a7JXr1EoUTSFYonX4WvNQyGeubXWzvl12m06QoPy9OK2OzEq53OJxXpiXKluGDMhWX"
    "22YWXJu6EFnkEk4kvws+EUAMVbyHtdydB11vO3fZNFr8SJqsngvGcTGXiSDuIHcLBglBq3"
    "nbap6da4pdtwZycRW8dRuuKLhMMKnJiR04AMbDGLimPmcrGiOETf4kRVYaWrYvbyAG0o3/"
    "CKeEQ8s0BSWDa3bILtt5CSDAkrMW7xZvysSlovkSB+z85osfqxRovtSr5Ubfr5VP6q9svu"
    "x6LGvpsYjFW7bPkrZZTxNh4+wyBUu1SL1SnSlXHOB5Y8ojbQS8JRsuOcOP2XlZuUGFPJ7S"
    "2kh1Yr/QR4jNPk0PweAFB/dHB4qcYXHFlbXclVtrqohnkuIiOUr8f8TmE5QtypQ3mqE0oY"
    "uMkSpFCUcW5igg0XkpSZmPYZeUvFFS8ocnlGFwFL1jUyaf7HYVm34JUKH6x4S0cquZP5Up"
    "6/Dvt53rOfdpYpKDdUe4Ez0TGexwDyOP3W8nugWkhNf5+1HITlVdoPkX3vrP++k/xlpoDA"
    "=="
)
