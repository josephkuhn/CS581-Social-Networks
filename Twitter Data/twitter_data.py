#  Author: Joseph Kuhn

# twitter_data.py searches Twitter for tweets matching a search term,
#      up to a maximum number

# to run from terminal window:
#        python3  twitter_data.py  --search_term1  mysearch1  --search_term2 mysearch2 --search_max  mymaxresults
# where:  mysearch1 is the first term the user wants to search for;  default = music
#   and:  mysearch2 is the second term the user wants to search for; default = movie
#   and:  mymaxresults is the maximum number of resulta;  default = 30
# for example:
#        python twitter_data.py --search_term1 trump --search_term2 obama --search_max 30

# other options used in the search:  lang = "en"  (English language tweets)
#  and  result_type = "popular"  (asks for most popular rather than most recent tweets)

# The program uses the TextBlob sentiment property to analyze the tweet for:
#  polarity (range -1 to 1)  and
#  subjectivity (range 0 to 1 where 0 is objective and 1 is subjective)

# The program creates a .csv output file with a line for each tweet
#    including tweet data items and the sentiment information

# This program will pull up to search_max tweets from each term that is input.
# It will determine the values of subjectivity and polarity, and will pull data such as number of retweets,
# the users who posted the tweets, the dates the tweets were posted, etc.
# It will then compare these results between the two terms, determining which search term is more polarizing,
# which term has more objective content versus subjective, and which is more popular in terms of activity (retweets).
# Finally, it will print these results in easy to read, orderly terms.

from textblob import TextBlob  # needed to analyze text for sentiment
import argparse  # for parsing the arguments in the command line
import csv  # for creating output .csv file
import tweepy  # Python twitter API package
import unidecode  # for processing text fields in the search results

### PUT AUTHENTICATION KEYS HERE ###
CONSUMER_KEY = "dxdWDtIYSS0V6r4Kimtkuh79k"
CONSUMER_KEY_SECRET = "9qpnVDXxgT9iUbcFPnoqpvVUPTbzCO9hJSTeK4keZANLh2ZRyl"
ACCESS_TOKEN = "623049678-5jahRsprLfRx1ZYqKH65SmkrYFkGaSVFHMle8NdU"
ACCESS_TOKEN_SECRET = "KIhOXiDOSAmMqLmHLLVWgBBpK4CGhNp8Yh4bJSFkjlPwc"

# AUTHENTICATION (OAuth)
authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate)

# Get the input arguments - search_term and search_max
parser = argparse.ArgumentParser(description='Twitter Search')
parser.add_argument("--search_term1", action='store', dest='search_term1', default="music")
parser.add_argument("--search_term2", action='store', dest='search_term2', default="movie")
parser.add_argument("--search_max", action='store', dest='search_max', default=30)
args = parser.parse_args()

search_term1 = args.search_term1
search_term2 = args.search_term2
search_max = int(args.search_max)

# create a .csv file to hold the results, and write the header line
csvFile = open('twitter_results1.csv', 'w')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["username", "userid", "created", "text", "retweets", "followers",
                    "friends", "polarity", "subjectivity"])

numTweets1 = 0
numTweets2 = 0
totalPolarity1 = 0.0
totalPolarity2 = 0.0
totalSubjectivity1 = 0.0
totalSubjectivity2 = 0.0
totalRetweets1 = 0
totalRetweets2 = 0

# do the twitter search
for tweet in tweepy.Cursor(api.search, q=search_term1, lang="en",
                           result_type="popular").items(search_max):
    created = tweet.created_at  # date created
    text = tweet.text  # text of the tweet
    text = unidecode.unidecode(text)
    retweets = tweet.retweet_count  # number of retweets
    username = tweet.user.name  # user name
    userid = tweet.user.id  # userid
    followers = tweet.user.followers_count  # number of user followers
    friends = tweet.user.friends_count  # number of user friends
    totalRetweets1 += retweets

    # use TextBlob to determine polarity and subjectivity of tweet
    text_blob = TextBlob(text)
    polarity = text_blob.polarity
    totalPolarity1 += polarity
    numTweets1 += 1
    subjectivity = text_blob.subjectivity
    totalSubjectivity1 += subjectivity

    # write tweet info to .csv tile
    csvWriter.writerow([username, userid, created, text, retweets, followers,
                        friends, polarity, subjectivity])
csvFile.close()
csvFile = open('twitter_results2.csv', 'w')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["username", "userid", "created", "text", "retweets", "followers",
                    "friends", "polarity", "subjectivity"])

for tweet in tweepy.Cursor(api.search, q=search_term2, lang="en",
                           result_type="popular").items(search_max):
    created = tweet.created_at  # date created
    text = tweet.text  # text of the tweet
    text = unidecode.unidecode(text)
    retweets = tweet.retweet_count  # number of retweets
    username = tweet.user.name  # user name
    userid = tweet.user.id  # userid
    followers = tweet.user.followers_count  # number of user followers
    friends = tweet.user.friends_count  # number of user friends
    totalRetweets2 += retweets

    # use TextBlob to determine polarity and subjectivity of tweet
    text_blob = TextBlob(text)
    polarity = text_blob.polarity
    totalPolarity2 += polarity
    numTweets2 += 1
    subjectivity = text_blob.subjectivity
    totalSubjectivity2 += subjectivity

    # write tweet info to .csv tile
    csvWriter.writerow([username, userid, created, text, retweets, followers,
                        friends, polarity, subjectivity])

csvFile.close()

totalPolarity1 /= numTweets1  # divide the total polarity number by the number of tweets analyzed
totalPolarity2 /= numTweets2
totalSubjectivity1 /= numTweets1 # divide the total polarity number by the number of tweets analyzed
totalSubjectivity2 /= numTweets2

isSubjective1 = False
isSubjective2 = False
isMoreSubjective = ""
isMorePositive = ""
typePolarity1 = ""
typePolarity2 = ""
hasMoreRetweets = ""
# determine which terms are more subjective, which has higher polarity, and which has more retweets
if totalSubjectivity1 > totalSubjectivity2:
    isMoreSubjective = search_term1
elif totalSubjectivity2 > totalSubjectivity1:
    isMoreSubjective = search_term2
else:
    isMoreSubjective = "Neither"
if totalPolarity1 > totalPolarity2:
    isMorePositive = search_term1
elif totalPolarity2 > totalPolarity1:
    isMorePositive = search_term2
else:
    isMorePositive = "Neither"
if totalRetweets1 > totalRetweets2:
    hasMoreRetweets = search_term1
elif totalRetweets2 > totalRetweets1:
    hasMoreRetweets = search_term2
else:
    hasMoreRetweets = "Neither"


# Print the search terms and number of max results
print("The first search term was \"" + str(search_term1) + "\".")
print("The second search term was \"" + str(search_term2) + "\".")
print("The number of maximum results that were pulled from Twitter was \"" + str(search_max) + "\".")
# Print the number of retweets for each term and compare them
print("The \"" + str(search_term1) + "\" search has a total of " + str(totalRetweets1) + " retweets from the " + str(search_max) + " tweets pulled.")
print("The \"" + str(search_term2) + "\" search has a total of " + str(totalRetweets2) + " retweets from the " + str(search_max) + " tweets pulled.")
if totalRetweets1 > totalRetweets2:
    print("This means that tweets mentioning \"" + str(search_term1) + "\" have more retweets and user involvement than tweets mentioning \"" + str(search_term2) + "\".")
elif totalRetweets2 > totalRetweets1:
    print("This means that tweets mentioning \"" + str(search_term2) + "\" have more retweets and user involvement than tweets mentioning \"" + str(search_term1) + "\".")
else:
    print("This means that tweets mentioning \"" + str(search_term1) + "\" have the same number of retweets and user involvement as weets mentioning \"" + str(search_term2) + "\".")
# Print the polarity value of each term and compare them
if totalPolarity1 > 0:
    print("The average polarity of the \"" + search_term1 + "\" search is " + str(totalPolarity1) + ". This means that the tweets from this search generate a positive reaction on average.")
    typePolarity1 = "positive"
elif totalPolarity1 < 0:
    print("The average polarity of the \"" + search_term1 + "\" search is " + str(totalPolarity1) + ". This means that the tweets from this search generate a negative reaction on average.")
    typePolarity1 = "negative"
else:
    typePolarity1 = "neutral"
    print("The average polarity of the \"" + search_term1 + "\" search is " + str(totalPolarity1) + ". This means that the tweets from this search generate a neutral reaction on average.")

if totalPolarity2 > 0:
    print("The average polarity of the \"" + search_term2 + "\" search is " + str(totalPolarity2) + ". This means that the tweets from this search generate a positive reaction on average.")
    typePolarity2 = "positive"
elif totalPolarity2 < 0:
    typePolarity2 = "negative"
    print("The average polarity of the \"" + search_term2 + "\" search is " + str(totalPolarity2) + ". This means that the tweets from this search generate a negative reaction on average.")
else:
    typePolarity2 = "neutral"
    print("The average polarity of the \"" + search_term2 + "\" search is " + str(totalPolarity2) + ". This means that the tweets from this search generate a neutral reaction on average.")
# Print the subjectivity value of each term and compare them
if totalSubjectivity1 >= 0.5:
    isSubjective1 = True
    print ("The average subjectivity value of the \"" + search_term1 + "\" search is " + str(totalSubjectivity1) + ". This means that the tweets from this search are on average more subjective than objective.")
else:  # totalSubjectivity1 < 0.5
    print("The average subjectivity value of the \"" + search_term1 + "\" search is " + str(totalSubjectivity1) + ". This means that the tweets from this search are on average more objective than subjective.")

if totalSubjectivity2 >= 0.5:
    isSubjective2 = True
    print ("The average subjectivity value of the \"" + search_term2 + "\" search is " + str(totalSubjectivity2) + ". This means that the tweets from this search are on average more subjective than objective.")
else:  # totalSubjectivity2 < 0.5
    print("The average subjectivity value of the \"" + search_term2 + "\" search is " + str(totalSubjectivity2) + ". This means that the tweets from this search are on average more objective than subjective.")
print()
# Recap the results for the first term, declaring the individual and compared results
print("To recap the results from the \"" + search_term1 + "\" search:")
if isSubjective1 == True:
    print("The tweets are on average more subjective than objective.", end=" ")
    if isMoreSubjective == search_term1:
        print("The tweets about this term are more subjective than the tweets about the \"" + search_term2 + "\" term.")
    elif isMoreSubjective == search_term2:
        print("However, the tweets about this term are not as subjective as the tweets about the \"" + search_term2 + "\" term.")
    else:
        print("They have the same average level of subjectivity as the tweets about the \"" + search_term2 + "\" term.")
else:
    print("The tweets are on average more objective than subjective.", end=" ")
    if isMoreSubjective == search_term1:
        print("However, they are still more subjective than the tweets about the \"" + search_term2 + "\" term.")
    elif isMoreSubjective == search_term2:
        print("They are less subjective than the tweets about the \"" + search_term2 + "\" term.")
    else:
        print("They have the same average level of subjectivity as the tweets about the \"" + search_term2 + "\" term.")
if typePolarity1 == "positive":
    print("The polarity of this search is " + typePolarity1 + ".", end=" ")
    if isMorePositive == search_term1:
        print("It is more positive than tweets about the \"" + search_term2 + "\" term.")
    elif isMorePositive == search_term2:
        print("However, it is not as positive as the tweets about the \"" + search_term2 + "\" term.")
    else:
        print("It has the same level of polarity as the tweets about the \"" + search_term2 + "\" term.")
elif typePolarity1 == "negative":
    print("The polarity of this search is " + typePolarity1 + ".", end=" ")
    if isMorePositive == search_term1:
        print("However, it is more positive than tweets about the \"" + search_term2 + "\" term.")
    elif isMorePositive == search_term2:
        print("It is not as positive as the tweets about the \"" + search_term2 + "\" term.")
    else:
        print("It has the same level of polarity as the tweets about the \"" + search_term2 + "\" term.")
elif typePolarity1 == "neutral":
    print("The polarity of this search is " + typePolarity1 + ".", end=" ")
    if isMorePositive == search_term1:
        print("However, it is more positive than tweets about the \"" + search_term2 + "\" term.")
    elif isMorePositive == search_term2:
        print("It is not as positive as the tweets about the \"" + search_term2 + "\" term.")
    else:
        print("It has the same level of polarity as the tweets about the \"" + search_term2 + "\" term.")

if hasMoreRetweets == search_term1:
    print("Finally, this search term has more retweets than the tweets about the \"" + search_term2 + "\" term.")
elif hasMoreRetweets == search_term2:
    print("Finally, this search term has less retweets than the tweets about the \"" + search_term2 + "\" term.")
else:
    print("Finally, this search term has the same amount of retweets as the tweets about the \"" + search_term2 + "\" term.")
print()
# Recap the results for the second term, declaring the individual and compared results
print("To recap the results from the \"" + search_term2 + "\" search:")
if isSubjective2 == True:
    print("The tweets are on average more subjective than objective.", end=" ")
    if isMoreSubjective == search_term2:
        print("The tweets about this term are more subjective than the tweets about the \"" + search_term1 + "\" term.")
    elif isMoreSubjective == search_term1:
        print("However, the tweets about this term are not as subjective as the tweets about the \"" + search_term1 + "\" term.")
    else:
        print("They have the same average level of subjectivity as the tweets about the \"" + search_term1 + "\" term.")
else:
    print("The tweets are on average more objective than subjective.", end=" ")
    if isMoreSubjective == search_term2:
        print("However, they are still more subjective than the tweets about the \"" + search_term1 + "\" term.")
    elif isMoreSubjective == search_term1:
        print("They are less subjective than the tweets about the \"" + search_term1 + "\" term.")
    else:
        print("They have the same average level of subjectivity as the tweets about the \"" + search_term1 + "\" term.")
if typePolarity2 == "positive":
    print("The polarity of this search is " + typePolarity2 + ".", end=" ")
    if isMorePositive == search_term2:
        print("It is more positive than tweets about the \"" + search_term1 + "\" term.")
    elif isMorePositive == search_term1:
        print("However, it is not as positive as the tweets about the \"" + search_term1 + "\" term.")
    else:
        print("It has the same level of polarity as the tweets about the \"" + search_term1 + "\" term.")
elif typePolarity2 == "negative":
    print("The polarity of this search is " + typePolarity2 + ".", end=" ")
    if isMorePositive == search_term2:
        print("However, it is more positive than tweets about the \"" + search_term1 + "\" term.")
    elif isMorePositive == search_term1:
        print("It is not as positive as the tweets about the \"" + search_term1 + "\" term.")
    else:
        print("It has the same level of polarity as the tweets about the \"" + search_term1 + "\" term.")
elif typePolarity2 == "neutral":
    print("The polarity of this search is " + typePolarity2 + ".", end=" ")
    if isMorePositive == search_term2:
        print("However, it is more positive than tweets about the \"" + search_term1 + "\" term.")
    elif isMorePositive == search_term1:
        print("It is not as positive as the tweets about the \"" + search_term1 + "\" term.")
    else:
        print("It has the same level of polarity as the tweets about the \"" + search_term1 + "\" term.")

if hasMoreRetweets == search_term2:
    print("Finally, this search term has more retweets than the tweets about the \"" + search_term1 + "\" term.")
elif hasMoreRetweets == search_term1:
    print("Finally, this search term has less retweets than the tweets about the \"" + search_term1 + "\" term.")
else:
    print("Finally, this search term has the same amount of retweets as the tweets about the \"" + search_term1 + "\" term.")