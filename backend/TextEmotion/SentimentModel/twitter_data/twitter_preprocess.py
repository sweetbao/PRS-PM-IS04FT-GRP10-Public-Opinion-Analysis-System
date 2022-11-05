import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re


ps = PorterStemmer()
# nltk.download('stopwords')
# nltk.download('omw-1.4')

# df = pd.read_csv('twitter_training.csv', header=None)
# print(df[3].shape)
# f1 = open('./train.sen', 'w')
# for i, d in enumerate(df[3]):
#     if df[2][i] != 'Irrelevant':
#         d = str(d).strip()
#         d = d.replace('\n', ' ')
#         if d != '':
#             f1.write(d+'\n')
# # f1.close()
# # f1 = open('./dev.mid')
# # f1_0 = open('./dev.sen', 'w')
# # lines = f1.readlines()
# # for line in lines:
# #     if line.strip() != '':
# #         f1_0.write(line)
#
# f2 = open('./train.lab', 'w')
# for d in df[2]:
#     if d != 'Irrelevant':
#         f2.write(d+'\n')

tweets = pd.read_csv('twitter_training.csv', header=None)
tweets_val = pd.read_csv('twitter_validation.csv', header=None)
tweets = tweets.sample(frac=1).reset_index(drop=True)
tweets = tweets[tweets[2] != "Irrelevant"]
tweets = tweets[[1, 2, 3]]
tweets.rename(columns={1: "Domain", 2: "Sentiment", 3: 'text'}, inplace=True)
# print(tweets.head())
sentences = tweets['text'].values
labels = tweets['Sentiment'].values
domain = tweets['Domain'].values
stopwords = [set(stopwords.words('english'))]
cleaned_sentences = []
final_labels = []
final_domains = []
for i in range(len(sentences)):
    try:
        sent = re.sub('[^A-Za-z]', ' ', sentences[i])
        sent = sent.lower()
        sent = nltk.word_tokenize(sent)
        ps = nltk.pos_tag(sent)
        sent = [i[0] for i in ps if i[1] == ('JJ' or 'VBP' or 'VB')]
        sent = ' '.join(sent)
        dom = domain[i]
        # if domain[i] == 'CS-GO' or domain[i] == 'FIFA' or domain[i] == 'NBA2K':
        #     dom = domain[i]
        # else:
        #     # 去掉domain括号里的单词，用大写字母分词
        #     dom = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", domain[i])
        #     dom = re.sub("[A-Z]", lambda x: " " + x.group(0), dom)
        #     # pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
        #     # dom = re.sub(pattern, lambda x: " " + x.group(0), dom)
        #     dom = dom.lower()
        if sent != '':
            cleaned_sentences.append(sentences[i])
            final_labels.append(labels[i])
            final_domains.append(dom)
        if i % 10000 == 0:
            print('nltk Count:', i)
    except:
        pass

data_len = len(cleaned_sentences)

with open('./train.sen', 'w') as f1:
    with open('./train.lab', 'w') as f2:
        with open('./dev.sen', 'w') as f3:
            with open('./dev.lab', 'w') as f4:
                with open('./test.sen', 'w') as f5:
                    with open('./test.lab', 'w') as f6:
                        with open('./train.dom', 'w') as f7:
                            with open('./dev.dom', 'w') as f8:
                                with open('./test.dom', 'w') as f9:
                        # for i in range(data_len):
                        #     if i < 0.6 * data_len:
                        #         f1.write(cleaned_sentences[i]+'\n')
                        #         f2.write(final_labels[i]+'\n')
                        #     elif i < 0.8*data_len:
                        #         f3.write(cleaned_sentences[i] + '\n')
                        #         f4.write(final_labels[i] + '\n')
                        #     else:
                        #         f5.write(cleaned_sentences[i] + '\n')
                        #         f6.write(final_labels[i] + '\n')
                                    for i in range(data_len):
                                        if i < 0.8 * data_len:
                                            f1.write(cleaned_sentences[i]+'\n')
                                            f2.write(final_labels[i]+'\n')
                                            f7.write(final_domains[i] + '\n')
                                        else:
                                            f3.write(cleaned_sentences[i] + '\n')
                                            f4.write(final_labels[i] + '\n')
                                            f5.write(cleaned_sentences[i] + '\n')
                                            f6.write(final_labels[i] + '\n')
                                            f8.write(final_domains[i] + '\n')
                                            f9.write(final_domains[i] + '\n')
