from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import os
import requests
from datetime import datetime, timezone, timedelta
from dateutil import tz

project_path = os.path.dirname(os.path.abspath(__file__))
url = f'file://{project_path}/index_result.html'

if not os.path.exists("output"):
    os.makedirs("output")

img_path = os.path.join("output", 'screenprint.png')

if os.path.exists(img_path):
    os.remove(img_path)

background_urls = {
    "sunnyImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Sunny.webp",
    "sunnyNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Clear Night.webp",
    "rainImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Rain 2.webp",
    "rainNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Rain 1.webp",
    "snowImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Snow 2.webp",
    "rainNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Snow 1.webp",
    "dustImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Duststorm 2.webp",
    "dustNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Duststorm 1.webp",
    "cloudyImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Cloudy 2.webp",
    "cloudyNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Cloudy 1.webp",
    "stormImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Thunderstorms 2.webp",
    "stormNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Thunderstorms 1.webp",
    "fogImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Light fog.webp",
    "fogNightImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/Hazy Night.webp",
    "sunnySunsetImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/partlysunny_sunset.webp",
    "cloudySunsetImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/mostcloudy_sunset.webp",
    "hazyImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/hazy_day.webp",
    "partlySunnyImageUrl": "https://assets.msn.cn/weathermapdata/1/static/images/webps/v1.0/partlysunny_day.webp"
}

weather_icons = {
    "d000": "SunnyDayV3",
    "d100": "MostlySunnyDay",
    "d200": "D200PartlySunny",
    "d210": "D210LightRainShowers",
    "d211": "D211LightRainSowShowers",
    "d212": "D212LightSnowShowers",
    "d220": "LightRainShowerDay",
    "d221": "D221RainSnowShowers",
    "d222": "SnowShowersDayV2",
    "d240": "D240Tstorms",
    "d300": "MostlyCloudyDayV2",
    "d310": "D310LightRainShowers",
    "d311": "D311LightRainSnowShowers",
    "d312": "LightSnowShowersDay",
    "d320": "RainShowersDayV2",
    "d321": "D321RainSnowShowers",
    "d322": "SnowShowersDayV2",
    "d340": "D340Tstorms",
    "d400": "CloudyV3",
    "d410": "LightRainV3",
    "d411": "RainSnowV2",
    "d412": "LightSnowV2",
    "d420": "HeavyDrizzle",
    "d421": "RainSnowV2",
    "d422": "Snow",
    "d430": "ModerateRainV2",
    "d431": "RainSnowV2",
    "d432": "HeavySnowV2",
    "d440": "ThunderstormsV2",
    "d500": "MostlyCloudyDayV2",
    "d600": "FogV2",
    "d605": "IcePelletsV2",
    "d705": "BlowingHailV2",
    "d905": "BlowingHailV2",
    "d907": "Haze",
    "d900": "Haze",
    "n000": "ClearNightV3",
    "n100": "MostlyClearNight",
    "n200": "PartlyCloudyNightV2",
    "n210": "N210LightRainShowers",
    "n211": "N211LightRainSnowShowers",
    "n212": "N212LightSnowShowers",
    "n220": "LightRainShowerNight",
    "n221": "N221RainSnowShowers",
    "n222": "N222SnowShowers",
    "n240": "N240Tstorms",
    "n300": "MostlyCloudyNightV2",
    "n310": "N310LightRainShowers",
    "n311": "N311LightRainSnowShowers",
    "n312": "LightSnowShowersNight",
    "n320": "RainShowersNightV2",
    "n321": "N321RainSnowShowers",
    "n322": "N322SnowShowers",
    "n340": "N340Tstorms",
    "n400": "CloudyV3",
    "n410": "LightRainV3",
    "n411": "RainSnowV2",
    "n412": "LightSnowV2",
    "n420": "HeavyDrizzle",
    "n421": "RainSnowShowersNightV2",
    "n422": "N422Snow",
    "n430": "ModerateRainV2",
    "n431": "RainSnowV2",
    "n432": "HeavySnowV2",
    "n440": "ThunderstormsV2",
    "n500": "PartlyCloudyNightV2",
    "n600": "FogV2",
    "n605": "BlowingHailV2",
    "n705": "BlowingHailV2",
    "n905": "BlowingHailV2",
    "n907": "Haze",
    "n900": "Haze",
    "xxxx1": "WindyV2",
}


def wait_element_load(driver, element_xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
    finally:
        driver.find_element_by_xpath(element_xpath).click()


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver


def get_CST_time():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(timezone(timedelta(hours=8)))

def get_screenprint():
    driver = init_driver()

    # Load the page
    driver.get(url)

    # Get the element
    element_xpath = '/html/body'
    driver.get_screenshot_as_file(img_path)
    e = driver.find_element(By.XPATH, element_xpath)
    left = e.location['x']
    top = e.location['y']
    right = e.location['x'] + 612
    bottom = e.location['y'] + 270

    # Crop the image
    im = Image.open(img_path)
    im = im.crop((left, top, right, bottom))
    if os.path.exists(img_path):
        os.remove(img_path)
    im.save(img_path)
    os.rename(img_path, os.path.join("output", get_CST_time().strftime("%Y-%m-%d") + '.png'))


def get_current_weather_info(lat=22.7897499, lon=114.4561802):
    msn_api = "https://api.msn.cn/weatherfalcon/weather/overview?&units=C&wrapodata=false&nowcastingv2=true" \
              "&getCmaAlehttps://api.msn.cn/weatherfalcon/weather/overview?apikey" \
              "=j5i4gDqHL6nGYwx5wi5kRhXjtf2c5qgFX9fzfk0TOo&activityId=AA6FA6D6-5BD8-42AA-9764-27CF4BD5CA9C&ocid" \
              "=msftweather&cm=zh-cn&it=web&user=m-005CC905B8116B0C112EDB62B9526AA7&units=C&appId=9e21380c-ff19-4c78" \
              "-b4ea-19558e93a5d3&wrapodata=false&includemapsmetadata=true&nowcastingv2=true&usemscloudcover=true" \
              "&cuthour=true&getCmaAlert=true&regioncategories=alert," \
              "content&feature=lifeday&includenowcasting=true&nowcastingapi=2&lifeDays=2&lifeModes=50&distanceinkm=0" \
              "&regionDataCount=20&orderby=distance&days=10&pageOcid=prime-weather::weathertoday-peregrine&source" \
              "=weather_csr&fdhead=prg-1sw-wxlfrc&region=cn&market=zh-cn&locale=zh-cn&lat={lat}&lon={lon}".format(
        lat=lat, lon=lon)
    response = requests.get(msn_api)
    if response.status_code == 200:
        return response.json()['responses'][0]['weather'][0]["current"]
    else:
        return None


def get_background_by_icon(icon):
    icon_to_background_key = {
        "d000": "sunnyImageUrl",
        "d100": "partlySunnyImageUrl",
        "d200": "partlySunnyImageUrl",
        "d210": "rainImageUrl",
        "d211": "rainImageUrl",
        "d212": "snowImageUrl",
        "d220": "rainImageUrl",
        "d221": "snowImageUrl",
        "d222": "snowImageUrl",
        "d240": "stormImageUrl",
        "d300": "cloudyImageUrl",
        "d310": "rainImageUrl",
        "d311": "snowImageUrl",
        "d312": "snowImageUrl",
        "d320": "rainImageUrl",
        "d321": "rainImageUrl",
        "d322": "snowImageUrl",
        "d340": "stormImageUrl",
        "d400": "cloudyImageUrl",
        "d410": "rainImageUrl",
        "d411": "snowImageUrl",
        "d412": "snowImageUrl",
        "d420": "HeavyDrizzle",
        "d421": "rainImageUrl",
        "d422": "snowImageUrl",
        "d430": "rainImageUrl",
        "d431": "snowImageUrl",
        "d432": "snowImageUrl",
        "d440": "stormImageUrl",
        "d500": "stormImageUrl",
        "d600": "fogImageUrl",
        "d605": "stormImageUrl",
        "d705": "stormImageUrl",
        "d905": "stormImageUrl",
        "d907": "hazyImageUrl",
        "d900": "hazyImageUrl",
        "n000": "sunnyNightImageUrl",
        "n100": "cloudyNightImageUrl",
        "n200": "sunnyNightImageUrl",
        "n210": "rainNightImageUrl",
        "n211": "rainNightImageUrl",
        "n212": "snowNightImageUrl",
        "n220": "snowNightImageUrl",
        "n221": "snowNightImageUrl",
        "n222": "snowNightImageUrl",
        "n240": "stormNightImageUrl",
        "n300": "cloudyNightImageUrl",
        "n310": "rainNightImageUrl",
        "n311": "rainNightImageUrl",
        "n312": "rainNightImageUrl",
        "n320": "rainNightImageUrl",
        "n321": "snowNightImageUrl",
        "n322": "snowNightImageUrl",
        "n340": "stormNightImageUrl",
        "n400": "cloudyNightImageUrl",
        "n410": "rainNightImageUrl",
        "n411": "snowNightImageUrl",
        "n412": "snowNightImageUrl",
        "n420": "rainNightImageUrl",
        "n421": "snowNightImageUrl",
        "n422": "snowNightImageUrl",
        "n430": "rainNightImageUrl",
        "n431": "snowNightImageUrl",
        "n432": "snowNightImageUrl",
        "n440": "stormNightImageUrl",
        "n500": "cloudySunsetImageUrl",
        "n600": "fogNightImageUrl",
        "n605": "stormNightImageUrl",
        "n705": "stormNightImageUrl",
        "n905": "stormNightImageUrl",
        "n907": "hazyImageUrl",
        "n900": "hazyImageUrl",
        "xxxx1": "partlySunnyImageUrl",
    }
    if icon in icon_to_background_key:
        return background_urls[icon_to_background_key[icon]]
    else:
        return 'file://{project_root}/black_background.png'


if __name__ == '__main__':
    st = time.time()
    weather_info = get_current_weather_info()
    if weather_info:
        info = {
            "background_img_url": get_background_by_icon(weather_info["symbol"]),
            "weather_icon_url": "https://assets.msn.cn/weathermapdata/1/static/weather/Icons/taskbar_v3/Condition_Card/{}.svg".format(
                weather_icons[weather_info["symbol"]]),
            "temp": int(weather_info["temp"]),
            "temp_feel": int(weather_info["feels"]),
            "cap": weather_info["cap"],
            "aqi": int(weather_info["aqi"]),
            "windir": weather_info['pvdrWindDir'],
            "windspd": weather_info['pvdrWindSpd'],
            "rh": int(weather_info['rh']),
            "vis": float(weather_info['vis']),
            "dewpt": int(weather_info['dewPt']),
            "baro": int(weather_info['baro']),
            "nowtime": get_CST_time().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open("index.html", encoding="utf-8") as f:
            file = f.read()
            for key, value in info.items():
                file = file.replace("{" + key + "}", str(value))
        with open("index_result.html", "w", encoding="utf-8") as f:
            f.write(file)

        get_screenprint()

    print("Time cost: {}".format(time.time() - st))
