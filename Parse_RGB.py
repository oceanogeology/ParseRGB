import os
import logging
import time
import datetime
try:
    import numpy as np
except BaseException:
    os.system('pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy')
    import numpy as np
try:
    from scipy import interpolate
except BaseException:
    os.system('pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple scipy')
    from scipy import interpolate
try:
    import pylab as pl
except BaseException:
    os.system('pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib')
    import pylab as pl
try:
    from xlwt import *
except BaseException:
    os.system('pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple xlwt')
    from xlwt import *
try:
    import cv2
except BaseException:
    os.system('pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python')
    import cv2
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def get_curr_time():
    return (datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

logging.info('program started...')
time.sleep(1)
cur_path = os.path.abspath(__file__)
cur_path = '\\'.join(cur_path.split('\\')[:-1])
print('Input image name only need to input name, not include the directory path')
getvalue = input("input image name and output num(use ',' seperate)>>>:")
img_name = getvalue.split(',')[0].strip()
img_root = os.path.join(cur_path, img_name)
assert os.path.exists(img_root), 'img not in {}'.format(cur_path)
img = cv2.imread(img_root)
if img is None:
    img = cv2.imread(img_name)
    if img is None:
        raise ValueError("image read error")
if ',' in getvalue:
    num = int(getvalue.split(',')[1].strip())
else:
    num = img.shape[1]
img_h, img_w, _ = img.shape
img_ori = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_shape = img.shape
if img_w >= img_h:
    target_size = 1920
else:
    target_size = 1080
img_scale = target_size / np.max(img_shape[0:2])
img_scale = (img_scale, img_scale)
img_draw = cv2.resize(img, None, None, fx=img_scale[1], fy=img_scale[0])
if img_draw.shape[0] > 1080:
    target_size = 1080
    img_scale = target_size / img_shape[0]
    img_scale = (img_scale, img_scale)
    img_draw = cv2.resize(img, None, None, fx=img_scale[1], fy=img_scale[0])

height, width, _ = img_draw.shape
drawing = False
mode = 0
iy = -1
ix1 = -1
ix2 = -1
count1 = 0
count2 = 0
color = (255, 255, 255)
count_line1 = 0
count_line2 = 0
p1x1, p1y1, p1x2, p1y2 = -1, -1, -1, -1
p2x1, p2y1, p2x2, p2y2 = -1, -1, -1, -1
img_ori1 = None
img_ori2 = None
ori1_ix = None
ori2_ix = None


def nothing(x):
    pass

def draw_line1(event, x, y, flags, param):
    global count_line1, color, ori1_ix
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        count_line1 += 1
        if drawing:
            if count_line1 == 1:
                ori1_ix, _ = x, y
                cv2.line(img_ori1, (ori1_ix, 0), (ori1_ix, img_ori1.shape[0] - 1), color, 1)
            else:
                raise ValueError("Wrong Operation In draw_line1")


def draw_line2(event, x, y, flags, param):
    global count_line2, color, ori2_ix
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        count_line2 += 1
        if drawing:
            if count_line2 == 1:
                ori2_ix, _ = x, y
                cv2.line(img_ori2, (ori2_ix, 0), (ori2_ix, img_ori2.shape[0] - 1), color, 1)
            else:
                raise ValueError("Wrong Operation In draw_line2")

def draw_line(event, x, y, flags, param):
    color = (255, 255, 255)
    global iy, drawing, width, height, count1, count2, ix1, ix2, p1x1, p1y1, p1x2, p1y2, p2x1, p2y1, p2x2, p2y2, \
        img_ori, img_scale, img_ori1, img_ori2, ori1_ix, ori2_ix
    if mode == 2 and event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        count2 += 1
        if drawing:
            if count2 == 1:
                p1x1, p1y1 = x, y
            elif count2 == 3:
                p2x1, p2y1 = x, y
            elif count2 == 2:
                cv2.rectangle(img_draw, (p1x1, p1y1), (x, y), (190, 255, 0))
                p1x2, p1y2 = x, y
                img_ori1 = img_ori[int(p1y1 / img_scale[1]):int(p1y2 / img_scale[1]), int(p1x1 / img_scale[1]):int(p1x2 / img_scale[1])]
            elif count2 == 4:
                cv2.rectangle(img_draw, (p2x1, p2y1), (x, y), (190, 255, 0))
                p2x2, p2y2 = x, y
                img_ori2 = img_ori[int(p2y1 / img_scale[1]):int(p2y2 / img_scale[1]), int(p2x1 / img_scale[1]):int(p2x2 / img_scale[1])]
                if img_ori1 is not None and img_ori2 is not None:
                    cv2.namedWindow('img_ori1')
                    cv2.namedWindow('img_ori2')
                    cv2.setMouseCallback('img_ori1', draw_line1)
                    cv2.setMouseCallback('img_ori2', draw_line2)
                    while True:
                        cv2.imshow('img_ori1', img_ori1)
                        cv2.imshow('img_ori2', img_ori2)
                        k1 = cv2.waitKey(1) & 0xFF
                        if k1 == ord('q'):
                            cv2.destroyWindow('img_ori1')
                            cv2.destroyWindow('img_ori2')
                            break

    elif mode == 1 and event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        if drawing:
            count1 += 1
            if count1 == 1:
                _, iy = x, y
                cv2.line(img_draw, (0, iy), (width - 1, iy), color, 1)
                if ori1_ix is not None and ori2_ix is not None:
                    ix1 = int((int(p1x1 / img_scale[1]) + ori1_ix) * img_scale[1])
                    ix2 = int((int(p2x1 / img_scale[1]) + ori2_ix) * img_scale[1])
                    cv2.line(img_draw, (ix1, 0), (ix1, height - 1), color, 1)
                    cv2.line(img_draw, (ix2, 0), (ix2, height - 1), color, 1)
                    count1 = 9999
            elif count1 == 2 or count1 == 3:
                ix, _ = x, y
                cv2.line(img_draw, (ix, 0), (ix, height - 1), color, 1)
            else:
                raise ValueError("Wrong Operation In draw_line")
            if count1 == 2:
                ix1 = ix
            elif count1 == 3:
                ix2 = ix

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_line)
while True:
    cv2.imshow('image', img_draw)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('p'):
        mode = 1
    elif k == ord('r'):
        mode = 2
    elif k == 27:
        break

y = int(iy / img_scale[1])
x1 = int(ix1 / img_scale[1])
x2 = int(ix2 / img_scale[1])
getcm = input("input__cm in img_ori1, input__cm in img_ori2. (use ',' seperate)>>>:")
cm1 = float(getcm.split(',')[0].strip())
cm2 = float(getcm.split(',')[1].strip())
assert cm1 < cm2, "Image direction is not satisified!!!"
B, G, R = img[y, x1:x2 + 1, :][:, 0], img[y, x1:x2 + 1, :][:, 1], img[y, x1:x2 + 1, :][:, 2]
Gray = img_gray[y, x1:x2 + 1]
All = [R, G, B, Gray]
label = ['R', 'G', 'B', 'Gray']
x = np.arange(x1, x2 + 1)
x = np.linspace(cm1, cm2, len(x))
xnew = np.linspace(cm1, cm2, num)
All_inter = []
for k in range(4):
    f = interpolate.interp1d(x, All[k], kind='slinear')
    All_inter.append(f(xnew))
if num < 65536:
    file = Workbook(encoding='utf-8')
    table = file.add_sheet('RGB')
    for k in range(5):
        if k == 0:
            for i in range(num):
                table.write(i, k, xnew[i])
        else:
            pl.plot(xnew, All_inter[k - 1], label=label[k - 1])
            for i in range(num):
                table.write(i, k, int(All_inter[k - 1][i]))
    file.save('%s_%s.xls' % (img_name.split('.')[0], get_curr_time()))
    pl.legend(['R', 'G', 'B', 'Gray'])
    pl.show()
else:
    fname = '%s_%s.txt' % (img_name.split('.')[0], get_curr_time())
    with open(fname, 'w') as f:
        for i in range(num):
            string = str(xnew[i]) + ',' + str(int(All_inter[0][i])) + ',' + str(int(All_inter[1][i])) + ',' + \
                     str(int(All_inter[2][i])) + ',' + str(int(All_inter[3][i])) + '\n'
            f.write(string)
logging.info('program ended...')
