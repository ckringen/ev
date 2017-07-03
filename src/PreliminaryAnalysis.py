
# coding: utf-8

import pandas as pd
import numpy as np


def readData( fname ):
    trials = pd.read_csv( fname ) 
    return trials

def columnNames( dataframe ):
    return list(dataframe.columns.values)

# get rid of bugged data, which amounts to 9416 records
def removeBugged( dataframe ):
    return dataframe[dataframe['Bugged'] != "Bugged"]

# add column for whether produced matches target
def ProdMatchesTgt(dataframe_row):
    if dataframe_row['Target Sentence'] == dataframe_row['Produced Sentence']:
        return True
    else:
        return False        

# how many bigrams from the target appeared in the production
# divided by the total number of bigrams in the target
def getBigrams( string ):
    bigs = []
    sep = string.lower().split()
    for k,v in enumerate(sep):
        if k == len(sep) - 1:
            break
        else:
            bigs.append((v,sep[k+1]))
    return bigs

def searchForBigrams( bigrams_prod, bigrams_tgt ):
    ''' bigrams is a list of tuples of word pairs, returns number of bigrams from tgt in prod
        divided by total number in prod 
    '''
    # set intersection
    bigList = [bigrams_prod,bigrams_tgt]
    bigList = [set(a) for a in bigList]
    
    numProdBig = len(bigList[1])
    intersectionTgtBig = set.intersection(*bigList)

    return len( intersectionTgtBig ) / numProdBig


def bigramDriver(dataframe_row):
    b1 = getBigrams(dataframe_row['Produced Sentence'])
    b2 = getBigrams(dataframe_row['Target Sentence'])
    
    proportion = searchForBigrams(b1,b2)
    return proportion


def levenshtein(s, t):
        '''
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
        Iterative with two matrix rows. Between production and original 
        '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]

    
def editDriver( dataframe_row ):
    a = dataframe_row['Produced Sentence']
    b = dataframe_row['Target Sentence']
    
    return levenshtein( a, b )


# add column for longest matching substring
def longest_common_substring(s1, s2):
    '''
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python_3
    '''
   m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
   longest, x_longest = 0, 0
   for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
   return s1[x_longest - longest: x_longest]


def lcsDriver( dataframe_row ):
    b1 = dataframe_row['Produced Sentence']
    b2 = dataframe_row['Target Sentence']
    
    lcs = longest_common_substring(b1,b2)
    return lcs


# https://github.com/clips/pattern/blob/master/pattern/vector/stopwords-en.txt
stop = set(''''d, 'll, 'm, 're, 's, 't, n't, 've, a, aboard, about, above, across, after, again, against, all, almost, alone, along, alongside, already, also, although, always, am, amid, amidst, among, amongst, an, and, another, anti, any, anybody, anyone, anything, anywhere, are, area, areas, aren't, around, as, ask, asked, asking, asks, astride, at, aught, away, back, backed, backing, backs, bar, barring, be, became, because, become, becomes, been, before, began, behind, being, beings, below, beneath, beside, besides, best, better, between, beyond, big, both, but, by, came, can, can't, cannot, case, cases, certain, certainly, circa, clear, clearly, come, concerning, considering, could, couldn't, daren't, despite, did, didn't, differ, different, differently, do, does, doesn't, doing, don't, done, down, down, downed, downing, downs, during, each, early, either, end, ended, ending, ends, enough, even, evenly, ever, every, everybody, everyone, everything, everywhere, except, excepting, excluding, face, faces, fact, facts, far, felt, few, fewer, find, finds, first, five, following, for, four, from, full, fully, further, furthered, furthering, furthers, gave, general, generally, get, gets, give, given, gives, go, goes, going, good, goods, got, great, greater, greatest, group, grouped, grouping, groups, had, hadn't, has, hasn't, have, haven't, having, he, he'd, he'll, he's, her, here, here's, hers, herself, high, high, high, higher, highest, him, himself, his, hisself, how, how's, however, i, i'd, i'll, i'm, i've, idem, if, ilk, important, in, including, inside, interest, interested, interesting, interests, into, is, isn't, it, it's, its, itself, just, keep, keeps, kind, knew, know, known, knows, large, largely, last, later, latest, least, less, let, let's, lets, like, likely, long, longer, longest, made, make, making, man, many, may, me, member, members, men, might, mightn't, mine, minus, more, most, mostly, mr, mrs, much, must, mustn't, my, myself, naught, near, necessary, need, needed, needing, needn't, needs, neither, never, new, new, newer, newest, next, no, nobody, non, none, noone, nor, not, nothing, notwithstanding, now, nowhere, number, numbers, of, off, often, old, older, oldest, on, once, one, oneself, only, onto, open, opened, opening, opens, opposite, or, order, ordered, ordering, orders, other, others, otherwise, ought, oughtn't, our, ours, ourself, ourselves, out, outside, over, own, part, parted, parting, parts, past, pending, per, perhaps, place, places, plus, point, pointed, pointing, points, possible, present, presented, presenting, presents, problem, problems, put, puts, quite, rather, really, regarding, right, right, room, rooms, round, said, same, save, saw, say, says, second, seconds, see, seem, seemed, seeming, seems, seen, sees, self, several, shall, shan't, she, she'd, she'll, she's, should, shouldn't, show, showed, showing, shows, side, sides, since, small, smaller, smallest, so, some, somebody, someone, something, somewhat, somewhere, state, states, still, still, such, suchlike, sundry, sure, take, taken, than, that, that's, the, thee, their, theirs, them, themselves, then, there, there's, therefore, these, they, they'd, they'll, they're, they've, thine, thing, things, think, thinks, this, those, thou, though, thought, thoughts, three, through, throughout, thus, thyself, till, to, today, together, too, took, tother, toward, towards, turn, turned, turning, turns, twain, two, under, underneath, unless, unlike, until, up, upon, us, use, used, uses, various, versus, very, via, vis-a-vis, want, wanted, wanting, wants, was, wasn't, way, ways, we, we'd, we'll, we're, we've, well, wells, went, were, weren't, what, what's, whatall, whatever, whatsoever, when, when's, where, where's, whereas, wherewith, wherewithal, whether, which, whichever, whichsoever, while, who, who's, whoever, whole, whom, whomever, whomso, whomsoever, whose, whosoever, why, why's, will, with, within, without, won't, work, worked, working, works, worth, would, wouldn't, ye, year, years, yet, yon, yonder, you, you'd, you'll, you're, you've, you-all, young, younger, youngest, your, yours, yourself, yourselves'''.split(', '))

def removeStopWords( s ):
    production = s.split( )
    for i in production:
        if i in stop:
            production.remove(i)
    return production
            
def deltaDistanceDriver(dataframe_row):    
    prod_content = dataframe_row["Target Sentence"]
        
    target = dataframe_row['Produced Sentence']
    target_content = ' '.join(removeStopWords(target))
    bigrams = searchForBigrams(target_content)

    matches_ratios = []
    for bigram in bigrams:
        match = re.findall(r"{0}\s(.*)\s{1}".format(bigram[0], bigram[1]), prod_content)
        if match:
            matches = match[0].split()
            ratio = len(matches) / len(bigrams)
            matches_ratios.append((match,ratio))



def writeToFile( dataframe, path ):
    dataframe.writeCSV( path )
            
if __name__ == "__main__":

    # note: we manually changed the header line of the csv,
    # removing the spaces between commas and modifying the last column name
    
    df = readData( "../data/processed_data.csv" )
    
    removeBugged( df )
    
    df['ProdMatchesOrig'] = df.apply(ProdMatchesTgt, axis=1)
    
    df['proportionMatchingBigram'] = df.apply(bigramDriver, axis=1)

    df['editDist'] = df.apply(editDriver, axis=1)

    df['LCS'] = df.apply(lcsDriver, axis=1)

    df['deltaDistance'] = df.apply(deltaDistanceDriver, xis=1)

    writeToFile( df, "analyzed_data.csv")
