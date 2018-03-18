import sys
sys.path.append('/home/pi/epaper/')
import epd1in54
import time 
import Image 
import ImageDraw 
import ImageFont

import string
import wifi
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
up = 12
down = 16
pp_select = 20
back = 7
GPIO.setup(pp_select, GPIO.IN)
GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
GPIO.setup(back, GPIO.IN)

def disp_np(artist,album,song,art):
	epd = epd1in54.EPD()
	epd.init(epd.lut_full_update)

	now_playing = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)  # 255: clear the frame
	#album_art=Image.open(art)
	song_sym = Image.open('/home/pi/symbols/bmp/25x25/music-note25.bmp')
	artist_sym = Image.open('/home/pi/symbols/bmp/25x25/person-stalker25.bmp')
	album_sym = Image.open('/home/pi/symbols/bmp/25x25/disc25.bmp')
	play_sym = Image.open('/home/pi/symbols/bmp/25x25/play25.bmp')
	pause_sym = Image.open('/home/pi/symbols/bmp/25x25/pause25.bmp')
	next_sym = Image.open('/home/pi/symbols/bmp/25x25/skip-forward25.bmp')
	prev_sym = Image.open('/home/pi/symbols/bmp/25x25/skip-backward25.bmp')


	draw = ImageDraw.Draw(now_playing)

	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)

	draw.rectangle((0, 14, 200, 15), fill = 0) 		#top icon tray

	now_playing.paste(song_sym,(0,30))			#song symbol
	draw.text((30,30+4), song, font = font, fill = 0)	#song name

	now_playing.paste(artist_sym,(0,60))			#artist symbol
	draw.text((30,60+4), artist, font = font, fill = 0)	#artist name

	now_playing.paste(album_sym,(0,90))			#album symbol
	draw.text((30,90+4), album, font = font, fill = 0)	#album name

	now_playing.paste(pause_sym,(88,150))
	now_playing.paste(next_sym,(130,150))
	now_playing.paste(prev_sym,(46,150))

	#now_playing.paste(album_art,(0,17))		#add album art cover to np page
	
	epd.clear_frame_memory(0xFF)			#display 
	epd.set_frame_memory(now_playing, 0, 0)
	epd.display_frame()

	epd.init(epd.lut_partial_update)		#initialize partial update for play/pause symbol change
	
        epd.set_frame_memory(now_playing, 0, 0)		#do second frame memory write for partial update
        epd.display_frame()

	#play song
	play_flag = 1
	while True:
		if GPIO.input(pp_select) == False:
			if play_flag == 1:
				play_flag = 0
				epd.set_frame_memory(play_sym, 88, 150)
				#pause song
			else:
				play_flag = 1
				epd.set_frame_memory(pause_sym, 88, 150)
				#play_song
			epd.display_frame()
		if GPIO.input(back) == False:
			return

def disp_list(items):

	num_items = len(items)
	if num_items == 0:
		return -1 #error

	num_pages = num_items / 7
	num_pitems = num_items % 7
	ppage = 0
	if num_pitems != 0:
		num_pages +=1
		ppage = 1
	cur_page = 0
	selection = 0

	print items
	print num_items
	print num_pages
	print num_pitems

	#epd = epd1in54.EPD()
        #epd.init(epd.lut_full_update)

	while True:
		epd = epd1in54.EPD()
        	epd.init(epd.lut_full_update)

		menu_list = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)  # 255: clear the frame
		draw = ImageDraw.Draw(menu_list)

        	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)

		arrow_sym = Image.open('/home/pi/symbols/bmp/25x25/arrow-right-a25.bmp')

        	draw.rectangle((0, 14, 200, 15), fill = 0)              #top icon tray

        	menu_list.paste(arrow_sym,(0,selection*25+20))                      	#arrow symbol
        	#draw.text((30,20+4), items[0], font = font, fill = 0)   #list the items

		i = 0
		yoff = 20
		while i < 7:
			if (ppage == True) and (i == num_pitems) and (cur_page == num_pages-1): #stop after displayed all of partial page
				break
	        	draw.text((30,yoff+4), items[cur_page*7 + i], font = font, fill = 0)   #list the items
			i += 1
			yoff +=25


		epd.clear_frame_memory(0xFF)                    #display 
        	epd.set_frame_memory(menu_list, 0, 0)
        	epd.display_frame()

		epd.init(epd.lut_partial_update)

		epd.set_frame_memory(menu_list, 0, 0)		#second frame mem write for partial update
		epd.display_frame

		#move_arrow = Image.new('1', (25, 184), 255)  # 255: clear the frame
		#draw = ImageDraw.Draw(move_arrow)
		while True:
			move_arrow = Image.new('1', (25, 190), 255)  # 255: clear the frame
        		#draw = ImageDraw.Draw(move_arrow)
			if GPIO.input(pp_select) == False:
				return selection+cur_page*7
			
			if GPIO.input(back) == False:
				return -99

			if GPIO.input(up) == False:
				if selection == 0 and cur_page == 0:
					pass
				elif selection == 0:
					cur_page -= 1
					selection = 6
					break
				else:
					selection -=1
					move_arrow.paste(arrow_sym,(0,selection*25))
                        		epd.set_frame_memory(move_arrow, 0, 20)
                        		epd.display_frame()

			elif GPIO.input(down) == False:
				if (ppage == True) and (selection == num_pitems-1) and (cur_page == num_pages-1):
					pass
				elif selection == 6 and cur_page == num_pages-1:
					pass
				elif selection != 6:
					selection +=1
					move_arrow.paste(arrow_sym,(0,selection*25))
					epd.set_frame_memory(move_arrow, 0, 20)
        				epd.display_frame()
				elif selection == 6:
					cur_page += 1
					selection = 0
					print cur_page
					break


	#return selection

def get_artists():
	p1 = subprocess.Popen(['ls','/home/pi/music/'],stdout=subprocess.PIPE)

        out,err = p1.communicate()
        p1.stdout.close()
        artists = out.splitlines()        #split the string by line into list (each ssid on own line)
	return artists

def get_albums(artist):
	path = '/home/pi/music/' + artist
	p1 = subprocess.Popen(['ls',path],stdout=subprocess.PIPE)

        out,err = p1.communicate()
        p1.stdout.close()
        albums = out.splitlines()        #split the string by line into list (each ssid on own line)
        return albums

def get_songs(artist,album):
	path = '/home/pi/music/' + artist + '/' + album
        p1 = subprocess.Popen(['ls',path],stdout=subprocess.PIPE)

        out,err = p1.communicate()
        p1.stdout.close()
        songs = out.splitlines()        #split the string by line into list (each ssid on own line)
        return songs 


def main():
	#art = '/home/pi/symbols/bmp/arrow-right-a1.bmp'
	art = 0

	select_art = 0
	select_alb = 0
	select_s = 0

	#artists = get_artists()
	#select_art = disp_list(artists)

	#while True:
		#artists = get_artists()
		#print artists
		#select_art = disp_list(artists)
		#if select_art == -99:
			#pass
		#else:
			#albums = get_albums(artists[select_art])		
			#select_alb = disp_list(albums)
			#if select_alb == -99:
				#pass
			#else:
				#songs = get_songs(artists[select_art],albums[select_alb])
				#print songs
				#songs_trim = [s[3:-4] for s in songs]
				#print songs_trim
				#print songs
	
				#select_s = disp_list(songs_trim)
				#print songs[select_s]
				#if select_s == -99:
					#pass
				#else:	
					#play the song
					#disp_np(artists[select_art],albums[select_alb],songs_trim[select_s],art)

	artists = get_artists()
        select_art = disp_list(artists)
	while select_art != -99:
		albums = get_albums(artists[select_art])
                select_alb = disp_list(albums)
                while select_alb != -99:
			songs = get_songs(artists[select_art],albums[select_alb])
                        #print songs
                        songs_trim = [s[3:-4] for s in songs]
                        #print songs_trim
                        #print songs

                        select_s = disp_list(songs_trim)
                        #print songs[select_s]
			while select_s != -99:
				#play the song
                                disp_np(artists[select_art],albums[select_alb],songs_trim[select_s],art)
				
				songs = get_songs(artists[select_art],albums[select_alb])
                        	songs_trim = [s[3:-4] for s in songs]
                        	select_s = disp_list(songs_trim)

			albums = get_albums(artists[select_art])
	                select_alb = disp_list(albums)

		artists = get_artists()
       		select_art = disp_list(artists)
#wi_name = wifi.scan()
#print wi_name

#print wifi.remove("SR Wireless Test")
#print wifi.remove("Fake")

#print wifi.add("TEST SSID","TEST PASSWORD")
#print wifi.add("TEST SSID","TEST PASSWORD")
#print wifi.remove("TEST SSID")
#print wifi.remove("TEST SSID")


if __name__ == '__main__':
    main()
