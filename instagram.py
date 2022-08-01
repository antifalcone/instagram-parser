from instagrapi import Client
import os
import json
import shutil
USERNAME = ''
PASSWORD = ''
pk = 0

def account_info(id_target):
    dict_user_info = client.user_info(id_target).dict()
    profile_pic_url = dict_user_info['profile_pic_url_hd']
    biography = dict_user_info['biography']
    external_url = dict_user_info['external_url']
    bool_is_business_account = dict_user_info['is_business']
    public_email = dict_user_info['public_email']
    contact_phone_number = dict_user_info['contact_phone_number']
    dict ={"profile_picture": profile_pic_url,"biography": biography,'external_url': external_url,'is_business': bool_is_business_account,'public_email': public_email,'contact_phone_number':contact_phone_number}
    print(json.dumps(dict))
    with open("account_info.json", "w") as write_file:
        json.dump(dict, write_file)

def medias_account(id_target):
    if os.path.exists(f'{os.getcwd()}/script/photos') == False:
        os.mkdir('script/photos')
        os.mkdir('script/photos/album_photos')
    else:
        ask_for_remove = input("Do you want remove this directory (photos/) ?Y/n: ")
        if (ask_for_remove == 'Y') or (ask_for_remove == 'y') or (ask_for_remove == 'н'):
            shutil.rmtree(r'script')
            os.mkdir('script/photos')
            os.mkdir('script/photos/album_photos')
        elif (ask_for_remove == 'N') or (ask_for_remove == 'n') or (ask_for_remove == 'т'):
            exit()
    media_type = 0
    i = 0
    list_of_media_in_account = client.user_medias(id_target, amount = 0)
    for count in list_of_media_in_account:
        for Media in count:
            if Media[0] == 'pk':
                pk = Media[1]
        dict = client.media_info(pk).dict()
        if dict['media_type'] == 1:
            i = i + 1
            url = dict['thumbnail_url']
            client.photo_download_by_url(url,f'{os.getcwd()}/script/photos/image{i}.img')
        elif dict['media_type'] == 8:
            client.album_download(pk,f'{os.getcwd()}script/photos/album_photos/')
def tagged_media_account(id_target):
    i = 0
    k = 0
    if os.path.exists('script/photos_tagged') == False:
        os.mkdir('script/photos_tagged')
        os.mkdir('script/photos_tagged/album_photos')
    else:
        ask_for_remove = input("Do you want remove this directory (photos_tagged/) ?Y/n: ")
        if (ask_for_remove == 'Y') or (ask_for_remove == 'y') or (ask_for_remove == 'н'):
            shutil.rmtree(r'script/photos_tagged')
            os.mkdir('script/photos_tagged')
            os.mkdir('script/photos_tagged/album_photos')
        elif (ask_for_remove == 'N') or (ask_for_remove == 'n') or (ask_for_remove == 'т'):
            exit()
    list_of_tagged_media = client.usertag_medias(id_target, amount = 0)
    for count in list_of_tagged_media:
        dicta = {}
        accessibility_caption = ''
        name_of_location = ''
        for Media in count:
            if Media[0] == 'pk':
                pk = Media[1]
        dict = client.media_info(pk).dict()
        if dict['caption_text'] != None:
            caption_text = dict['caption_text']
        if dict['accessibility_caption'] != None:
            accessibility_caption = dict['accessibility_caption']

        if dict['location'] != None:
            location = dict['location']
            name_of_location = location['name']

        if dict['media_type'] == 1:
            i = i + 1
            url = dict['thumbnail_url']
            print(url)
            image = client.photo_download_by_url(url,f'{os.getcwd()}/script/photos_tagged/image{i}')
        elif dict['media_type'] == 8:
            image = client.album_download(pk,f'{os.getcwd()}/script/photos_tagged/album_photos/')
        dicti = {"photo": image, "caption_text": caption_text,"accessibility_caption": accessibility_caption,"name_of_location" : name_of_location}
        dicta.update(dicti)
        print(dicta)
client = Client()
client.login(USERNAME,PASSWORD)
id_target = client.user_id_from_username('pavel_shvaytsburg')
account_info(id_target)
medias_account(id_target)
tagged_media_account(id_target)
