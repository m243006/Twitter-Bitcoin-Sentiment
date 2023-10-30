import datetime, time, random
import sys
import data

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




#
# sentiment.py -lexicon|learn [-data <data-dir>]
#

# YOU MUST WRITE THESE TWO FUNCTIONS (train and test)
#
def label_with_lexicon(lexicon_positives, lexicon_negatives, testing_tweets):
    scores = dict()
    final = list()
    for p in testing_tweets:
        l = p.lower().split()
        newl = []
        pos = 0
        neg = 0
        for word in l:
            word = word.lower()
            if word == 'not':
                neg = neg + 5
            if word == 'yes':
                pos = pos + 10
            if 'sad' in word:
                neg = neg + 100


            if 'rise' in word:
                pos = pos + 100
            if 'above' in word:
                pos = pos + 10
            if 'moon' in word:
                pos = pos + 100
            if 'bull' in word:
                pos = pos + 100
            if 'buy' in word:
                pos = pos + 100
            if 'up' in word:
                pos = pos + 1000
            if 'rebound' in word:
                pos = pos + 2000
            if 'bounce' in word:
                pos = pos + 2000
            if 'U+1F911' in word: 
                pos = pos + 100 
            if 'U+1F680' in word: 
                pos = pos + 1000 
            if '🚀' in word: 
                pos = pos + 1000 
            if '🔥' in word: 
                pos = pos + 1000 
            if '🌖' in word: 
                pos = pos + 100
            if '📈' in word: 
                pos = pos + 1000
            if '🟢' in word: 
                pos = pos + 1000
            if '💪' in word: 
                pos = pos + 100
            if 'gain' in word:
                pos = pos + 10

            if 'sad' in word:
                neg = neg + 100
            if 'los' in word:
                neg = neg + 100
            if 'down' in word:
                neg = neg + 100
            if 'lost' in word:
                neg = neg + 100
            if 'scam' in word:
                neg = neg + 100
            if 'plunge' in word:
                neg = neg + 100
            if 'tank' in word:
                neg = neg + 100

            if 'useless' in word:
                neg = neg + 10
            if 'crash' in word:
                neg = neg + 100
            if 'short' in word:
                neg = neg + 100
            if 'down' in word:
                neg = neg + 100
            if 'bear' in word:
                neg = neg + 100
            if '🔴' in word:
                neg = neg + 1000
            if '📉' in word:
                neg = neg + 1000
                

            #call helper two times just to clean the words as good as it can
            word =helper(word)
            word =helper(word)
            word =helper(word)
            word =helper(word)
           
            if word in lexicon_positives:
                if word in scores:
                    scores[word] = scores[word] + 0.5
                else:
                    scores[word] = 1
                pos = pos + scores[word]
            if word in lexicon_negatives:
                if word in scores:
                    scores[word] = scores[word] + 0.5
                else:
                    scores[word] = 1
                neg = neg + scores[word]
               
           
        score = pos - neg
        if score < 0:
            final.append('n')
        elif score > 0:
            final.append('p')
        else:
            final.append('d')
   
    return final
       
           
   
    '''
    lexicon_positives: a list of strings, positive words
    lexicon_negatives: a list of strings, negative words
    testing_tweets: a List of tweets that this function must predict sentiment
    Returns: a List of predicted sentiment labels ('positive','negative','objective')
             --> equal to the length of testing_tweets
    '''

def helper(word):
    try:
        if(len(word) == 0):
            return word
        if(word == '\'' or word == '.' or word == ',' or word == '!' or word == '?' or word == '\"' or word == '[' or word== ']') or word == '(' or word == ')' or word == '' or word == ' ' or word == '-' or word == ':' or word == ';':
            return word
        else:
            if word[-1] == '?' or word[-1] == '.' or word[-1] == '!' or word[-1] == "," or word[-1] == ':' or word[-1] == ";" or word[-1] == "\"" or word[-1] == '_' or word[-1] == '-' or word[-1] == '[' or word[-1] == ']' or word[-1] == ')' or word[-1] == '(':
                word = word[:-1]
            if word[0] == '?' or word[0] == '#' or word[0] == '.' or word[0] == '!' or word[0] == "," or word[0] == ':' or word[0] == ";" or word[0] == "\"" or word[0] == '_' or word[0] == '-' or word[0] == '[' or word[0] == ']' or word[0] == ')' or word[0] == '(':
                word = word[0:]
            else:
                pass
    except:
        pass
    return word



    
def isenglish(tweet):
    # Python 3.7 - fast!
    return tweet.isascii()

    # Python 3.6 - twice as slow...
    #return all(ord(c) < 128 for c in s)



#
# DO NOT CHANGE ANYTHING BELOW THIS LINE.
#

if __name__ == '__main__':

    # Command-line argument parser
   
    #negative = [i for i in open("negatives.txt").readlines() if i != ""]
    #positive = [i for i in open("positives.txt").readlines() if i != ""]
    #testing_tweets =  negative + positive
    #testing_labels = ['n'] * len(negative) + ['p'] * len(positive)
    parse = tweet_parser()
    twt = parse.tweets
    running = [twt[i].text for i in range(len(twt))if i % 5 == 0];
    dates = [twt[i].tweet_created for i in range(len(twt))if i % 5 == 0];
   
    tweets = data.Tweets()
    lexicon = tweets.get_lexicon()
    predicted_labels = label_with_lexicon(lexicon[0], lexicon[1], running)
       
    # EVALUATE
    #accuracy = data.evaluate(predicted_labels, testing_labels)
    #print('Final Accuracy: %.2f%%\n\n' % (accuracy))
    neg = open("neg_test.txt", 'w')
    pos = open("pos_test.txt", 'w')
    for i in range(len(predicted_labels)):
        if(predicted_labels[i] == 'n'):
            neg.write(dates[i] + "\n")
        if(predicted_labels[i] == 'p'):
            pos.write(dates[i] + "\n")
    neg.close()
    pos.close()
