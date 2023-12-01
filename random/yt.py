from pytube import YouTube

def download(link):
    path="C:/Users/freef/Downloads"
    yt=YouTube(link)
    ys=yt.streams.get_highest_resolution()
    print("Downloading...")
    ys.download(path)
    print("Down load completed!!")
    
