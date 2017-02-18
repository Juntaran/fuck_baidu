import os

user_agent_headers = {
    'Referer': "https://www.baidu.com/",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
}

download_block_size = 1024 * 1024 * 5

home_path = os.path.expanduser("~")
app_path = os.path.join(home_path, ".fuck_baidu")

cookie_file_path = os.path.join(app_path, "cookie_file")
download_info_database_file_path = os.path.join(app_path, "info.db")
download_info_table_name = "download_infos"
max_download_task_number = 5
