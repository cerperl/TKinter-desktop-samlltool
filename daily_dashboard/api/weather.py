#每日天气获取(7days)
#api网站
#https://open-meteo.com/en/docs?utm_source=chatgpt.com


import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    #paramas做传递参数给url
    params = {
        "latitude": "28.8359",
        "longitude": "108.766",
        "timezone": "Asia/Shanghai",
        "daily": "temperature_2m_mean,weather_code"
    }

    #返回并处理
    res = requests.get(url, params=params).json()


    #返回天气列表
    tem_list:list[float] = res["daily"]["temperature_2m_mean"]

    #返回天气
    res_weathercode:list[int] = res["daily"]["weather_code"]



    #天气映射表
    weathercode_map = {
        0: "晴天", 
        1: "大致晴朗", 
        2: "局部多云", 
        3: "阴天", 
        45: "有雾", 
        48: "霜雾", 
        51: "细雨", 
        53: "细雨适中", 
        55: "细雨密集", 
        56: "冻毛毛雨", 
        57: "冻毛毛雨(密)", 
        61: "雨(轻)", 
        63: "雨(中)", 
        65: "雨(重)", 
        66: "冻雨(轻)", 
        67: "冻雨(重)", 
        71: "降雪(轻)", 
        73: "降雪(中)", 
        75: "降雪(重)", 
        77: "雪粒", 
        80: "阵雨(轻微)", 
        81: "阵雨(中)", 
        82: "阵雨(剧烈)", 
        85: "小雪阵雨", 
        86: "大雪阵雨", 
        95: "雷暴", 
        96: "雷暴伴轻冰雹", 
        99: "雷暴伴重冰雹", 

    }
    weathercode_list:list[str] = [weathercode_map.get(code, "未知天气") for code in res_weathercode]

    #把每一天的文本塞进去
    result=  []
    for day, (tem, wocde) in enumerate(zip(tem_list, weathercode_list), start=1):
        result.append(f"{tem}°C\t {wocde}")

    return result #返回7条
    

if __name__ == "__main__":
    for line in get_weather():
        print(line)

