from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


# aerich migrate  升级和降级

# 命令 aerich upgrade 执行 async def upgrade 进行升级
async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` ADD `addr` VARCHAR(255) NOT NULL COMMENT '教室' DEFAULT '';"""

# 命令 aerich downgrade 执行 async def downgrade 进行降级
async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` DROP COLUMN `addr`;"""


MODELS_STATE = (
    "eJztmV1vmzAUhv9KxVUndVO+aNLdpdmqdV1bqe2mSW2FDBiCQuzUmLVRxX+fbSAGAgySNq"
    "UTN2l6fGzOefxx3phnZY5N6HqfJi7wlM97zwoCc8i+pOwHewpYLKSVGyjQXeFoxB66Rwkw"
    "KLNZwPUgM5nQM4izoA5GzIp81+VGbDBHB9nS5CPnwYcaxTakU0hYw+09MzvIhE/Qi/9dzD"
    "TLga6ZCtMx+bOFXaPLhbCdInoiHPnTdM3Arj9H0nmxpFOMVt4OotxqQwQJoJAPT4nPw+fR"
    "RVnGGYWRSpcwxEQfE1rAd2ki3YoMDIw4PxZNOA82f8rHXncwHIz6h4MRcxGRrCzDIExP5h"
    "52FAQubpRAtAMKQg+BUXITf9fITaaA5KOL/TPwWMhZeDGqMnqxQeKTS6aUn3LnD/vQZJ8Q"
    "DO98ddDh34+sjlKN6hw8aS5ENp1ylKpawvDX+GrybXy1z7w+8NExW9zhir+ImnphWxDw1W"
    "nNEpy5QQfG7BEQU0u1yBnwqG9CHtfaLBxHPU/OrqALRObr5KP9eR2OstNJqLyIg3gVxdZo"
    "nwhguIeLiK03zXvzrAUgYIuo+bP5k+ITC/vEg7lnWdhSfppJn/Y8a8+zHZxnI92C7AwDHb"
    "0x59lBYkEC0yR1wMb+uwOrKHlYD1X1iAHVwaAxKCkEBjsOtFp7PN3p33u9GSf/S2z3taq6"
    "RnId4wkm0LHRGVwKmqcsKICMvJ0e1YQbOVLzKBbVT2Ym4HFVPTJrhCXJUoM03Kjj68n4y1"
    "clKJYkWxbjKormHKDlDeafFadlC1nz2pWsZFJE8FpGdSRSIVzOQXPlEYqNkBcmgvYMLhMo"
    "oxldzUXUGvaLGumUYN+eJntJEZO7Fphdy8qDoFRTxTnkiKpEesWqyks4tbKqkixQ9cNDJg"
    "XUrhWG00qszSWWemT2Q3G1iRbo9ypIgX6vUAnwprQQWDzmLMdikJF7AzjqBl+To063GRw9"
    "hGts68j7jSXUamurfWu4y40tsfEbu3oiNNGjVaCpW88t5Wd8vdo8flW1Z2JpvJnwTOqo7X"
    "SnvCJ677JTZpJVnSmZnpadKWGZVZ1pTbq97BQIy3Vn/OssR3cmfrgV687E78RWd1YrTtG9"
    "CeyMWt3Z6s6GcGyY7qS1dCdtiu6UW5vBtLo716AbvSYrrO113pJtXtb/05dkY0gcY5pXV6"
    "OW0rIKpE9bVV9wKbx2Jf0DiRftk6o1INHljetAdYo7eCnGtkYNiJH7+wTY7XQqAGRehQBF"
    "W+YKAiMaXQinIX6/vrwouIOQXTIgfyKW4K3pGPRgz3U8et9MrCUUedY86LnnPbhJePvn49"
    "9ZrpMfl8eCAvaoTcQoYoDjeiX25ctL8BfVf0Mc"
)
