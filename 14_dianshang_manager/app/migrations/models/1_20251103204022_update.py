from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `products` ADD `category` VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `products` DROP COLUMN `category`;"""


MODELS_STATE = (
    "eJztmlFvmzoUx79KxdMqdVWb227TfUvTdMvWNlObXU2bJuSAS6wam4JZG0357rMNxAYMK0"
    "nakjvekmMf7POzOf4f4JflUxfiaP9LBEPr351fFgE+5D9y9r0dCwSBsgoDA1MsO8a8h7SA"
    "acRC4DBuvAE4gtzkwsgJUcAQJdxKYoyFkTq8IyKeMsUE3cXQZtSDbCYn8v0HNyPiwgcYZX"
    "+DW/sGQezm5olcMba022weSNuIsDPZUYw2tR2KY5+ozsGczShZ9kaECasHCQwBg+LyLIzF"
    "9MXs0jCziJKZqi7JFDUfF96AGDMt3EcycCgR/PhsIhmgJ0Y55A1y/N7h0dujd/+8OXq7SI"
    "JSESfdZdyXE2sh2wEDSQ8JT9ESiyV/l5gNZiA0Q9N9Cuj4hIvoMlAvys4HDzaGxGMz/vf4"
    "oAbZf/2rwYf+1avjg12JTqGCPkC4CaelwzZCOjx4DCXeq4hpBqIZdO0ARNE9DQ03YzUwg+"
    "tm0GUGxU4lpKeA1zs+fgQ83qsID0U2T5jop+F+PKEUQ0Aq8pjuV2A25Y5PBW25BVeCVsPo"
    "ZDw+F5OO7jBiUM9lCpYTQhGODViZ1ilvYciHZlx5zwIvN3Xdz360dMfxGNwxwfN0GWpgTk"
    "YXw+tJ/+KziMSfc6YSUX8yFC2v3uxKCjRiXii9lMPkmyWuC2JGbULvbeBqiSezZsHlFicO"
    "3BUXJ+/ZLc7aiyMnIPTSza2mAYRhCpzbexC6dq5FLSJPwqmWK+Si1O/s0xXEQMIpL1UqGM"
    "fiGu1cpUW29TKrDov2aBWtcpPf84sWQIAnZy3GFiOlPD6H1I2lKC5p66ypVl4HSadOYW+J"
    "wm6qrjerrLdG+eijl2hN4EPF9iq4rQQt3UbPn3iMx8Hw6yR3EpyPL99LY55XECLHsK9OoY"
    "N8gM2wlj7FQzVx2k+d27nPapidDgeji/45r0b2ert51ZjtuKNSnRIx6tw2SGTL/n/OZZsC"
    "drBuLnu9zGHvVspqmtbmoXk0nDfJZLrPX5bNutKkNeq3K01avDhrliY2z/L+JuqTEb9OO5"
    "frRWqUpGYzVCjLYq66PlE1Y1edtL86YZQBbAOfxsSUDevUZNG1E5VC1wAWGxJStUhSHs8n"
    "kawAEldg2ZhOesy7gl6JVqeSWnMQdyqpxYuTTiD/1tZudNBpHs9Xv77UgVcSlHlyZWxnNI"
    "TII5/gXNIb8XkAYnxUUvgKon3UqvQiN4fgfqmX9A3Bw+NBweRsG/SvB/3TobXoRHgbRLhk"
    "UiXEM2B/EONqgTpF3o4EVafI72JAGGKGJ22VzHSX7crum3tA2T0PX7N06cR4a/ReWYyneb"
    "xJItVdtisprJZR9VQg35A3w5V3+v8Dq9HINHvIt6ZI3sIvP4oqWb+JzDLZsPE2gE77EmR7"
    "4eVvqaZVxlNK6z7kJ//MMujqtKVWVAPVp9PTrUhmdXr6Jwwj40cl1c9kNZe/7L212PQNQK"
    "XdtxPSyl+486syaHpd8vF6fFkhkZVLAdYXwoP47iKH7e1gFLEf7URXQ0pEXZS8wnZiUhnP"
    "me8XvwFrUiby"
)
