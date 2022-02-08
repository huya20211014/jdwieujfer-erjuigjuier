import os

if __name__ == '__main__':
    post_global = ['.mp4', '.jpg', '.jpeg', '.png', '.mov', '.MP4', '.JPG', '.JPEG', '.PNG', '.gif', '.GIF']
    mp4files = []
    for mp4_ in os.listdir('.'):
        for post_ in post_global:
            if post_ in mp4_:
                mp4files.append(mp4_)
                break
    pre_ = input('请输入前缀')

    for mp4_ in mp4files:
        nsrc = mp4_
        ndet = '{}_{}'.format(pre_, nsrc)
        print(nsrc, '-->', ndet)
        os.rename(nsrc, ndet)
