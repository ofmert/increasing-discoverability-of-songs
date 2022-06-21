import requests
import json
import csv
import time

f = open('final_output.csv', 'w', newline='')
writer = csv.writer(f)

headers = {
    'accept': 'application/json',
}

#list of lists with doubles containing song_id and lyrics -->[['songid1', "lyrics1"], ['songid2', '"lyrics2"']
all_song_doubles = []

#list of lists of lists with containing song_id and lists of lists regarding entity uris -->['songid', ['uri1', 'uri2']]
complete_doubles = []

def get_all_entity_uris(final_songid, text):
    current_saved_entity_uris = []
    current_double = []

    #Requestion the lyrics
    request_url = "http://spotlight.amp.lod.labs.vu.nl/rest/annotate?text=" #"http://api.dbpedia-spotlight.org/en/annotate?text="
    r = requests.get(request_url + text, headers=headers)
    #Checking if API gives response
    if(r.status_code == 200):
        try:
            #key
            entity_results = json.loads(r.text)['Resources']

            # looping through all recognized uris
            for entity_result in entity_results:
                if(entity_result['@URI'] not in current_saved_entity_uris):
                    current_saved_entity_uris.append(entity_result['@URI'])
            
            #print(current_saved_entity_uris)
            current_double.append(final_songid)
            current_double.append(current_saved_entity_uris)
            complete_doubles.append(current_double)
        except KeyError:
            pass
    else:
        pass



def get_all_relation_uris(final_songid, saved_entity_uri):
    
    entity_url = saved_entity_uri
    #request
    entity_request_url = requests.get(entity_url, headers=headers)
    #Checking if API gives response
    if(entity_request_url.status_code == 200):
        try:
            #key1
            entity_uri_split = entity_url.split("/")
            entity_name = entity_uri_split[-1]
            entity_relations = json.loads(entity_request_url.text)['http://dbpedia.org/resource/' + entity_name]
            #key2
            sameas_relations = entity_relations['http://www.w3.org/2002/07/owl#sameAs']

            for sameas_relation in sameas_relations:
                samesas_tuple = (final_songid, 'owl:sameAs', sameas_relation["value"])
                print("")
                print('@@@@@@@@@@@@@@ Writing owl:sameAs relation @@@@@@@@@@@@@@')
                print("")
                print(samesas_tuple)
                print("")
                writer.writerow(samesas_tuple)

            #key3
            rdftype_relations = entity_relations['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']

            for rdftype_relation in rdftype_relations:
                rdftype_tuple = (final_songid, 'rdf:type', rdftype_relation["value"])
                print("")
                print('@@@@@@@@@@@@@@ Writing rdf:type relation @@@@@@@@@@@@@@')
                print("")
                print(rdftype_tuple)
                print("")
                writer.writerow(rdftype_tuple)

        except KeyError:
            pass
    else:
        pass




#File input
#input = open('test.txt')#1 array met elementen
input = open('lyrics4.nq')#1 array met elementen
input_lines = input.readlines()

#Extract all songs id's and song lyrics
for line in input_lines:
    current_double = []

    #extracting song id
    songid = line.split('<')[1:2]
    newsongid = songid[0]
    shortened_songid = newsongid[:-2]
    current_double.append(shortened_songid)

    #extracting song lyrics
    lyrics = line.split()[2:-2]
    lyrics = ' '.join(lyrics)
    text = lyrics

    #adding every double to the list of all doubles
    current_double.append(text)
    all_song_doubles.append(current_double)

""" print("")
print('@@@@@@@@@@@@@@ All Song Doubles @@@@@@@@@@@@@@')
print("")
print(all_song_doubles)
print("")
 """

counter = 1
#loops thourgh all song double in order to get -->['songid', ['uri1', 'uri2']]
for song_double in all_song_doubles:
    
    print("")
    print('@@@@@@@@@@@@@@ Song Number %d @@@@@@@@@@@@@@' %counter)
    print("")
    print(song_double[0])
    counter += 1
    print("")

    # song_id , text
    get_all_entity_uris(song_double[0], song_double[1])

""" print("")
print("@@@@@@@@@@@@@@ COMPLETE DOUBLES @@@@@@@@@@@@@@")
print("")
print(complete_doubles) """

#Extracts all the owl:sameAs and rdf:type relations
for double in complete_doubles:
    for uri in double[1]:
        get_all_relation_uris(double[0], uri)
