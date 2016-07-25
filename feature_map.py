#! /usr/bin/python


import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


file = open(sys.argv[1],"r")
toWrite = open(sys.argv[2],"w+")

feature_map = {}
feature_index = 0
HASH_SIZE = 1000000

def process_Id_Feature(prefix,id):
    global feature_map
    global feature_index
    str = prefix + "_" + id
    if str in feature_map:
        return feature_map[str]
    else:
        feature_index = feature_index + 1
        feature_map[str] = feature_index
    return feature_index

def hash_feature(prefix,id):
    str = prefix +"_" + id
    return hash(str)%HASH_SIZE

def extract_Feature1(seg):
    list = []
    list.append(process_Id_Feature("url",seg[1]))
    list.append(process_Id_Feature("ad",seg[2]))
    list.append(process_Id_Feature("ader",seg[3]))
    list.append(process_Id_Feature("depth",seg[4]))
    list.append(process_Id_Feature("pos",seg[5]))
    list.append(process_Id_Feature("query",seg[6]))
    list.append(process_Id_Feature("keyword",seg[7]))
    list.append(process_Id_Feature("title",seg[8]))
    list.append(process_Id_Feature("desc",seg[9]))
    list.append(process_Id_Feature("user",seg[10])) 
    return list

def extractFeature2(seg):
    depth = float(seg[4])
    pos = float(seg[5])
    ralative_pos = int (pos*10/depth)
    return process_Id_Feature("pos_ratio",str(relative_pos))


def extract_combination_feature(seg):
    list = []
    if(len(seg) >=16):
        str1 = seg[2] + "_" + seg[15]
        list.append(process_Id_Feature("gender",seg[15]))
        str2 = seg[15] + "_" + seg[16]
        list.append(process_Id_Feature("age",seg[16]))
    return list
      
def extract_numerical_feature(seg):
    
    list = []
    
    num_query = len(seg[11].strip().split("|"))
    num_keyword = len(seg[12].strip().split("|"))
    num_title = len(seg[13].strip().split("|"))
    num_description = len(seg[14].strip().split("|"))
    
    list.append(str(process_Id_Feature("num_query"," ")) + ":" + str(num_query))
    list.append(str(process_Id_Feature("num_keyword"," ")) + ":" + str(num_keyword))
    list.append(str(process_Id_Feature("num_description"," ")) + ":" + str(num_description))
    list.append(str(process_Id_Feature("num_title"," ")) + ":" + str(num_title))
    
    tfidf_vectorizer = TfidfVectorizer()
    corpus = seg[11:15]
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    #print tfidf_matrix.shape
    
    #tfidf = tf_idf(corpus)
    
    #query_similar_keyword = tfidf_similarity(tfidf[0],tfidf[1])
    query_similar_keyword = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    #print query_similar_keyword
    #query_similar_title = tfidf_similarity(tfidf[0],tfidf[2])
    query_similar_title = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[2:3])
    #print query_similar_title
    #query_similar_description = tfidf_similarity(tfidf[0],tfidf[3])
    query_similar_description = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[3:])
    #print query_similar_description
    #keyword_similar_title = tfidf_similarity(tfidf[1],tfidf[2])
    keyword_similar_title = cosine_similarity(tfidf_matrix[1:2],tfidf_matrix[2:3])
    #print keyword_similar_title
    #title_similar_description = tfidf_similarity(tfidf[2],tfidf[3])
    title_similar_description = cosine_similarity(tfidf_matrix[1:2],tfidf_matrix[3:])
    #print title_similar_description  
    
    
    list.append(str(process_Id_Feature(query_similar_keyword," ")) + ":" + str(query_similar_keyword))
    list.append(str(process_Id_Feature(query_similar_title," ")) + ":" + str(query_similar_title))
    list.append(str(process_Id_Feature(query_similar_description," ")) + ":" + str(query_similar_description))
    list.append(str(process_Id_Feature(keyword_similar_title," ")) + ":" + str(keyword_similar_title))
    list.append(str(process_Id_Feature(title_similar_description," ")) + ":" + str(title_similar_description))
    
    depth = float(seg[4])
    position  float(seg[5])
    relative_pos = float((depth - position)*10.0/depth)
    list.append(str(process_Id_feature("relative_pos_num"," ")) + ":" + str(relative_pos))
    return list
        
def toStr(label,list):
    line = label
    for i in list:
        line = line + "\t" + str(i) + ":1"
    return line

def num_to_str(numer_list):
    return "\t".join(numer_list)

for line in file:
    seg = line.strip().split("\t")
    list = extractFeature1(seg)
    list.append(extractFeature2(seg))
    list.extend(extract_combination_feature(seg))
    #list.extend(extractFeature4(seg))
    #list.extend(extractFeature5(seg))
    list_numer = extract_numerical_feature(seg)
    toWrite.write(toStr(seg[0],list) + "\t" + num_to_str(list_numer) + "\n")
    
toWrite.close
file.close()
