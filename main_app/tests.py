import qrcode
def new_qrcode(data):
    # 构建二维码
    img = qrcode.make(data)
    # 显示图片格式，为qrcode.image.pil.PilImage
    print(type(img))
    # 保存图片 
    img.save("test2.png")

new_qrcode({
    'first data':1,
    'second data':'',
    'third data':'这里是第三个信息',
    'fourth data':'http://www.baidu.com',
})