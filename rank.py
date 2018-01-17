from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
from itertools import islice
import numpy as np
import operator,re, math, json
from textblob import TextBlob


def calculate_pt(word_array, reldoc, doc):
    pt = []
    for word in word_array:
        rel_pre = rel_abs = 0.0
        for document in reldoc:
            if word in doc[document]:
                rel_pre += 1
            else:
                rel_abs += 1
        rel_pre += 0.5
        rel_abs += 0.5
        pt.append(rel_pre / (rel_pre + rel_abs))
    return pt

def calculate_ut(word_array, reldoc, doc):
    ut = []
    for word in word_array:
        non_rel_pre = non_rel_abs = 0.0
        for document in list(set(doc) - set(reldoc)):
            if word in document:
                non_rel_pre += 1
            else:
                non_rel_abs += 1
        non_rel_pre += 0.5
        non_rel_abs += 0.5
        ut.append(non_rel_pre / (non_rel_pre + non_rel_abs))
    return ut

def calculate_ct(pt,ut):
    ct = []
    for i in range(len(pt)):
        ct.append(math.log(((pt[i] * (1 - ut[i])) / (ut[i] * (1 - pt[i])))))
    return ct

def calculate_rsv(ct,tf_array,doc):
    rsv = []
    tfrow = len(tf_array)
    tfcol = len(tf_array[0])
    for i in range(len(doc)):
        rsvval = 0
        for j in range(tfcol):
            if tf_array[tfrow - 1, j] > 0 and tf_array[i, j] > 0:
                rsvval += ct[j]
        rsv.append(rsvval)
    return rsv

def calculate_rsv_variant(ct, doc, word_array):
    doc_ct_mat = []
    dt = []
    for d in range(0, len(doc)):
        doc_ct = []
        for index, word in enumerate(word_array):
            if word in doc[d]:
                doc_ct.append(ct[index])
            else:
                doc_ct.append(0)
        doc_ct_mat.append(doc_ct)
    for index,document in enumerate(doc):
        dt.append(1 - spatial.distance.cosine(doc_ct_mat[index], doc_ct_mat[-1]))
    return dt

def get_rsv_result(rsv, doc, full_doc):
    final_mydic = {}
    for idx, i in enumerate(doc):
        final_mydic.update({i.split(':-')[0]: rsv[idx]})
    d_descending = OrderedDict(sorted(final_mydic.items(), key=operator.itemgetter(1), reverse=True))
    result = []
    count = 0
    for key, value in d_descending.items():
        if count < 9 and value > 0 and key in full_doc.keys():
            #print(count, value, key)
            result.append(key)
            count +=1
    return result

def sentimental_analysis(result, full_doc):
    rate = []
    for i in result:
        x = 0
        for j in range(len(full_doc[i]) - 5):
            blob = TextBlob(full_doc[i]["Review "+str(j)])
            for sentence in blob.sentences:
                x += sentence.sentiment.polarity
        rate.append(x)

    return rate

def ranking(result, full_doc):
    rate = sentimental_analysis(result, full_doc)
    download = [int(full_doc[i]["Download"]) for i in result]
    mean = np.mean(download)
    std = np.std(download)
    normalize_download = [((x - mean)/std)+3 for x in download]
    value = [normalize_download[i] + rate[i]/(len(full_doc[result[i]]) - 5) + float(full_doc[result[i]]["Rating"]) for i in range(len(result))]
    output = {}
    for i in range(len(result)):
        output[result[i]] = value[i]
    output = OrderedDict(sorted(output.items(), key=operator.itemgetter(1), reverse=True))
    return [i for i in output.keys()]

def print_dict(dict,full_dict):
    for key,value in dict.items():
        print(key,full_dict[key]["Link"])

def main(query):
#if __name__ == '__main__':
    query = "music"
    vect = TfidfVectorizer(min_df=1)
    file = open(r'C:\Users\User\Desktop\IR\Package\APP.json')
    data = json.load(file)
    doc = []
    full_doc = {}
    for i in data['Apps']:
        full_doc[i['Name']] = i

    for idx, i in enumerate(data['Apps']):
        doc.append(i['Name'] + ":-" + i['Description'])
    search_query = query #input("Enter Query : ")
    doc.append( "=> " + search_query)
    tfidf = vect.fit_transform(doc)
    weights = (tfidf * tfidf.T).A
    dist = cosine_similarity(weights)
    cos_sim = np.round(dist, 4)
    mydic = {}
    for idx,i in enumerate(doc):
        mydic.update({idx: cos_sim[len(cos_sim) - 1, idx]})
    sorted_mydic = sorted(mydic.items(), key=operator.itemgetter(1), reverse=True)
    top_k_doc = 6
    reldoc = [ i[0] for i in islice(sorted_mydic, top_k_doc)]
    del reldoc[0]
    tf_array = tfidf.toarray()
    word_array = vect.get_feature_names()
    ut = calculate_ut(word_array,reldoc,doc)
    pt = calculate_pt(word_array,reldoc,doc)
    ct = calculate_ct(pt,ut)
    rsv = calculate_rsv(ct,tf_array,doc)
    #print(rsv)
    #rsv_var = calculate_rsv_variant(ct,doc,word_array)
    result = get_rsv_result(rsv,doc,full_doc)
    output = ranking(result,full_doc)
    print(output)
    return [output,full_doc]

    #print_dict(output,full_doc)
    #print_result(rsv_var, doc)
