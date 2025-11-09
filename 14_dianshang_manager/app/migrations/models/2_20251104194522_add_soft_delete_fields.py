from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `orders` ADD `is_deleted` BOOL NOT NULL DEFAULT 0;
        ALTER TABLE `orders` ADD `deleted_at` DATETIME(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `orders` DROP COLUMN `is_deleted`;
        ALTER TABLE `orders` DROP COLUMN `deleted_at`;"""


MODELS_STATE = (
    "eJztm/FTmzAUx/8Vj5/mnfO0022336rWrZvanXa73XY7LoVIc4YEIai9Xf/3JQFKgIDSYq"
    "Ubv9WXPJL3SXh8X8A/hkttiIPdbwH0jQ9bfwwCXMh/ZOw7WwbwvNQqDAxMsOwY8h7SAiYB"
    "84HFuPEa4ABykw0Dy0ceQ5RwKwkxFkZq8Y6IOKkpJOg2hCajDmRTOZFfv7kZERs+wCD507"
    "sxrxHEdmaeyBZjS7vJZp60DQk7lR3FaBPTojh0SdrZm7EpJYveiDBhdSCBPmBQXJ75oZi+"
    "mF0cZhJRNNO0SzRFxceG1yDETAn3iQwsSgQ/PptABuiIUfZ5gxy/t3/w7uD9m7cH7+ZRUG"
    "nEUXcZ98XYmMt2wEDUQ8JLaYnFkr8LzI6nwNdDU31y6PiE8+gSUC/KzgUPJobEYVP+5+Fe"
    "BbLv/cvjT/3LV4d72xJdigq6AOE6nBYOmwhpf+8plHivPKYpCKbQNj0QBPfU19yM5cA0rs"
    "2gSwwpuzQhPQe83uHhE+DxXnl4KDB5wkR3mvvxiFIMASnJY6pfjtmEOz4XtMUWXApaBaOj"
    "0ehMTDq4xYhBNZelsCwfinBMwIq0TngLQy7U48p65njZsetu8qOlO47HYI8InsXLUAFzPD"
    "wfXI37519FJO6MM5WI+uOBaHn1dltSoAFzfOmVOox/GuK6IGTUJPTeBLaSeBJrElxmcULP"
    "XnJxsp7d4qy8OHICQi9d3ygaQBgmwLq5B75tZlrSReRJONZyuVwU+51+uYQYSDjFpYoF40"
    "hco52rNE+2XmJVYdEeLaNVbHJ7bt4CCHDkrMXYYqSYx1ef2qEUxQVtnTRVymsv6tQp7A1R"
    "2HXVdbPKemOUjzp6gdYYPpRsr5zbUtDibbT+xKN9HAx+jDNPgrPRxUdpzPLyfGRp9tUJtJ"
    "ALsB7Wwif/UI2cdmPndu6zCmYng+Phef+MVyM7ve2sakx23EGhTgkYtW5qJLJF/8dzWVPA"
    "9lbNZa8XOez9UllN0do8NIf6szqZTPX5z7JZV5q0Rv12pUmLF2fF0sTkWd5toj4Z8uu0c7"
    "lepEaJajZNhbIo5srrk7Rm7KqT9lcnjDKATeDSkOiyYZWazLt2olLoGsBCTUIqF0mpx/ok"
    "kuFBYgssjemkp7wr6BVoocDk6QOK4Iop/JHjbsVxjefddfNYswfeccxLCJesZwPCpV01c8"
    "M6JZl6pYrsJH5rVGQn8Vu8OPEEsp8cmLVUmuKxvsOXl1JrhWooS66I7ZT6EDnkC5xJekM+"
    "D0C053y5T3jaR62s2OFmH9wvxL66IXh40cNNyqz+1XH/ZGDMuwqyDRWkZFJWRSbAHqkk0w"
    "Xqysl2JKidinLyNgSEIaY5Ji5lprpsVnZv7nS9e5mzYt3difHW6L2iGI/zeJ1EqrpsVlJY"
    "LqOqqUB+3lEPV9bp3wdWoZFpckK9okjewM+W8ipZvYn0Mlmz8RpAp3zGtLnwsrdU3SrjOa"
    "V1H/In/9TQ6Oq4pVJUg7RPp6dbkcyq9PQd9APtF1HlLxQUl//sowux6WuAirtvJqSl/z2D"
    "X5VB3bu+z1ejixKJnLrkYH0jPIhfNrLYzhZGAfvdTnQVpETUeckrbEc6lbHOfD//C8ctC6"
    "k="
)
