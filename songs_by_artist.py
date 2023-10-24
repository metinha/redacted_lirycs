# a Program that uses azapi library to query all the songs from an artist passing the name from command line
# import azlyrics and send the results to elasticsearch
import azapi
import sys
import json
import elasticsearch
from ssl import create_default_context
import time

def send_to_elasticsearch(data):
    # connect to elasticsearch
    context = create_default_context(cafile="./http_ca.crt")
    #ssl_context=context
    # This is my cert fingerprint, you need to change it to your own as well as your host, and api keys
    CERT_FINGERPRINT = "bc7029484d77a4857f843cbae97f16f3496a271b55b180c4b763475315b69ec2"
    es = elasticsearch.Elasticsearch(
    "https://10.10.0.200:9200",api_key=("<your_api_id>", "<your_api_key>"),ssl_assert_fingerprint=CERT_FINGERPRINT       
)
    
    # create an index
    #es.indices.create(index='songs', ignore=400)
    # send the data to elasticsearch
    es.index(index='songs', body=json.dumps(data))

def main():

    api_call = azapi.AZlyrics()
    #get the artist name from command line
    if len(sys.argv) < 2:
        print("Please pass the artist name as argument")
        sys.exit(1)
    else:
        api_call.artist = sys.argv[1]
        songs = api_call.getSongs()
        data={}
        #print(songs)
        for song in songs:
            try:
                my_lyrics = api_call.getLyrics(url=songs[song]["url"])
                data= {
                "artist":api_call.artist,
                "song":song,
                "album":songs[song]["album"],
                "year":songs[song]["year"],
                "lyrics":{
                    "raw": my_lyrics,
                    "mild": my_lyrics
                    }
                }
                send_to_elasticsearch(data)
                time.sleep(10)
            except IndexError:
                continue
        #print(new_song)

if __name__ == "__main__":
    main()