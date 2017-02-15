import requests
import json

object_detect_url = "https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject"
api_key = "-w8bVAmjgdhbp3KHYlIqgcJjmMUIbosD"
api_secret = "hOyZQtIFJlIHwhgFHEDX41jXfY8Q8FUn"
image_url = [
	"http://dy-public.oss-cn-shenzhen.aliyuncs.com/wcy/fullsizeoutput_7f1.jpeg"]

for image in image_url:
	r = requests.post(object_detect_url, data = {'api_key':api_key, 'api_secret': api_secret, 'image_url': image})
	data = json.loads(r.text)
	print(image)
	print(data['time_used'])
	print(data['scenes'])
	print(data['objects'])