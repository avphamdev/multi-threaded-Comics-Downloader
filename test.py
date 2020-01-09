import requests
import threading
import os
import bs4 as bs


os.makedirs('xkcd', exist_ok=True)  # ?: store comics in ./xkcd


def download_Xkcd(start_comic, end_Comic):
    for url_Number in range(start_comic, end_Comic):
        # TODO:Download the page.
        print('Downloading page https://xkcd.com/%s...' % (url_Number))

        response = requests.get('https://xkcd.com/%s' % (url_Number))
        print(response.status_code)

        soup = bs.BeautifulSoup(response.text, 'html.parser')

        # TODO: Find the URL of the comic image.
        comic_Elem = soup.select('#comic img')
        if comic_Elem == []:
            print('Could not find comic image.')
        else:
            comic_Url = comic_Elem[0].get('src')
            print('Downloading image %s...' % (comic_Url))
            response = requests.get('https:' + comic_Url)
            img_File = open(os.path.join('xkcd', os.path.basename(comic_Url)), 'wb')
            for chunks in response.iter_content(100000):
                img_File.write(chunks)
            img_File.close()


# TODO: Create and start the Thread objects.
download_Threads = []  # ?: a list of all the Thread objects.

for i in range(0, 140, 10):  # TODO: loops 14 times, creates 14 threads
    start = i
    end = i + 9
    if start == 0:
        start = 1  # ?:There is no comic 0, so set it to 1.
    download_Thread = threading.Thread(target=download_Xkcd, args=(start, end))
    download_Threads.append(download_Thread)
    download_Thread.start()

# TODO: Wait for all threads to end.
for thread in download_Threads:
    thread.join()  # ?: Method .join() của Thread object sẽ dừng chương trình tới khi thread đó chạy xong.

print('Done.')


# ?: Tóm lại, multi-threading sẽ giúp chương trình tải hình nhanh hơn.
# ?: Vì ta có nhiều thread cùng một lúc xử lý Network Connection.
# ?: Nếu chỉ xài single-threading, chương trình sẽ phải tải từng ảnh một (lâu hơn)


os.system('pause')
