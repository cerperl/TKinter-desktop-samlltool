#随机狗狗图背景
import requests
import os

def download_random_dog(path="dog.jpg"):
    url = 'https://dog.ceo/api/breeds/image/random'
    img_url = requests.get(url).json()["message"]


    img_data = requests.get(img_url).content
    with open(path, "wb") as f:
        f.write(img_data)
    
    print("dog image saved to:", os.path.abspath(path))
    return path  #返回本地文件路径

if __name__ == "__main__":
    download_random_dog()
