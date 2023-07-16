import pytube

link = 'https://www.youtube.com/watch?v=h3-naWSga9I&ab_channel=CodeWithIshraq'

yt = pytube.YouTube(link)

yt.streams.get_highest_resolution().download()

print('Downloaded', link)