from canvas import Canvas
import cv2

# 使用する画像の読み込み
images = []
for i in range(4):
    images.append(cv2.imread(f'images/image{i}.png', cv2.IMREAD_UNCHANGED))

# キャンバスを作成
canvas = Canvas(name='canvas1', H=540, W=720, bg='white')

# キャンバスに画像を新規レイヤーとして追加 (alphaは不透過度)
canvas.add_layer(images[0], name=f'image{0}', alpha=1.0, format='png')
canvas.add_layer(images[1], name=f'image{1}', alpha=0.2, format='png')
canvas.add_layer(images[2], name=f'image{2}', alpha=0.2, format='png')
canvas.add_layer(images[3], name=f'image{3}', alpha=0.2, format='png')

# キャンバスの情報を取得
canvas.info()

# 作成した画像を保存
canvas.save_image('output/result.jpg')