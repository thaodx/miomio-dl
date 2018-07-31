# -*- coding: utf-8 -*-
# Miomio.TV video downloader by thaodx@gmail.com
# Dependency: Python 2.*

import sys, requests, re, urllib, os

def make_folder_to_save(path):
	try:
		if not os.path.exists(path):
			os.makedirs(path)
	except Exception, e:
		print e
		pass

def save_file_to_local(content, path, file_name):
	try:
		make_folder_to_save(path)
		open(path + '/' + file_name, 'wb').write(content)

	except Exception, e:
		print '> [ERROR] Could not save file.'
		print e

def main():
	if( len(sys.argv) < 3):
		print '> [ERROR] Not enough parameter. Usage: python miomio-dl.py <VIDEO_URL> <SAVE_PATH> <SAVE_FILE_NAME.mp4>'
		return
	video_link = sys.argv[1]
	print '> Fetching watching page...'
	r = requests.get(video_link)
	matches_player = re.search('.*mioplayer_h5\/player\.php(.*?)".*', r.text)
	if matches_player.group(1):
		print '> Fetching player page...'
		player_url = 'http://www.miomio.tv/mioplayer_h5/player.php' + matches_player.group(1)
		player_html = requests.get(player_url, headers={'referer': video_link}).text
		matches_video_url = re.search('.*\<source src\="(.*?)".*', player_html)
		if matches_video_url.group(1):
			video_url = matches_video_url.group(1)
			print '> Downloading video from url...'
			print '> ...'+video_url
			print '> Please wait...'
			r = requests.get(video_url, headers={'referer': player_url}, allow_redirects=True)
			if r.status_code < 300:
				print '> Saving file...'
				save_file_to_local(r.content, sys.argv[2], sys.argv[3])
				print '> File saved to [' + (sys.argv[2] + '/' + sys.argv[3]) + ']'

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)
