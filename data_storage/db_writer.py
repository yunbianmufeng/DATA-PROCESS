import argparse
import json
import mysql.connector
import psycopg2


def write_to_mysql(input_file, db_host, db_user, db_password, db_name):
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()

        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 假设数据是包含多个字典的列表，每个字典代表一条记录
        for item in data:
            columns = ', '.join(item.keys())
            values = ', '.join(['%s'] * len(item))
            query = f"INSERT INTO your_table_name ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(item.values()))

        # 提交事务
        conn.commit()
        print(f"数据已成功写入 MySQL 数据库 {db_name}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except mysql.connector.Error as e:
        print(f"MySQL 数据库错误: {e}")
    except Exception as e:
        print(f"处理文件或数据库操作时出现错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def write_to_postgres(input_file, db_host, db_user, db_password, db_name):
    try:
        # 连接到 PostgreSQL 数据库
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()

        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 假设数据是包含多个字典的列表，每个字典代表一条记录
        for item in data:
            columns = ', '.join(item.keys())
            values = ', '.join(['%s'] * len(item))
            query = f"INSERT INTO your_table_name ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(item.values()))

        # 提交事务
        conn.commit()
        print(f"数据已成功写入 PostgreSQL 数据库 {db_name}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except psycopg2.Error as e:
        print(f"PostgreSQL 数据库错误: {e}")
    except Exception as e:
        print(f"处理文件或数据库操作时出现错误: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def write_to_db(input_file, db_type, db_host, db_user, db_password, db_name):
    if db_type == 'mysql':
        write_to_mysql(input_file, db_host, db_user, db_password, db_name)
    elif db_type == 'postgres':
        write_to_postgres(input_file, db_host, db_user, db_password, db_name)
    else:
        print("不支持的数据库类型，请使用 'mysql' 或 'postgres'。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='数据写入数据库脚本')
    parser.add_argument('--input_file', required=True, help='要存储的数据文件路径。')
    parser.add_argument('--db_type', required=True, help='数据库类型（如 mysql、postgres 等）。')
    parser.add_argument('--db_host', required=True, help='数据库主机地址。')
    parser.add_argument('--db_user', required=True, help='数据库用户名。')
    parser.add_argument('--db_password', required=True, help='数据库密码。')
    parser.add_argument('--db_name', required=True, help='数据库名称。')
    args = parser.parse_args()

    input_file = args.input_file
    db_type = args.db_type
    db_host = args.db_host
    db_user = args.db_user
    db_password = args.db_password
    db_name = args.db_name

    write_to_db(input_file, db_type, db_host, db_user, db_password, db_name)
