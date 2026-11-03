import psutil
import logging
import yaml
import sys

logging.basicConfig(
        filename = 'health.log',
        level = logging.INFO,
        format = '%(asctime)s [%(levelname)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
        )
def load_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"未找到配置文件: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"yaml文件配置错误: {e}")
        sys.exit(1)

def check(config):
    thresholds = config.get('thresholds', {})
    cpu = thresholds.get('cpu', 80)
    mem = thresholds.get('memory', 80)
    disk = thresholds.get('disk', 80)
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    print(f"CPU: {cpu_usage}% MEM: {mem_usage}% DISK: {disk_usage}%")
    is_health = True

    if cpu_usage > cpu :
        msg = f"CPU使用过高：{cpu_usage}% (阈值: {cpu}%)"
        print(f"[WARN] {msg}")
        logging.warning(msg)
        is_health = False
    if mem_usage > mem :
        msg = f"内存使用过高: {mem_usage}% (阈值: {mem}%)"
        print(f"[WARN] {msg}")
        logging.warning(msg)
        if_health = False
    if disk_usage > disk:
        msg = f"磁盘使用过高: {disk_usage}% (阈值: {disk}%)"
        print(f"[WARN] {msg}")
        logging.warning(msg)
        is_health = False
    if is_health:
        logging.info(f"巡检正常。CPU={cpu_usage}%, MEMORY={mem_usage}%, DISK={disk_usage}%")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__=="__main__":
    config = load_config()
    check(config)
