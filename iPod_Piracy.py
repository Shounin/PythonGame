__author__ = 'Soffía & Styrmir'
import stagger
from stagger.id3 import *
import os
import shutil


def read_id3(src, dest):
    files = []
    #Get list of files in directory
    for dirName, subdirList, fileList in os.walk(src):
        files.append([os.path.join(os.getcwd(), os.path.join(dirName, x)) for x in fileList])
    flatFiles = [x for sublist in files for x in sublist]

    for x in flatFiles:
        #special case for empty files
        if os.stat(x).st_size is 0:
            os.remove(x)
        else:
            tag = stagger.read_tag(x)
            tag = check(tag)

            #The following if/else soup contains cases for dealing with an unknown artist,
            # unknown album or unknown song name.
            #Sorts files first by artist (with a special folder for unknown artists) then album
            #(or root folder if unknown) and then changes the name of the file if the metadata contains the song name
            if tag.artist == '':
                path = os.path.join(dest, 'Unknown Artist')
                if not os.path.exists(path):
                    os.makedirs(os.path.join(dest, 'Unknown Artist'))
                if tag.title is not '':
                    shutil.move(x, os.path.join(os.path.join(dest, 'Unknown Artist'), tag.title + os.path.splitext(x)[1]))
                else:
                    shutil.move(x, os.path.join(dest, 'Unknown Artist'))
            else:
                if tag.album is not '':
                    path = os.path.join(dest, os.path.join(tag.artist.strip(), tag.album))
                    if not os.path.exists(path):
                        os.makedirs(path)
                    if tag.title is not '':
                        shutil.move(x, os.path.join(os.path.join(dest, os.path.join(tag.artist.strip(), tag.album)), tag.title + os.path.splitext(x)[1]))
                    else:
                        shutil.move(x, os.path.join(dest, os.path.join(tag.artist.strip(), tag.album)))
                else:
                    path = os.path.join(dest, tag.artist)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    if tag.title is not '':
                        shutil.move(x, os.path.join(dest, os.path.join(tag.artist.strip(), tag.title + os.path.splitext(x)[1])))
                    else:
                        shutil.move(x, os.path.join(dest, tag.artist.strip()))

    #remove empty folders
    for dirName, subdirList, fileList in os.walk(src, topdown=False):
        for name in subdirList:
            if not os.listdir(os.path.join(dirName, name)):
                os.rmdir(os.path.join(dirName, name))

#Special cases for characters which cannot be in folder names
def check(tag):
    if ':' in tag.artist:
        tag.artist = ''.join(tag.artist.split(':'))
    if ':' in tag.title:
        tag.title  = ''.join(tag.title.split(':'))
    if ':' in tag.album:
        tag.album  = ''.join(tag.album.split(':'))
    if '?' in tag.artist:
        tag.artist = ''.join(tag.artist.split('?'))
    if '?' in tag.title:
        tag.title  = ''.join(tag.title.split('?'))
    if '?' in tag.album:
        tag.album  = ''.join(tag.album.split('?'))
    if '"' in tag.artist:
        tag.artist = ''.join(tag.artist.split('"'))
    if '"' in tag.title:
        tag.title  = ''.join(tag.title.split('"'))
    if '"' in tag.album:
        tag.album  = ''.join(tag.album.split('"'))
    if '/' in tag.artist:
        tag.artist = ' '.join(tag.artist.split('/'))
    if '/' in tag.title:
        tag.title  = ' '.join(tag.title.split('/'))
    if '/' in tag.album:
        tag.album  = ' '.join(tag.album.split('/'))
    if '\\' in tag.artist:
        tag.artist = ' '.join(tag.artist.split('\\'))
    if '\\' in tag.title:
        tag.title  = ' '.join(tag.title.split('\\'))
    if '\\' in tag.album:
        tag.album  = ' '.join(tag.album.split('\\'))
    if len(tag.title) > 50:
        tag.title = tag.title[:50]

    tag.artist = tag.artist.strip()
    tag.title  = tag.title.strip()
    tag.album  = tag.album.strip()
    
    return tag

src = input('Please enter name of source folder\n')
dest = input('Please enter name of destination folder\n')
read_id3(src, dest)
