# BeatCET6
Identify marked words in photo.  
For example, if input is a photo like below:    
![sample](https://cloud.githubusercontent.com/assets/11898075/20553888/e82d351a-b192-11e6-83bf-306bff76f907.png)  
The program will output:
`water: 水`

## Introduction
BeatCET6 aims to identify the words marked in photo, and translate them into chinese.

## Example
1. original photo:
![a5](https://cloud.githubusercontent.com/assets/11898075/20553416/7dc13b7a-b18f-11e6-93e2-d5ad62ebce4f.jpg)

2. after processed:
![targets](https://cloud.githubusercontent.com/assets/11898075/20553508/1f9b250a-b190-11e6-82ff-63f314dc3873.jpg)

3. result:  
![image](https://cloud.githubusercontent.com/assets/11898075/20553486/f731f2c4-b18f-11e6-98bf-c29f121673fb.png)

## Usage
1. put your image to the dir that a.py lying
2. change origin_path in a.py config part
3. change r,g,b that match your mark color
4. `python a.py`

## Doc
See [Wiki](https://github.com/kyshel/BeatCET6/edit/wiki)

## Powered By (Require)
- [python-pillow/Pillow](https://github.com/python-pillow/Pillow)
- [sirfz/tesserocr](https://github.com/sirfz/tesserocr)
- [terryyin/google-translate-python](https://github.com/terryyin/google-translate-python)

## Credits
Made with ❤ by [Kyshel](https://github.com/kyshel)  
MIT License  
