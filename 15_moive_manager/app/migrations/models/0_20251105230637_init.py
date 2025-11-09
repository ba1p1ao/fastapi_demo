from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `avatar_url` VARCHAR(500),
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `movies` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `cover_url` VARCHAR(500),
    `description` LONGTEXT,
    `release_year` INT,
    `duration` INT,
    `rating` DECIMAL(3,1),
    `director` VARCHAR(255),
    `actors` LONGTEXT,
    `country` VARCHAR(100),
    `language` VARCHAR(100),
    `plot` LONGTEXT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `comments` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `content` LONGTEXT NOT NULL,
    `rating` DECIMAL(2,1),
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `is_deleted` BOOL NOT NULL  DEFAULT 0,
    `deleted_at` DATETIME(6),
    `movie_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_comments_movies_98a3db4d` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comments_users_24d9ac18` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `slug` VARCHAR(100) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `movie_categories` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `category_id` INT NOT NULL,
    `movie_id` INT NOT NULL,
    CONSTRAINT `fk_movie_ca_categori_a7884894` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_movie_ca_movies_334db5f9` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE
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
    "eJztml9v2zYQwL9K4KcU8ILGTdpib47jbFmTuEjcYVhRCLTEyEQo0qWoJELh7z6Skizqb0"
    "1HWaRGb/aRZ5I/Ho93Z/4YeNSB2D/44kM2+H3vx4AAD4oPGflwbwBWq1QqBRwssOoYiB5K"
    "AhY+Z8DmQngLsA+FyIG+zdCKI0qElAQYSyG1RUdE3FQUEPQ9gBanLuRLNZGv34QYEQc+Qj"
    "/5urqzbhHETmaeyJFjK7nFw5WSnRN+pjrK0RaWTXHgkbTzKuRLSja9EeFS6kICGeBQ/jxn"
    "gZy+nF28zGRF0UzTLtEUNR0H3oIAc225WzKwKZH8xGx8tUBXjnIoGtT4o8OjD0cf370/+r"
    "COFpWuOOqu1n01H6xVO+Ag6qHgpbTkZqnPBWaTJWDl0HSdHDox4Ty6BNSLsvPAo4UhcflS"
    "Mnz7tobZ3+PryZ/j633R642Cl8KCHkDYhNRGoYuYRsfHW2ASvfKYVsD3HyhzrCXwlya4Co"
    "rNYEsEKbfUHbUKHLgXx5RZATMysqzWTshiO3oxYsdbncjj4om0GZSrsgAvEjsVLRx5sJxa"
    "VjNHzYlVD5IPLTU7sQZnRnAYb2ENw/n55fRmPr78LFfihf53rBCN51PZsv/+jaJAfe4ypZ"
    "UqzP8dyN8FAacWoQ8WcDTPk0iTxa3ltXx7p101UrAA9t0DEOc606LtIvU8KNdU2MOTWPPs"
    "0zXEQPEp7lYcmUyiX2nnVq0T+0ukyZZJPnREq4gVm7yRl5cAAlw1azm2HCkmcknvESwL4q"
    "KG2ijOk136MK4jYRxHHBvFcBuFV3bF2vQeGt+wGaXXdcHqoxeIzeFjxYHMqXWEWd39Of1n"
    "nrk6L2ZXfyhhlheDGAIfWiEEzMCB5dV+7spaASxyZr9tnNjHndyaZm0BA+WmVklOV3ml1C"
    "QAMVwxAIY28gCusLiNUj72jbQOYu1WEqzBczqdnF+OL/bfDQ9VTCuOK+JQ93JHRSeHGLQ5"
    "LTmw1XeCrtMR99ZUliqXXRKrV98GqUZHSDVwEdg0IJyFZmHGRqUjnBqqq2FA3ECkMCawdJ"
    "3XRWuFaUm1o/r0Jf07QqmJs9dXhdpVFdI3J1g5O25OVrPfnCdvzqYA1VfsKv1QsWKnG7Oq"
    "klm2mLhLWVwv252HKstNMj/WIS7PWclMLKWklqkZUXU1U7fXvp7Z/nqmGITHm7ptmKOpdK"
    "Wm2US9qc/9i7n/yCD372PF1oQjxVgR+ZZw5VASK16slGIISIUDzSjm9mYhNJ9rO0xvlO2N"
    "+2Q2u8gadUn9NFrzDsac1WzAmFvlGJq23WTqtcYbxYZG976uslMx+yVcyBMCgOw7NDNWms"
    "avj6qQpGXJFbGdUQaRSz7BUNE7F/MAxC6rluXedbaPWlXCMZSBzMMm1NYNQiwvcmhSPhnf"
    "TMan00HxcDaAbfOSorvcdKdTDq66IvCsOV+UCIeDsqQvaRvWZn2ZVLrP+9rhy4Y1eZ/pU+"
    "RmnyF35i8AHwclOV81pqR/F58hG0HaqZjZF/H+x+eIGpmqh4lZeD95omj1Tr5rTj7esdAs"
    "3s9p/foxf59LNpMg9aG+QaifKY1qQfYT2enxenfx5VxQm5KlMWTIXpZdqXFL7U0K0j79/d"
    "kKf1Z3f95D5pc+kq1OADSVbqZKu79WFEZvACru3k1IO+eTlX+3/nUzuzL9u/ULEYv46iCb"
    "D/cw8vm3dqKrISVXnf9HQMpOzDLM5v39+j8hca7u"
)
