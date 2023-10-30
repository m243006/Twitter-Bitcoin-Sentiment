import datetime, time, random

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
            self.tweet_created = datetime.datetime.strptime(self.tweet_created, "%Y-%m-%d %H:%M:%S")
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


pos = open("positives.txt", 'a')
neg = open("negatives.txt", "a")
disc = open("discard.txt", 'a')
a = tweet_parser()
resp = ' '
while(resp[0] != 'q'):
    twt = a.get_random_tweet()
    print()
    print(twt.text)
    print()
    resp = input("Is this tweet positive (p)? negative (n)? or discard (d)? (q for quit)")
    if(len(resp) == 0):
        resp = " "
    if(resp[0] == 'p'):
        pos.write(twt.text)
    if(resp[0] == 'n'):
        neg.write(twt.text)
    if(resp[0] == 'd'):
        disc.write(twt.text)
pos.close()
neg.close()
disc.close()
