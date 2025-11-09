from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100),
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `posts` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `content` LONGTEXT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `author_id` INT NOT NULL,
    CONSTRAINT `fk_posts_users_63d1e9cc` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
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
    "eJztmO9PozAYx/+VhVde4hndOTX3Duc8d+pmFO+MxpAOOmiEFqHctpj979cWWCkDbjP+2C"
    "57B88PeJ5PC/22L5pPbOhFO1ckotr3xouGgQ/ZhWLfbmggCKSVGygYeCIwYBHCAgYRDYHF"
    "HzMEXgSZyYaRFaKAIoKZFceex43EYoEIO9IUY/QcQ5MSB1IXhszx8MjMCNtwDKPsNngyhw"
    "h6tlInsvm7hd2kk0DYupieikD+toFpES/2sQwOJtQleBaNsOjQgRiGgEL+eBrGvHxeXdpm"
    "1lFSqQxJSszl2HAIYo/m2l2QgUUw58eqiUSDDn/L1+be/uH+0beD/SMWIiqZWQ6nSXuy9y"
    "RREOgZ2lT4AQVJhMAouVFE2ePm0LVdEJazmyUU8LGii/gyWHX8MoMEKCfNGxH0wdj0IHao"
    "y7G1WjW8funX7TP9eotFfeHdEDaRk+ndS13NxMehSojsjRQm00fFaMBxxRTMpawLyBpuRu"
    "fO4EX7UfTs5XFtXep3gqQ/ST0X/d6PLDyHt33RPy5SDSHv3wQlYE+YhyIfVsBVMgt87TR1"
    "J7tYTdoa68HuY2+S/lPq6HcvOzeGfnmlDMGJbnS4p6ngz6xbB4UJPntI43fXOGvw28Z9v9"
    "cRBNm/3QnFG2Wcca/xmkBMiYnJyAR27veXWTMwysDGgf3KgVUzNwP7qQObFi/HlflcEppL"
    "LcVKzr9X5BUZwjdYlLmSGT6VrskJk3mIpySEyMHncCJYdllNAFtli3Gq2m4juNpribTKGR"
    "aC0UzfqdODNcjagjRRKPpNWz/paALkAFhPIxDapkKUe0iTFCyz2HmX3/SLFoCBIwjwPnjV"
    "ebQlQjlDXi2UYxaxEcprJ5T5sInrJbRyPudtVN67U1TEcmt3Aa3c2q2UytylajroA+Qtg3"
    "CW8Cp+KZ1P223s7S5CkEVVIhQ+lWEAomhE2A/MBZG7DMu5xHXZeXzEFm6z2fgfNGmy2ZjT"
    "VtUaIfdZZQdY6uAfp2mn59fQAwJspd7KTslWb4Cr9Nb0PTWSDkNkuWUqKfXU6iQgYzZCaY"
    "2E0h8mb9OvZNGFKZeyWZLkNpB9GktATMPXE+C7CKXKY9mfN/3esseyt5g1+GAji243PBTR"
    "x9XEWkORd11/SFs8jy2sxvwBx2VHFx+5BZ/+BRL4iY8="
)
