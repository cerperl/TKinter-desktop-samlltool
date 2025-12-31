#月相计算
from datetime import datetime, timezone


#月相映射表
MOON_PHASE_MAP = [
    (0.03, "新月"), 
    (0.22, "娥眉月"), 
    (0.28, "上弦月"), 
    (0.47, "盈满月"), 
    (0.53, "满月"), 
    (0.72, "亏凸月"), 
    (0.78, "下弦月"), 
    (0.97, "残月"), 
    (1.01, "新月"), #人为兜底
]


def moon_phase_text(phase:float) -> str:
    for upper, text in MOON_PHASE_MAP:
        if phase <= upper:
            return text
    return "未知月相"


def get_moon_phase():
    #参考新月时间(业界常用标准)
    refrence = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    #距离参考新月的天数
    days = (now - refrence).total_seconds() / 86400

    #朔望月长度
    synodic_month = 29.53058867

    #当前月相
    phase:float = (days % synodic_month) / synodic_month

    return moon_phase_text(phase)

if __name__ == "__main__":
     moon = get_moon_phase()
     print(moon)