# -*- coding: utf-8 -*-
"""
操作数据库
"""
import asyncio
import aiomysql
from contextlib import asynccontextmanager


def format_sql(words: str):
    return words.replace("\'", "\\\'")


"""
create table test.urls
(
    id           bigint auto_increment
        primary key,
    download_url varchar(255) not null,
    file_name    varchar(255) not null,
    refer        varchar(255) not null
);

"""


def __init__():
    pass


@asynccontextmanager
async def conn(host, user, password, port):
    mydb = await aiomysql.connect(
        host=host,  # 数据库主机地址
        user=user,  # 数据库用户名
        password=password,  # 数据库密码
        port=port
        # charset="utf-8"
    )
    yield mydb
    mydb.close()


class _BaseSQLclient:
    def __init__(self, host, user, password, port, db: str):
        """

        :param host:
        :param user:
        :param password:
        :param port:
        :param db: 连接的数据库名字
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db

    async def execute(self, sql: str):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                await conn.commit()


class SQLclient(_BaseSQLclient):
    def __init__(self, host, user, password, port, db: str):
        super().__init__(host, user, password, port, db)

    @classmethod
    async def create(cls, host, user, password, port, db):
        """
        real的构造方法
        :param host:
        :param user:
        :param password:
        :param port:
        :param db:
        :return:
        """
        self = cls(host, user, password, port, db)
        self.pool = await aiomysql.create_pool(host=self.host, port=self.port, user=self.user,
                                               password=self.password, db=self.db, charset="utf8", autocommit=True)
        return self

    async def insert(self, download_url, file_name, refer):
        download_url = format_sql(download_url)
        file_name = format_sql(file_name)
        refer = format_sql(refer)
        sql = "insert into urls (download_url,file_name,refer) values (\'{0}\',\'{1}\',\'{2}\')".format(download_url,
                                                                                                        file_name,
                                                                                                        refer)
        print(sql)
        print("")
        await self.execute(sql)

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()


async def main():
    """
    直接运行此文件就是测试
    :return:
    """
    client = await SQLclient.create("dbhost", "dbuser", "dbpasswd", 3306, "db")
    await client.insert(
        "https://konachan.com/sample/2091aebfcbe90bcbb61ddf08cbc368a6/Konachan.com%20-%20281976%20sample.jpg",
        "blush-censored-footjob-gray_hair-lambda-original-p",
        "https://konachan.com/post?page=7&tags=footjob")
    await client.insert("haha", "hanpi", "gu")
    await client.insert("g", "f", "l")


if __name__ == "__main__":
    asyncio.run(main())
