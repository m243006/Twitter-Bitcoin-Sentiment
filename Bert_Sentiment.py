import datetime, time, random, torch
from transformers import BertTokenizer, BertModel, BertConfig

class tweet:
    def __init__(self, string):
        splat = string.split(',')
        splat_cleaned = []
        flag = False
        self.valid = True
        for i in range(len(splat)):
            if(flag):
                splat_cleaned[-1] += ',' + splat[i]
            else:
                splat_cleaned.append(splat[i])
            if(not flag and len(splat[i]) > 0 and splat[i][0] == '"'):
                splat_cleaned[-1] = splat[i][1:]
                flag = True
            if(flag and len(splat[i]) > 0 and splat[i][-1] == '"' and not(len(splat[i]) > 1 and splat[i][-2] == '"' and not(len(splat[i]) > 2 and splat[i][-3] == '"'))):
                splat_cleaned[-1] = splat_cleaned[-1][:-1]
                flag = False
        if(len(splat_cleaned) != 13):
            self.valid = False
        else:
            self.splat = splat_cleaned
            (self.name, self.location, self.bio, self.user_created, self.followers, self.friends, self.favorites, self.verified, self.tweet_created, self.text, self.hashtags, self.source, self.retweet) = splat_cleaned
            self.followers = int(self.followers.split('.')[0])
            self.friends = int(self.friends.split('.')[0])
            self.favorites = int(self.favorites.split('.')[0])
            self.verified = (self.verified == 'True')
            if(self.hashtags == ''):
                self.hashtags = []
            else:
                self.hashtags = eval(self.hashtags)
            self.retweet = (self.retweet == 'True')
            self.user_created = datetime.datetime.strptime(self.user_created, "%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return "\n".join(self.splat) + "\n"


class tweet_parser:
    def __init__(self):
        self.tweets = []
        tweet_file = open('Bitcoin_tweets.csv', 'r', newline='')
        line = tweet_file.readline()
        num_tried = 0
        num_succeed = 0
        fil = tweet_file.read().split('\n')
        print("read in")
        cur = fil[0]
        for j in fil[1:]:
            if(cur[-6:] == ',False' or cur[-5:] == ",True"):
                num_tried += 1
                if(num_tried % 100000 == 0):
                    print(str(num_tried) + " out of 4600000 tweets loaded")
                a = tweet(cur)
                if(a.valid):
                    self.tweets.append(a)
                cur = ""
            cur += j

    def get_random_tweet(self):
        return random.choice(self.tweets)


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
config = BertConfig.from_pretrained('bert-base-uncased', output_hidden_states=True)
model = BertModel.from_pretrained('bert-base-uncased', config=config)

def cls_token(sent):
    inputs = tokenizer([sent], padding=True, return_tensors="pt")
    outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state[0]
    return last_hidden_states[0]

a = tweet_parser()

pos = open("machine_positive.txt", 'w')
neg = open("machine_negative.txt", 'w')
disc = open("/dev/null", 'w')
notes = []
for i in open("positives.txt", 'r').readlines():
    notes.append((cls_token(i), pos))
for i in open("negatives.txt", 'r').readlines():
    notes.append((cls_token(i), neg))
for i in open("discard.txt", 'r').readlines()[:1000]:
    notes.append((cls_token(i), disc))

cos = torch.nn.CosineSimilarity(dim=0)
for i in range(0, len(a.tweets), 1000):
    vec = cls_token(a.tweets[i].text)
    mx = -1
    loc = disc
    for j in notes:
        dif = cos(vec, j[0])
        if(dif > mx):
            mx = dif
            loc = j[1]
    loc.write(a.tweets[i].tweet_created[:10] + "\n")
pos.close()
neg.close()
disc.close()
