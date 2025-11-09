from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `task` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'task id',
    `title` VARCHAR(255) NOT NULL COMMENT 'task title',
    `description` VARCHAR(255) NOT NULL COMMENT 'task description' DEFAULT '',
    `is_completed` BOOL NOT NULL COMMENT 'task is completed' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL COMMENT 'task create datetime',
    `updated_at` DATETIME(6) NOT NULL COMMENT 'task update datetime'
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
    "eJztlmtP2zAUhv9KlE+dxBDtuGnfWuhEJ9pOELYJhCI3cVOrjh3ikwFC/e/YTlIn7oWyic"
    "u0fUvec479+rETnwc35iGmYttDYup+dh5chmIsH2r6luOiJDGqEgCNqE6EMmMkIEUBSG2M"
    "qMBSCrEIUpIA4UyqLKNUiTyQiYRFRsoYucmwDzzCMMGpDFxdS5mwEN9hUb4mU39MMA1rNk"
    "mo5ta6D/eJ1noMvuhENdvIDzjNYmaSk3uYcDbPJgyUGmGGUwRYDQ9ppuwrd8UqyxXlTk1K"
    "brFSE+IxyihUlltjoGk5uY8lIALOFERpSehVRmqqj63m7sHu4af93UOZou3MlYNZvkYDIC"
    "/UGAaeO9NxBCjP0CwNPCAgh1vgdzRB6XKA8wKLoTRtMyyJrYNYCoaiOTkbYJy72YBkjO58"
    "ilkEE4Vvb28Nt+/ts6OT9llDZn1Qo3N5qvOjPihCrTym4BqYVYfPQGqVvR5Y112B1XL0Lu"
    "ASIZHFCcWKwQLdDucUI7bio7dKLcIjWftSiJf/B4t/gHBqtp7GvIZqZzg8VYPEQtxQLfQ8"
    "i+5Fv9M9azQ1dJlEAFf/EYZ0kGJFwUewyPlYRoDEeDnoeqWFOSxKt8uHN/hf5AadqoM/ou"
    "71+t1zr93/VkN/3Pa6KtLS6r2lNvatYz8fxPnR804c9epcDgddzZALiFI9o8nzLl3lCWXA"
    "fcZvfRRWQZRyKdX2NkvC39zbeuU73Nvc4D+2t6orGk8rV7sSRiiY3qI09BcivMVX5S6G4l"
    "ZsK4ihSO+Moql8Fj1iG6ckmCzrHovI2v4RmZz/HeTTx301g1duHn/hVDyz16mUvHEDuTnF"
    "l+9t1KfxDIhF+t8JsLmzswFAmbUSoI5ZLQtngNmSO+3r+XCwolcxJRbICyYXeBWSALYcSg"
    "Rcv0+sayiqVddurRJeo9/+aXM9Oh127OtIDdCRjN/0epk9ArTmSz8="
)
