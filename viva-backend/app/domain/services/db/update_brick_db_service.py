import logging
import time

from infrastructure.database.brick_repository import BrickRepository



logging.basicConfig(filename='update_brick_db.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

db_url = 'postgresql://root:root@localhost/root'
repo = BrickRepository(db_url)
ids = repo.get_all_ids()
logging.warning("begin to process, ids:" + str(ids))
for index, id in enumerate(ids):
    try:
        word = repo.get_brick_by_id(id)
        if word.pronunciation == None:
            word.update_fields()
            print(word)
            repo.update_brick(word)
            logging.warning("finish-" + word.spelling)

    except Exception as e:
        logging.error(f"Error processing ID {id}: {e}")
        continue  # 发生异常时忽略当前ID，继续处理下一个ID

    # # 每处理50个id后暂停30秒
    # if (index + 1) % 50 == 0:
    #     logging.warning("Processed 50 IDs, sleeping for 10 seconds.")
    #     time.sleep(10)  # 睡眠
    