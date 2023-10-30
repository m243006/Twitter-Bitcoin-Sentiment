a = open("useful.txt").readlines()
for i in range(len(a)):
    if i % 13 == 9:
        positives = open("positives.txt", 'a')
        negatives = open("negatives.txt", 'a')
        b = input("Is this tweet positive? (p) or negative? (n)")
        if(b == 'p'):
            positives.write(a[i] + "\n")
        else:
            negatives.write(a[i] + "\n")
        positives.close()
        negatives.close()
